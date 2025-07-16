import asyncio
import re
import html
import json
import time
import random
import string
from datetime import datetime
from typing import List, Dict, Any, Optional, Set

import aiohttp
import bs4
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from submodule_integrations.models.integration import Integration
from submodule_integrations.oncoemr.generic_note_model import CatchAllModel
from submodule_integrations.oncoemr.oncoemr_models import FollowupNoteTemplateModel
from submodule_integrations.utils.errors import (
    IntegrationAuthError,
    IntegrationAPIError,
)
from submodule_integrations.oncoemr.consultation_models import (
    ConsultationNoteTemplateModel,
)
from submodule_integrations.oncoemr.consultation_mappings import (
    CONSULTATION_TEXTFIELDS_MAPPING,
    CONSULTATION_RADIO_BUTTONS_MAPPING,
    CONSULTATION_CHECKBOXES_MAPPING,
)
from submodule_integrations.oncoemr.oncoemr_mapping import (
    FOLLOWUP_TEXTFIELDS_MAPPING,
    FOLLOWUP_RADIO_BUTTONS_MAPPING,
    FOLLOWUP_CHECKBOXES_MAPPING,
)


class OncoEmrIntegration(Integration):
    def __init__(
            self,
            domain: str,
            token: str,
            location_id: str,
            network_requester=None,
            user_agent: str = UserAgent().random,
    ):
        super().__init__("oncoemr")
        self.user_agent = user_agent
        self.url = domain if "https://" in domain else f"https://{domain}"
        self.network_requester = network_requester

        self.headers = {
            "Host": domain.replace("https://", ""),
            "User-Agent": self.user_agent,
            "Cookie": token,
            "Accept": "*/*",
            "Accept-Encoding": "gzip",
        }

        self.user_id = None
        self.group_id = None
        self.location_id = location_id

    @classmethod
    async def create(
            cls,
            domain: str,
            token: str,
            location_id: str,
            network_requester=None,
            user_agent: str = UserAgent().random,
    ):
        """Async factory method that ensures state data is loaded before returning the instance"""
        instance = cls(
            domain=domain,
            token=token,
            location_id=location_id,
            network_requester=network_requester,
            user_agent=user_agent,
        )
        await instance._load_state_data()
        return instance

    async def _make_request(
            self, method: str, url: str, **kwargs
    ) -> dict | str | bytes:
        if self.network_requester is not None:
            response = await self.network_requester.request(
                method, url, process_response=self._handle_response, **kwargs
            )
            return response
        else:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse):
        if response.status == 200:
            try:
                data = await response.json()
            except (json.decoder.JSONDecodeError, aiohttp.ContentTypeError):
                data = await response.text()

            return data

        if response.status == 401:
            raise IntegrationAuthError(
                "OncoEMR: Auth failed",
                response.status,
            )
        elif response.status == 400:
            raise IntegrationAPIError(
                self.integration_name,
                f"{response.reason}",
                response.status,
                response.reason,
            )
        else:
            raise IntegrationAPIError(
                self.integration_name,
                f"{await response.text()}",
                response.status,
                response.reason,
            )

    async def _load_state_data(self):
        path = self.url + "/nav/visit-list"
        response = await self._make_request("GET", path, headers=self.headers)
        soup = self._create_soup(response)

        data_script = soup.select_one("script#json\\:piwikOptions")
        data = json.loads(data_script.text.strip())
        self.user_id = data.get("userId")
        self.group_id = data.get("groupId")

    async def _verify_patient_exists(self, patient_id: str):
        patient_basic_info = await self._patient_partial_page_info(
            patient_id=patient_id
        )
        header_data = patient_basic_info.get("HeaderData")
        if header_data.get("PatientMrn") or header_data.get("PatientDisplayName"):
            return

        demographics = await self._basic_patient_demographics_data(patient_id)
        if demographics is not None:
            return

        raise IntegrationAPIError(
            integration_name=self.integration_name,
            error_code="not_found",
            status_code=404,
            message=f"Patient not found for ID: `{patient_id}`",
        )

    async def _get_physicians(self) -> List[Dict]:
        path = self.url + "/User/PhysicianUsers"
        headers = self.headers.copy()
        headers["X-Requested-With"] = "XMLHttpRequest"

        response = await self._make_request("GET", url=path, headers=headers)
        return response

    async def fetch_physicians(self):
        physicians = await self._get_physicians()

        processed = []
        for physician in physicians:
            data = {
                "id": physician["UserId"],
                "first_name": physician["FirstName"],
                "last_name": physician["LastName"],
                "username": physician["UserName"],
            }

            processed.append(data)

        return processed

    async def fetch_visit_list(self, doctor_ids: List[str], selected_date: str | None):
        doctors_list = await self.fetch_physicians()
        providers = []
        for doctor_id in doctor_ids:
            this_doctor = next(
                (doctor for doctor in doctors_list if doctor.get("id") == doctor_id), None
            )
            if this_doctor is None:
                raise IntegrationAPIError(
                    integration_name=self.integration_name,
                    error_code="not_found",
                    status_code=404,
                    message=f"Doctor not found for ID: `{doctor_id}",
                )

            providers.append(doctor_id)

        providers_str = ",".join(providers)

        path = f"{self.url}/VisitList/UpdateVisitList"

        if selected_date is None:
            selected_date = self._get_current_date()

        first_param = {
            "sVisitDate": f"{selected_date}",
            "sLocID": -1,
            "sResource": f"{providers_str}",
            "bNewLocation": False,
            "bNewResource": True,
            "sMDUID": f"{providers_str}",
            "bShowPatLocCol": "True",
            "bMDVisitsOnly": "True",
            "bHideUnscheduled": "True",
            "olHideFilters": ["chkHideUnscheduled"],
            "bShowVisitsOnly": True,
        }

        params = {
            "sVisitListRequest": json.dumps(first_param),
            "_": str(int(time.time() * 1000)),  # Current timestamp in milliseconds
        }

        response = await self._make_request(
            "GET", url=path, params=params, headers=self.headers
        )
        if isinstance(response, dict):
            visit_html = response.get("sViewHtml")
        else:
            visit_html = response

        parsed_visit_list = self._parse_patient_table(visit_html)
        return parsed_visit_list

    async def _basic_patient_demographics_data(self, patient_id: str) -> dict:
        path = self.url + "/pc/demographics"
        params = {
            "patientId": f"{patient_id}",
            "includeDeletedOrMerged": "false",
        }
        response = await self._make_request(
            "GET", url=path, params=params, headers=self.headers
        )
        return response

    async def _patient_status_info(self, patient_id: str) -> dict:
        path = self.url + "/PatientPortal/Status"
        params = {
            "patientId": f"{patient_id}",
        }
        response = await self._make_request(
            "GET", url=path, params=params, headers=self.headers
        )
        return response

    async def _patient_partial_page_info(self, patient_id: str) -> dict:
        path = self.url + "/PartialPage/GetPageInfoForPatient"
        first_param = {
            "sPID": f"{patient_id}",
            "sUID": f"{self.user_id}",
            "sGID": f"{self.group_id}",
            "bNewPatient": True,
            "bCheckAccess": True,
            "sRequestedPage": "$default$",
            "sSessionKey": "",
            "oAttr": {
                "bIsPatientPage": True,
                "bReloadOnNewPatient": False,
                "sHelpFileName": "",
                "sTitle": "",
                "sLocName": "",
                "bShowFind": True,
                "bHidePatient": False,
                "sController": "",
                "sAction": "",
                "sOnload": "PD_VISITLIST.localStartup",
            },
        }
        params = {
            "sPageInfo": json.dumps(first_param),
            "_": str(int(time.time() * 1000)),
        }
        response = await self._make_request(
            "GET", url=path, params=params, headers=self.headers
        )
        return response

    async def _patient_demographics_html(self, patient_id: str) -> str:
        params = {
            "PID": f"{patient_id}",
            "locationId": f"{self.location_id}",
            "_PP": "1",
            "_": str(int(time.time() * 1000)),
        }
        path = self.url + "/WebForms/pages_pd/PD_Demographics.aspx"
        response = await self._make_request(
            "GET", url=path, params=params, headers=self.headers
        )
        return response

    async def fetch_patient_demographics(self, patient_id: str):
        await self._verify_patient_exists(patient_id=patient_id)

        demographics = await self._basic_patient_demographics_data(patient_id)
        if demographics is None:
            return {
                "success": False,
                "message": f"No patient found with ID: `{patient_id}`",
            }

        demo_html = await self._patient_demographics_html(patient_id)
        demo_soup = self._create_soup(demo_html)

        employer_elem = demo_soup.select_one("span#lblEmployer")
        employer = employer_elem.text.strip() if employer_elem else None
        occupation_elem = demo_soup.select_one("span#lblOccupation")
        occupation = occupation_elem.text.strip() if occupation_elem else None
        physician_elem = demo_soup.select_one("span#lblDoc")
        physician = physician_elem.text.strip() if physician_elem else None
        advance_directive_elem = demo_soup.select_one("span#lblAdvancedDirective")
        advance_directive = (
            advance_directive_elem.text.strip() if advance_directive_elem else None
        )
        industry_elem = demo_soup.select_one("span#lblIndustry")
        industry = industry_elem.text.strip() if industry_elem else None
        pref_clinic_elem = demo_soup.select_one("span#lblLocation")
        pref_clinic = pref_clinic_elem.text.strip() if pref_clinic_elem else None
        status_elem = demo_soup.select_one("span#lblStatus")
        status = status_elem.text.strip() if status_elem else None
        benefit_elem = demo_soup.select_one("span#lblBenefitStatus")
        benefit = benefit_elem.text.strip() if benefit_elem else None

        data = {
            "patient_id": patient_id,
            "physician": physician,
            "dob": demographics.get("dateOfBirth"),
            "gender": demographics.get("gender"),
            "first_name": demographics.get("firstName"),
            "last_name": demographics.get("lastName"),
            "middle_name": demographics.get("middleName"),
            "preferred_name": demographics.get("preferredName"),
            "pronouns": demographics.get("pronouns"),
            "has_medicare": demographics.get("hasMedicare"),
            "birth_info": demographics.get("birthDetails"),
            "deceased_date": demographics.get("deceasedDate"),
            "preferred_language": demographics.get("preferredLanguageCode"),
            "ethnicity": demographics.get("ethnicityCodes"),
            "mothers_maiden_name": demographics.get("mothersMaidenName"),
            "record_number": demographics.get("mrn"),
            "ssn": demographics.get("ssn"),
            "affiliated_tribe": demographics.get("tribalAffiliation"),
            "marital_status": demographics.get("maritalStatusCode"),
            "employer": employer,
            "occupation": occupation,
            "industry": industry,
            "preferred_clinic": pref_clinic,
            "status": status,
            "advance_directive": advance_directive,
            "is_test_patient": demographics.get("isTestPatient"),
            "benefit_status": benefit,
        }

        return data

    async def _patient_allergies_data(self, patient_id: str) -> list[dict]:
        params = {
            "patientId": patient_id,
        }
        path = self.url + "/pc/allergies"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        return response

    async def _patient_oncology_data(self, patient_id: str) -> list[dict]:
        params = {
            "patientId": patient_id,
            "showHccStatus": False,
        }
        path = self.url + "/pc/oncology-diagnoses"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        return response

    async def _get_all_notes(self, patient_id: str) -> list[dict]:
        params = {
            "PID": patient_id,
            "locationId": f"{self.location_id}",
            "_PP": 1,
            "_": str(int(time.time() * 1000)),
        }
        path = self.url + "/WebForms/pages_pd/PD_DocMDMain.aspx"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        soup = self._create_soup(response)
        note_elems = soup.select("a.PDMenu")
        notes_list = []

        pattern1 = r'editDoc\("([^"]+)"\)'
        pattern2 = r'window\.openDocumentViewer\("([^"]+)",\s*"([^"]+)"'

        for note_elem in note_elems:
            name = note_elem.text.strip()
            onclick = note_elem.get("onclick")
            note_id = None

            # Try first pattern
            match = re.search(pattern1, onclick)
            if match:
                note_id = match.group(1)
            else:
                # Try second pattern
                match = re.search(pattern2, onclick)
                if match:
                    note_id = match.group(2)

            data = {
                "name": name,
                "note_id": note_id,
            }
            notes_list.append(data)

        return notes_list

    async def _get_note_data(self, patient_id: str, note_id: str) -> dict:
        params = {
            "patientId": patient_id,
            "noteIds": note_id,
        }
        path = self.url + "/pc/document-viewer-records"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        records = response.get("documentRecords")
        note_data = next((item for item in records if item.get("id") == note_id), None)
        return note_data

    async def _get_note_pdf_file(
            self, patient_id: str, note_id: str
    ) -> dict[str, str | bytes]:
        note_data = await self._get_note_data(patient_id, note_id)
        note_path = note_data.get("presignedUrl")

        return {
            "data": note_data,
            "file": note_path,
        }

    async def fetch_patient_notes(self, patient_id: str):
        await self._verify_patient_exists(patient_id=patient_id)

        notes = await self._get_all_notes(patient_id)
        note_files = []

        for note in notes:
            data = {}
            if note.get("note_id"):
                data = await self._get_note_pdf_file(
                    patient_id=patient_id,
                    note_id=note.get("note_id"),
                )
            else:
                data["status"] = "No Note ID"

            data["name"] = note.get("name")
            note_files.append(data)

        return note_files

    async def _followup_note_page(self, patient_id: str):
        path = self.url + "//WebForms/PD_DocOncoNoteDB.aspx"
        params = {
            "FID": "DO_06APW5AY04PK7CHWD1EP",
            "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
            "_SK": "",
            "__full": "true",
        }
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        return response

    async def make_followup_note(self, template: FollowupNoteTemplateModel):
        patient_id = template.patient_id
        await self._verify_patient_exists(patient_id=patient_id)

        note_page = await self._followup_note_page(patient_id=patient_id)

        note_soup = self._create_soup(note_page)
        note_guid_elem = note_soup.select_one("input#txtNoteGUID")
        note_guid = note_guid_elem.get("value")

        note_form_id_elem = note_soup.select_one("input#txtFormID")
        note_form_id = note_form_id_elem.get("value")

        existing_data = self._extract_form_data_bs(note_page)

        filled_template = self._apply_template_to_dict(
            template_model=template,
            target_dict=existing_data,
            checkboxes_mapping=FOLLOWUP_CHECKBOXES_MAPPING,
            radio_buttons_mapping=FOLLOWUP_RADIO_BUTTONS_MAPPING,
            textfields_mapping=FOLLOWUP_TEXTFIELDS_MAPPING,
        )
        output_parts = [f"{k}%01{v}" for k, v in filled_template.items()]
        output_string = "%02".join(output_parts)

        param_string = f"""
%02
%02
AsteraMedOncFollowUp-2023v9%02
Astera MedOnc Follow Up - 2023 v8%02
{self._get_current_date()}%02
{note_form_id}%02
background%02
Astera MedOnc Follow Up - 2023 v8%02
{self._get_current_date()}%02
%02
{self.group_id}%02
{patient_id}%02
%02
%02
PRINT%02
{note_guid}%02
MD Visit Note%02
{output_string}%02
PRINT
    """
        param_string = param_string.replace("\n", "").strip()

        query_json = {
            "sNameValues": param_string,
            "assessedDiagnosesData": "",
            "autoSaveCounter": "2",
            "hash": f"{int(time.time() * 1000)}{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}",
        }
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        path = self.url + "/VisitNotes/AutoSaveVisitNote"
        response = await self._make_request(
            "POST", path, json=query_json, headers=headers
        )

        if self._verify_note_str(response):
            return {
                "success": True,
            }
        else:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                status_code=500,
                error_code="server_error",
                message=f"Failed to process note: {response}",
            )

    async def _initial_consultation_note_page(self, patient_id: str):
        path = self.url + "//WebForms/PD_DocOncoNoteDB.aspx"
        params = {
            "FID": "DO_06APW5G421SENZ2PR3XB",
            "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
            "_SK": "",
            "__full": "true",
        }
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        return response

    async def make_consultation_note(self, template: ConsultationNoteTemplateModel):
        patient_id = template.patient_id
        await self._verify_patient_exists(patient_id=patient_id)

        note_page = await self._initial_consultation_note_page(patient_id=patient_id)

        note_soup = self._create_soup(note_page)
        note_guid_elem = note_soup.select_one("input#txtNoteGUID")
        note_guid = note_guid_elem.get("value")

        note_form_id_elem = note_soup.select_one("input#txtFormID")
        note_form_id = note_form_id_elem.get("value")

        existing_data = self._extract_form_data_bs(note_page)
        filled_template = self._apply_template_to_dict(
            template_model=template,
            target_dict=existing_data,
            checkboxes_mapping=CONSULTATION_CHECKBOXES_MAPPING,
            radio_buttons_mapping=CONSULTATION_RADIO_BUTTONS_MAPPING,
            textfields_mapping=CONSULTATION_TEXTFIELDS_MAPPING,
        )
        output_parts = [f"{k}%01{v}" for k, v in filled_template.items()]
        output_string = "%02".join(output_parts)

        param_string = f"""
%02
%02
AsteraMedOncInitialConsultation-2023v3%02
Astera MedOnc Initial Consultation - 2023 v3%02
{self._get_current_date()}%02
{note_form_id}%02
background%02
Astera MedOnc Initial Consultation - 2023 v3%02
{self._get_current_date()}%02
%02
{self.group_id}%02
{patient_id}%02
%02
%02
PRINT%02
{note_guid}%02
MD Visit Note%02
{output_string}%02
PRINT
    """
        param_string = param_string.replace("\n", "").strip()
        query_json = {
            "sNameValues": param_string,
            "assessedDiagnosesData": "",
            "autoSaveCounter": "1",
            "hash": f"{int(time.time() * 1000)}{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}",
        }

        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        path = self.url + "/VisitNotes/AutoSaveVisitNote"
        response = await self._make_request(
            "POST", path, json=query_json, headers=headers
        )

        if self._verify_note_str(response):
            return {
                "success": True,
            }
        else:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                status_code=500,
                error_code="server_error",
                message=f"Failed to process note: {response}",
            )

    async def _fetch_available_note_types(self):
        params = {
            'FT': 'VisitNote',
            'AJAX': '1',
            # '__OS': f'{self.group_id}~{self.user_id}',
            'M': 'sSwitchListRS',
            'P0': '[ShowAll]',
            '_': f'{int(time.time() * 1000)}',
        }
        path = self.url + "/WebForms/OncoEMR.aspx"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        soup = self._create_soup(response.get("Payload"))
        options = []

        # Extract all option elements
        for option in soup.find_all("option"):
            if len(option.get("value")) > 0:
                options.append(
                    {"value": option.get("value", ""), "text": option.text.strip()}
                )

        return options

    async def fetch_note_types(self):
        options = await self._fetch_available_note_types()
        cleaned = []
        for option in options:
            cleaned.append(option["text"])

        return cleaned

    async def _get_note_page(self, template_id: str, patient_id: str, note_id: str = None):
        path = self.url + "//WebForms/PD_DocOncoNoteDB.aspx"
        if note_id:
            params = {
                "NID": f"{note_id}",
                "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
                "_SK": "",
                "__full": "true",
            }
        else:
            params = {
                "FID": f"{template_id}",
                "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
                "_SK": "",
                "__full": "true",
            }
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        return response

    async def generic_notes_submit(self, note_name: str, patient_id: str, fields: dict, created_on: str = None,
                                   forward_to: str = None, note_category: str = None):
        # created_on: MM/DD/YYYY
        note_inputs = await self.generic_notes_fetch(
            note_name=note_name,
            patient_id=patient_id,
        )

        if forward_to:
            all_physicians = await self._get_physicians()
            forwarding_physician = next(
                (
                    item
                    for item in all_physicians
                    if item.get("UserId") == forward_to
                ),
                None,
            )
            if forwarding_physician is None:
                raise IntegrationAPIError(
                    integration_name=self.integration_name,
                    status_code=500,
                    error_code="server_error",
                    message=f"No physician found with ID `{forward_to}`",
                )

        note_types = await self._fetch_available_note_types()
        selected_note = next(
            (
                item
                for item in note_types
                if self._fuzzy_compare(note_name, item["text"])
            ),
            None,
        )
        cur_note_id = await self._fetch_latest_note_id(patient_id=patient_id, note_name=note_name)
        if "secure31" not in self.url:
            print(f"creating brand new note on {self.url}")
            cur_note_id = None

        note_page = await self._get_note_page(
            template_id=selected_note["value"], patient_id=patient_id, note_id=cur_note_id
        )
        existing_data = self._extract_form_data_bs(note_page)

        # break down `fields` into `textfields`, `radio_buttons`, and `checkboxes`
        submit_textfields = fields.get("textfields")
        submit_radio_buttons = fields.get("radio_buttons")
        submit_checkboxes = fields.get("checkboxes")

        merged_input = self._notes_textfields_merge_id_to_value(
            id_label=note_inputs["textfield_data"]["text_id_label"],
            label_value=submit_textfields,
        )
        applied_data = self._generic_notes_merge_new_with_existing(
            merged_input=merged_input,
            existing_data=existing_data,
        )

        # convert the radio button and checkboxes dict to expected form with correct id prefix
        radio_buttons_data = self._prepare_toggle_input_dict(data=submit_radio_buttons, prefix="FD_rdo")
        checkboxes_data = self._prepare_toggle_input_dict(data=submit_checkboxes, prefix="FD_chk")

        # merge new checkbox and radio button values into existing data
        applied_data.update(radio_buttons_data)
        applied_data.update(checkboxes_data)

        # merge direct id updates from operator into existing data
        direct_updates = fields.get("direct_updates")
        applied_data.update(direct_updates)

        applied_parts = [f"{k}%01{v}" for k, v in applied_data.items()]
        applied_string = "%02".join(applied_parts)

        note_soup = self._create_soup(note_page)
        note_guid_elem = note_soup.select_one("input#txtNoteGUID")
        note_guid = note_guid_elem.get("value")

        note_form_id_elem = note_soup.select_one("input#txtFormID")
        note_form_id = note_form_id_elem.get("value")

        if note_category is None:
            note_category_elem = note_soup.select_one("input#txtCategory")
            note_category = note_category_elem.get("value")

        date_pattern = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")
        if created_on:
            # First check basic format with regex
            if not date_pattern.match(created_on):
                raise IntegrationAPIError(
                    integration_name=self.integration_name,
                    status_code=400,
                    error_code="client_error",
                    message=f"Invalid date format for `created_on`: {created_on}. Expected MM/DD/YYYY.",
                )

            # Then check if it's a valid date
            try:
                datetime.strptime(created_on, "%m/%d/%Y")
            except ValueError:
                raise IntegrationAPIError(
                    integration_name=self.integration_name,
                    status_code=400,
                    error_code="client_error",
                    message=f"Invalid date for `created_on`: {created_on}. Date doesn't exist.",
                )

        if cur_note_id:
            created_on = None

        param_string = f"""
{cur_note_id if cur_note_id else ''}%02
{cur_note_id if cur_note_id else ''}%02
{note_name.replace(' ', '')}%02
{note_name}%02
{created_on if created_on else self._get_current_date()}%02
{note_form_id}%02
background%02
{note_name}%02
{"" if created_on else self._get_current_date()}%02
%02
{self.group_id}%02
{patient_id}%02
%02
%02
PRINT%02
{note_guid}%02
{note_category}%02
{applied_string}%02
PRINT
        """
        param_string = param_string.replace("\n", "").strip()
        query_json = {
            "sNameValues": param_string,
            "assessedDiagnosesData": "",
            "autoSaveCounter": "1",
            "hash": f"{int(time.time() * 1000)}{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}",
        }

        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        headers["Referer"] = self.url + (f"//WebForms/PD_DocOncoNoteDB.aspx?FID={selected_note["value"]}&__OS="
                                         f"{self.group_id}~{self.user_id}~{patient_id}&_SK=&__full=true")

        path = self.url + "/VisitNotes/AutoSaveVisitNote"
        response = await self._make_request(
            "POST", path, json=query_json, headers=headers
        )

        if self._verify_note_str(response):
            return {
                "success": True,
            }
        else:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                status_code=500,
                error_code="server_error",
                message=f"Failed to process note: {response}",
            )

    async def _forward_note(self, forward_to, note_name, patient_id, selected_note):
        forward_params = {
            'AJAX': '1',
            '__OS': f'{self.group_id}~{self.user_id}~{patient_id}',
            'M': 'sForwardRS',
            'P0': f'[{forward_to}%02%01{selected_note['value']}%01{note_name}%01%01{patient_id}%01{self.group_id}]',
            '_': f'{int(time.time() * 1000)}',
        }
        path = self.url + "/pages_pd/PD_DocForwardDB.aspx"
        forward_response = await self._make_request('GET', path, params=forward_params, headers=self.headers)
        fr_data = json.loads(forward_response)
        if fr_data.get('Success'):
            forward_status = True
        else:
            forward_status = False
        return forward_status

    async def generic_notes_fetch(self, note_name: str, patient_id: str):
        await self._verify_patient_exists(patient_id=patient_id)
        note_types = await self._fetch_available_note_types()

        selected_note = next(
            (
                item
                for item in note_types
                if self._fuzzy_compare(note_name, item["text"])
            ),
            None,
        )
        if selected_note is None:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                status_code=404,
                error_code="not_found",
                message=f"Note `{note_name}` not found",
            )

        cur_note_id = await self._fetch_latest_note_id(patient_id=patient_id, note_name=note_name)
        if "secure31" not in self.url:
            # allow direct note edits on secure31 only. other envs prefer creating new copies
            print(f"creating brand new note on {self.url}")
            cur_note_id = None

        note_page = await self._get_note_page(
            template_id=selected_note["value"], patient_id=patient_id, note_id=cur_note_id
        )
        note_soup = self._create_soup(note_page)
        existing_data = self._extract_form_data_bs(note_page)

        textfield_id_label_pairs = {}
        textfield_label_value_pairs = {}

        checkbox_pairs = {}
        radio_button_collection = {}

        for key, value in existing_data.items():
            if "fd_txt" in key.lower():
                label = self._get_label_for_textarea(textarea_id=key, soup=note_soup)
                if label is None:
                    continue
                if "invisible" in label.lower():
                    continue
                if "**" in label.lower():
                    continue
                if "grid" in key.lower():
                    continue

                new_key = key.replace('FD_txt', '')
                textfield_id_label_pairs[key] = new_key
                textfield_label_value_pairs[new_key] = value

            if "fd_chk" in key.lower():
                chk_box_label = self._get_label_for_input_button(inp_id=key, soup=note_soup)
                if chk_box_label is None:
                    continue

                new_key = key.replace('FD_chk', '')
                checkbox_pairs[new_key] = {
                    "label": chk_box_label,
                    "value": value == "true",
                }

            if "fd_rdo" in key.lower():
                rdo_group_name = self._get_radio_button_group_name(rdo_id=key, soup=note_soup)
                if rdo_group_name is None:
                    continue
                rdo_group_name = rdo_group_name.replace('FD_rdo', '')
                rdo_group_dict = radio_button_collection.get(rdo_group_name, {})

                rdo_btn_label = self._get_label_for_input_button(inp_id=key, soup=note_soup)
                if rdo_btn_label is None:
                    continue

                new_key = key.replace('FD_rdo', '')
                rdo_group_dict[new_key] = {
                    "label": rdo_btn_label,
                    "value": value == "true",
                }

                radio_button_collection[rdo_group_name] = rdo_group_dict

        # logic for checkboxes within tables
        tables_collection = {}
        grid_tables = note_soup.select('table[id*="Grid"]')
        fax_table = note_soup.select_one('table[id="tblFaxRecipients"]')
        if fax_table:
            grid_tables.append(fax_table)

        for grid_table in grid_tables:
            if grid_table is None:
                # completely not needed but left on purpose just in case
                # already had it trigger an error on one random note type
                continue

            table_data = self._parse_grid_table(table=grid_table)
            if len(table_data) == 0:
                continue

            table_id = grid_table.get('id')
            table_id = table_id.replace('tbl', '')

            tables_collection[table_id] = table_data

        # logic for pain scale selection
        pain_scale_collection = {}
        pain_scale_table = note_soup.select_one('table#tbl_gsGSPaiComparativePainScale')
        if pain_scale_table is not None:
            pain_scale_table_data = [row.text.strip() for row in pain_scale_table.select('tr')]
            for row in pain_scale_table_data:
                if '\n' in row:
                    _, v = row.split('\n')
                    pain_scale_collection[v] = False

        # logic for phq scale on secure30
        phq_scale_collection = {}
        phq_scale_table = note_soup.select_one('table#tbl_gsGSDepPHQ-9')
        if phq_scale_table is not None:
            phq_scale_table_data = [row.text.strip() for row in phq_scale_table.select('tr')]
            for row in phq_scale_table_data:
                if '\n' in row:
                    v = row.replace('\n', '~ ')
                    phq_scale_collection[v] = False

        note_category_elem = note_soup.select_one("input#txtCategory")
        note_category = note_category_elem.get("value")

        updated_note_name_elem = note_soup.select_one("span#spnPageTitle")
        updated_note_name = updated_note_name_elem.text.strip()

        result = {
            "patient_id": patient_id,
            "note_name": updated_note_name,
            "note_category": note_category,
            "textfield_data": {
                "text_id_label": textfield_id_label_pairs,
                "text_label_value": textfield_label_value_pairs
            },
            "radio_button_data": radio_button_collection,
            "checkbox_data": checkbox_pairs,
            "tables_data": tables_collection,
            "pain_scale_data": pain_scale_collection,
            "phq_scale_data": phq_scale_collection,
        }
        return result

    async def _fetch_latest_note_id(self, patient_id: str, note_name: str, get_newest: bool = True):
        endpoint = "/WebForms/pages_pd/PD_DocMDMain.aspx"
        path = self.url + endpoint
        params = {
            "PID": f"{patient_id}",
            "locationId": f"{self.location_id}",
            "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
            "_PP": 1,
            "_": str(int(time.time() * 1000)),
        }
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        soup = self._create_soup(response)

        unsigned_notes_tab = soup.select_one("div#pnlEditUnsigned")
        note_anchors = unsigned_notes_tab.select("a.PDMenu")

        """
        Logic: 
            - If provided 'note name' not within the 10 most recently opened, default to the first note.
            - If no opened notes exist for patient, return None to default to template using note name.  
        """

        latest_anchor = None
        for anchor in note_anchors:
            anchor_name = anchor.text.strip()
            anchor_name = anchor_name.split(" ", 1)[1]
            if self._fuzzy_compare(note_name, anchor_name):
                latest_anchor = anchor
                break

        if get_newest and latest_anchor is None and note_anchors:
            latest_anchor = note_anchors[0]

        if latest_anchor is None:
            return None

        onclick = latest_anchor.get("onclick")
        match = re.search(r'editDoc\("([^"]+)"\)', onclick)
        doc_id = match.group(1) if match else None
        print(f"Latest note ID for ({note_name}): {doc_id}")
        return doc_id

    @staticmethod
    def _parse_grid_table(table: bs4.Tag):
        """
        Parse table with checkboxes into structured data.

        Args:
            table (str): HTML grid table

        Returns:
            list: List of row dictionaries with checkbox and column data
        """
        # Get header row to map column positions
        header_row = table.select_one('tr th')
        headers = []
        if header_row:
            headers = [th.get_text(strip=True).lower() for th in table.select('tr th')]

        rows = []
        data_rows = table.select('tr[id]')  # Any row with an ID

        for row in data_rows:
            checkboxes = row.select('input[type="Checkbox"]')
            enabled_checkboxes = []

            for checkbox in checkboxes:
                if checkbox.get('disabled'):
                    continue
                else:
                    # Find which cell contains this checkbox
                    parent_cell = checkbox.find_parent('td')
                    cell_index = 0
                    if parent_cell:
                        all_cells = row.select('td')
                        cell_index = all_cells.index(parent_cell)

                    column_name = headers[cell_index] if cell_index < len(headers) else f"column_{cell_index}"

                    checkbox_data = {
                        'id': checkbox.get('id', '').replace('FD_chk', ''),
                        'value': checkbox.has_attr('checked'),
                        'column': column_name.replace(' ', '_').replace('-', '_')
                    }
                    enabled_checkboxes.append(checkbox_data)

            # Skip row if no enabled checkboxes
            if not enabled_checkboxes:
                continue

            row_data = {'checkboxes': enabled_checkboxes}

            # Try ID-based extraction first (more reliable)
            cells = row.select('td[id^="td_"]')
            if cells:
                for cell in cells:
                    cell_id = cell.get('id', '')
                    # Extract column name from ID pattern (td_..._ColumnName)
                    parts = cell_id.split('_')
                    if len(parts) >= 3:
                        column_name = parts[-1].lower()
                        row_data[column_name] = cell.get_text(strip=True)
            else:
                # Fallback to position-based extraction using headers
                all_cells = row.select('td')
                # Skip cells with checkboxes
                checkbox_cells = len([cell for cell in all_cells if cell.select('input[type="Checkbox"]')])
                for i, cell in enumerate(all_cells[checkbox_cells:], checkbox_cells):
                    header_idx = i - checkbox_cells
                    if header_idx < len(headers):
                        header = headers[header_idx].replace(' ', '_').replace('-', '_')
                        row_data[header] = cell.get_text(strip=True)

            rows.append(row_data)

        return rows

    @staticmethod
    def _prepare_toggle_input_dict(data: dict, prefix: str):
        updated = {}

        for key, value in data.items():
            updated[f"{prefix}{key}"] = "true" if value else "false"

        return updated

    @staticmethod
    def _get_radio_button_group_name(rdo_id: str, soup: BeautifulSoup):
        rdo_button = soup.find("input", {"id": rdo_id, "type": "radio"})
        if rdo_button:
            return rdo_button.get("name")

        return None

    @staticmethod
    def _get_label_for_input_button(inp_id: str, soup: BeautifulSoup):
        label_elem = soup.find("label", {"for": inp_id})
        if label_elem:
            return label_elem.text.strip()

        return None

    @staticmethod
    def _notes_textfields_merge_id_to_value(id_label: dict, label_value: dict):
        """
        Merges id_label and label_value dictionaries to create an id_value dictionary.

        Args:
            id_label: A dictionary mapping textarea IDs to their labels.
            label_value: A dictionary mapping labels to their values.

        Returns:
            A dictionary mapping textarea IDs directly to their values.
        """
        result = {}

        # For each textarea ID in id_label
        for textarea_id, label in id_label.items():
            # Look up the corresponding value using the label
            if label in label_value:
                result[textarea_id] = label_value[label]
            else:
                # Handle missing values gracefully
                result[textarea_id] = ""

        return result

    @staticmethod
    def _generic_notes_merge_new_with_existing(merged_input: dict, existing_data: dict):
        """
        Merges merged_input with existing_data, prioritizing values from merged_input
        when the same key exists in both dictionaries.

        Args:
            merged_input: Dictionary containing new values to prioritize.
            existing_data: Dictionary containing existing data.

        Returns:
            A dictionary with all keys from both dictionaries, with values from
            merged_input taking precedence over existing_data when keys overlap.
        """
        # Create a copy of existing_data to avoid modifying the original
        result = existing_data.copy()

        # Update with merged_input values, which will overwrite any duplicate keys
        result.update(merged_input)

        return result

    @staticmethod
    def _get_cleaned_text(element: Optional[bs4.Tag]) -> Optional[str]:
        """Gets stripped text from an element, cleans it, and handles None."""
        if not element:
            return None
        # Use separator=' ' to handle elements broken across lines better
        text = element.get_text(separator=" ", strip=True)
        # Remove common action links and extra whitespace more robustly
        noise_pattern = r"\s*(?:Clear All|Clear|Hide|Neg|NE|Edit|New ICD-10|New Problem/Diagnosis|Write Script|Outside Med|Med Reconcile|Not Documented|New Relative|New Clinical Observation|Create Provider|One-time Recipient)\b"
        text = re.split(noise_pattern, text, 1)[0]
        text = text.replace(
            "\xa0", " "
        ).strip()  # Replace non-breaking spaces and strip again
        if text.endswith(":"):
            text = text[:-1].strip()
        # Handle cases where only the asterisk might remain after cleaning
        if text == "*":
            return None
        return text if text else None  # Return None if cleaning results in empty string

    @staticmethod
    def _find_closest_question_table(start_element: bs4.Tag) -> Optional[bs4.Tag]:
        """Traverse up and find the preceding table likely containing the question name."""
        current = start_element
        # Limit upward traversal to avoid crossing major section boundaries if possible
        max_levels = 10  # Adjust as needed
        levels = 0
        while current and current.name != "body" and levels < max_levels:
            # Check previous siblings first at each level
            prev_sibling = current.previous_sibling
            while prev_sibling:
                if (
                        isinstance(prev_sibling, bs4.Tag)
                        and prev_sibling.name == "table"
                        and "margin-left" in prev_sibling.get("style", "")
                ):
                    # Check if it actually contains the question-name span structure
                    if prev_sibling.select_one("td.bold_text_bar > span.question-name"):
                        return prev_sibling
                # Check inside previous sibling if it's a container (less direct, might be needed)
                # if isinstance(prev_sibling, bs4.Tag):
                #      found_table = prev_sibling.find('table', style=lambda s: s and 'margin-left:10px' in s)
                #      if found_table and found_table.select_one('td.bold_text_bar > span.question-name'):
                #           return found_table
                prev_sibling = prev_sibling.previous_sibling

            # If not found in siblings, move up
            current = current.parent
            levels += 1
        return None

    @staticmethod
    def _get_label(textarea_id: str, soup: bs4.BeautifulSoup) -> Optional[str]:
        potential_div_containers = soup.select('div[id^="divOOH"]')

        # Find the parent div without using CSS selectors for the textarea
        parent_div = None
        for div in potential_div_containers:
            # Use find() instead of select_one() to avoid CSS selector issues
            if div.find("textarea", id=textarea_id) is not None:
                parent_div = div
                break

        if parent_div is None:
            print(f"No container found for textarea: {textarea_id}")
            return None

        # Find the question name element and check if it exists
        question_name_element = parent_div.find("span", class_="question-name")
        if question_name_element is None:
            # check for bold bar
            bold_bar_element = parent_div.find(class_="bold_text_bar")
            if bold_bar_element:
                question_name_element = bold_bar_element
            else:
                print(f"No question name or bold bar found for textarea: {textarea_id}")
                return None

        return question_name_element.get_text(strip=True)

    @staticmethod
    def _get_label_for_textarea(
            textarea_id: str, soup: bs4.BeautifulSoup
    ) -> Optional[str]:
        """
        Finds the label for a textarea, including its section header,
        *only if* it's determined to be editable.

        Args:
            textarea_id: The ID attribute of the textarea element (e.g., "FD_txtFieldName").
            soup: The BeautifulSoup object containing the parsed HTML.

        Returns:
            The combined "Header - Label" text, just the label, or just the header,
            or None if not editable or no label components found.
        """
        textarea = soup.find("textarea", id=textarea_id)
        if not textarea:
            return None

        field_name = None
        if textarea_id.startswith("FD_txt"):
            field_name = textarea_id.replace("FD_txt", "")
        elif textarea_id.startswith("FD_grd"):  # Explicitly ignore grids here
            return None  # Grids are not directly editable free text

        # --- Editability Check (based on user's successful logic) ---
        is_potentially_editable = False
        if field_name:
            # Must NOT have labelNoEdit
            if soup.find("div", id=f"labelNoEdit{field_name}"):
                return None  # Not editable if labelNoEdit exists

            # Must HAVE either an RTE mount or an Edit button linked
            has_editor = bool(soup.find("div", id=f"inlineEditorMount{field_name}"))
            # Check specifically for the pencil icon link associated with editing these fields
            has_edit_button = bool(
                soup.find(
                    "a",
                    id=lambda x: x
                                 and x.startswith("inlineEditButton")
                                 and field_name in x,
                )
            )
            # Looser check for edit button if ID doesn't match exactly
            if not has_edit_button:
                # Find parent td/container and check for *any* edit link within it
                container = textarea.find_parent("td") or textarea.find_parent(
                    "div", id=f"div{field_name}"
                )
                if container:
                    edit_link = container.find(
                        "a", class_="text_bar", onclick=lambda x: x and field_name in x
                    )
                    has_edit_button = bool(edit_link)

            is_potentially_editable = has_editor or has_edit_button

        if not is_potentially_editable:
            # print(f"DEBUG: Field {textarea_id} failed editability check (no RTE mount or relevant edit button).")
            return None
        # --- End Editability Check ---

        # --- Find Start Element for Searching ---
        start_element = textarea
        if field_name:
            rte_mount = soup.find("div", id=f"inlineEditorMount{field_name}")
            if rte_mount:
                start_element = rte_mount
            else:
                div_container = textarea.find_parent("div", id=f"div{field_name}")
                if div_container:
                    start_element = div_container
        # --- End Finding Start Element ---

        specific_label_tag: Optional[bs4.Tag] = None
        section_header_tag: Optional[bs4.Tag] = None

        # --- Find Specific Label (Patterns 1 & 2) ---
        q_table = OncoEmrIntegration._find_closest_question_table(start_element)
        if q_table:
            name_span = q_table.select_one("span.question-name")
            if name_span:
                specific_label_tag = name_span
        else:
            parent_td = start_element.find_parent("td")
            if parent_td:
                prev_td = parent_td.find_previous_sibling("td")
                if prev_td:
                    bold_bar = prev_td.find(class_="bold_text_bar")
                    if bold_bar:
                        specific_label_tag = bold_bar
                if not specific_label_tag:
                    parent_table = parent_td.find_parent("table")
                    if parent_table:
                        prev_table = parent_table.find_previous_sibling("table")
                        if prev_table:
                            bold_bar = prev_table.find("td", class_="bold_text_bar")
                            if bold_bar:
                                specific_label_tag = bold_bar
        # --- End Specific Label Search ---

        # --- Find Section Header (Pattern 4 Logic - simplified) ---
        container_div = start_element.find_parent("div", id=re.compile(r"^divOOH_"))
        if container_div:
            prev_tag = container_div.find_previous_sibling(
                True
            )  # Find previous TAG sibling
            if prev_tag and (
                    (
                            prev_tag.name == "span"
                            and "SectionDivider" in prev_tag.get("class", [])
                    )
                    or (
                            prev_tag.name == "h2"
                            and "container-name-header" in prev_tag.get("class", [])
                    )
            ):
                section_header_tag = prev_tag
        # --- End Section Header Search ---

        # --- Clean and Combine ---
        specific_label_text = OncoEmrIntegration._get_cleaned_text(specific_label_tag)
        section_header_text = OncoEmrIntegration._get_cleaned_text(section_header_tag)

        if specific_label_text and specific_label_text.lower().strip() == "this is invisible":
            if specific_label_tag.select_one('font').get('color') == '#ffffff':
                specific_label_text = None

        # Combine if both exist
        if section_header_text and specific_label_text:
            # Avoid duplication if header and label are accidentally the same
            if section_header_text.lower() == specific_label_text.lower():
                return section_header_text
            else:
                return f"{section_header_text} - {specific_label_text}"
        elif specific_label_text:
            return specific_label_text  # Return only specific label if no header found
        elif section_header_text:
            # Less common, but return header if only that was found near an editable field
            return section_header_text
        else:
            # Fallback if absolutely nothing is found (should be rare for editable)
            # print(f"Warning: No label components found for editable field: {textarea_id}")
            return field_name  # Return field name as last resort

    async def extract_all_text_fields(self, patient_id: str):
        note_types = await self._fetch_available_note_types()
        text_fields = []

        for note_type in note_types:
            note_page = await self._get_note_page(
                template_id=note_type["value"], patient_id=patient_id
            )
            text_fields.extend(self._extract_form_text_fields(note_page, note_type))

        # Write results to file
        with open("text_fields.txt", "w", encoding="utf-8") as f:
            for field in text_fields:
                if field["label"]:
                    f.write(f"{field['id']}\t{field['label']}\n")
                else:
                    f.write(f"{field['id']}\n")

        return text_fields

    @staticmethod
    def _extract_form_text_fields(note_page: str, note_type: dict) -> list[dict] | None:
        """
        Extracts all editable textarea fields and their labels from a note page.

        Args:
            note_page: HTML content of the note page
            note_type: Dictionary containing information about the note type

        Returns:
            List of dictionaries containing field ID, label, and note type,
            or None if no text fields found
        """
        soup = OncoEmrIntegration._create_soup(note_page)

        # Find all textarea elements with IDs starting with FD_txt
        all_textareas = soup.find_all(
            "textarea", id=lambda x: x and x.startswith("FD_txt")
        )

        if not all_textareas:
            return None

        text_fields = []
        seen_fields = set()

        for textarea in all_textareas:
            field_id = textarea.get("id")

            # Skip if already processed
            if field_id in seen_fields:
                continue

            # Get field name (without the FD_txt prefix)
            field_name = field_id.replace("FD_txt", "")

            # Check if this textarea is non-editable (look for labelNoEdit)
            no_edit_label = soup.find("div", id=f"labelNoEdit{field_name}")
            if no_edit_label:
                continue

            # Mark as seen
            seen_fields.add(field_id)

            # Find the label for this field
            label = None

            # Step 1: Look for the table with question-name span that's associated with this field
            # Find HTML comment with "begin question" and the field name
            current_element = textarea
            while current_element and not label:
                prev_sibling = current_element.previous_sibling
                while prev_sibling and not label:
                    if (
                            isinstance(prev_sibling, bs4.Comment)
                            and "begin question" in str(prev_sibling)
                            and field_name in str(prev_sibling)
                    ):
                        # Found the comment, now look for the table with question-name span
                        tables = soup.find_all(
                            "table", attrs={"style": "margin-left:10px"}
                        )
                        for table in tables:
                            # Check if this table is close to our comment
                            if table.previous_sibling and prev_sibling in str(
                                    table.previous_sibling
                            ):
                                name_span = table.select_one("span.question-name")
                                if name_span:
                                    label = name_span.get_text(strip=True)
                                    if label.endswith(":"):
                                        label = label[:-1]
                                break
                    prev_sibling = prev_sibling.previous_sibling
                if not label:
                    current_element = current_element.parent
                    if current_element and current_element.name == "body":
                        break

            # Step 2: If still no label, try finding the nearest table with question-name
            if not label:
                # Find the parent td or div that contains this textarea
                parent_container = textarea.parent
                while parent_container and parent_container.name not in [
                    "td",
                    "div",
                    "body",
                ]:
                    parent_container = parent_container.parent

                if parent_container and parent_container.name != "body":
                    # Look for the closest previous table
                    closest_table = parent_container.find_previous(
                        "table", attrs={"style": "margin-left:10px"}
                    )
                    if closest_table:
                        name_span = closest_table.select_one("span.question-name")
                        if name_span:
                            label = name_span.get_text(strip=True)
                            if label.endswith(":"):
                                label = label[:-1]

            # Step 3: If still no label, look for section headers
            if not label:
                parent_container = textarea.parent
                while parent_container and parent_container.name != "body":
                    # Check for container-name-header or SectionDivider
                    section_header = parent_container.find_previous(
                        "h2", class_="container-name-header"
                    )
                    if section_header:
                        label = section_header.get_text(strip=True)
                        break

                    section_divider = parent_container.find_previous(
                        "span", class_="SectionDivider"
                    )
                    if section_divider:
                        header_text = section_divider.get_text(strip=True)
                        # Remove 'Clear All' and 'Hide' text if present
                        if "Clear All" in header_text:
                            label = header_text.split("Clear All")[0].strip()
                        else:
                            label = header_text
                        break

                    parent_container = parent_container.parent

            # Clean up any font tags or other HTML in labels
            if label:
                # Remove any HTML tags from the label
                clean_label = ""
                for part in label.children:
                    if isinstance(part, bs4.NavigableString):
                        clean_label += str(part)
                if clean_label:
                    label = clean_label

            # Add this field to our results
            text_fields.append(
                {
                    "param": field_id,
                    "label": label
                             or field_name,  # Default to field name if no label found
                    "note": note_type["text"],
                }
            )

        return text_fields

    @staticmethod
    def _fuzzy_compare(str1, str2):
        """
        Perform a fuzzy comparison between two strings.
        - Converts both strings to lowercase
        - Removes all non-alphanumeric characters (keeps letters and digits)
        - Compares the resulting strings

        Args:
            str1 (str): First string to compare
            str2 (str): Second string to compare

        Returns:
            bool: True if strings match after processing, False otherwise
        """

        # Process both strings
        def process_string(s):
            if not isinstance(s, str):
                s = str(s)
            # Convert to lowercase and remove non-alphanumeric characters
            return re.sub(r"[^a-z0-9]", "", s.lower())

        processed_str1 = process_string(str1)
        processed_str2 = process_string(str2)

        # Return whether the processed strings match
        return processed_str1 == processed_str2

    async def _get_icd10_code_data(self, code: str):
        params = {"searchTerm": code, "includeRetired": "false", "diseaseId": ""}
        path = self.url + "/ICDSearch/Search"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )

        codes = response.get("Codes")
        this_data = next((item for item in codes if item.get("Code") == code), None)
        return this_data

    async def set_icd10_code(self, patient_id: str, code: str, add_type: str):
        await self._verify_patient_exists(patient_id=patient_id)

        code = code.upper()
        code_data = await self._get_icd10_code_data(code)
        if code_data is None:
            return {
                "code": code,
                "success": False,
                "message": f"ICD-10 code `{code}` not found.",
            }

        params = {
            "AJAX": "1",
            "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
            "M": "sSaveRS",
            "P0": f'[{code}{code_data.get("LongDescription")}{add_type}{self._get_current_date()}'
                  f"{patient_id}{code}]",
            "_": f"{time.time() * 1000}",
        }
        path = self.url + "/pages_pd/PD_DiagnosisOncologyICD10DB.aspx"
        response = await self._make_request(
            "GET", path, params=params, headers=self.headers
        )
        success = response.get("Success")
        return {
            "code": code,
            "success": success,
        }

    async def _patient_info(self, patient_id: str):
        path = self.url + "/Home/HeaderData"
        referrer = self.url + "/nav/treatment-plan?PID=" + patient_id
        headers = self.headers.copy()
        headers["Referer"] = referrer
        response = await self._make_request("GET", path, headers=headers)

        if response.get("PatientId") is None or response.get("PatientId") != patient_id:
            raise IntegrationAPIError(
                integration_name="oncoemr",
                status_code=404,
                message=f"No data found for patient `{patient_id}`",
            )

        return response

    async def _fetch_patient_orders_html(self, patient_id: str):
        path = self.url + f"/{self.group_id}/PatientOrders"
        referrer = self.url + "/nav/treatment-plan?PID=" + patient_id
        headers = self.headers.copy()
        headers["Referer"] = referrer

        response = await self._make_request("GET", path, headers=headers)
        return response

    async def _fetch_order_types(self):
        path = self.url + "/Orders/OrderTypes/"
        response = await self._make_request("GET", path, headers=self.headers)
        return response

    async def _fetch_order_sets(self):
        path = self.url + "/Orders/OrderSets/"
        response = await self._make_request("GET", path, headers=self.headers)
        return response

    async def make_order_entry(
            self, patient_id: str, order_name: str, order_type: str, order_date: str
    ):
        await self._verify_patient_exists(patient_id=patient_id)

        patient_data = await self._patient_info(patient_id)
        patient_provider_id = patient_data.get("PrimaryPhysicianId")

        all_physicians = await self._get_physicians()
        patient_provider = next(
            (
                item
                for item in all_physicians
                if item.get("UserId") == patient_provider_id
            ),
            None,
        )
        if patient_provider is None:
            raise IntegrationAPIError(
                integration_name="oncoemr",
                status_code=404,
                message=f"Failed to find physician for patient `{patient_id}`",
            )
        parsed_provider = {
            "id": f"{patient_provider_id}",
            "username": f"{patient_provider.get('UserName')}",
            "firstName": f'{patient_provider.get("FirstName")}',
            "lastName": f'{patient_provider.get("LastName")}',
            "displayName": f'{patient_provider.get("LastNameCommaFirstName")}',
            "userType": patient_provider.get("UserType"),
            "isEnabled": patient_provider.get("IsEnabled"),
            "isSuspended": patient_provider.get("IsSuspended"),
            "locationId": f'{patient_provider.get("LocationId")}',
            "npi": f'{patient_provider.get("Npi")}',
            "spi": patient_provider.get("Spi"),
            "UserName": f'{patient_provider.get("LastNameCommaFirstName")}',
            "UserId": f"{patient_provider_id}",
        }

        location = patient_data.get("SelectedUserLocation").get("LocationId")

        try:
            order_date = datetime.strptime(order_date, "%Y-%m-%d")
            order_date = order_date.strftime("%Y-%m-%d")
        except ValueError:
            raise IntegrationAPIError(
                integration_name="oncoemr",
                status_code=400,
                message=f"Invalid date format passed. Expected: [YYYY-MM-DD]. Received: `{order_date}`",
            )

        type_names = {
            "Activities": "Activity",
            "Tests": "Test",
            "Drugs": "Drug",
            "Radiology": "Radiology",
        }

        # logic for order sets
        if order_type == "OrderSets":
            order_sets_list = await self._fetch_order_sets()
            order_sets_list = order_sets_list.get("OrderSets")
            selected_set: dict = next(
                (item for item in order_sets_list if item.get("Name") == order_name),
                None,
            )

            if selected_set is None:
                raise IntegrationAPIError(
                    integration_name="oncoemr",
                    status_code=404,
                    message=f"Failed to find order set `{order_name}`",
                )

            set_orders = {
                type_names["Activities"]: selected_set.get("Activities"),
                type_names["Tests"]: selected_set.get("Tests"),
                type_names["Drugs"]: selected_set.get("Drugs"),
                type_names["Radiology"]: selected_set.get("Radiology"),
            }

            order_models = []
            for type_name, type_list in set_orders.items():
                for each in type_list:
                    cpt_code = next(
                        (
                            item.get("value")
                            for item in each.get("Details")
                            if item.get("title") == "CPT Code"
                        ),
                        None,
                    )
                    instr = next(
                        (
                            item.get("value")
                            for item in each.get("Details")
                            if item.get("title") == "Instructions"
                        ),
                        None,
                    )
                    finance = next(
                        (
                            item.get("value")
                            for item in each.get("Details")
                            if item.get("title") == "Financial"
                        ),
                        None,
                    )
                    dcc = next(
                        (
                            item.get("value")
                            for item in each.get("Details")
                            if item.get("title") == "Delivery CPT code"
                        ),
                        None,
                    )
                    dcq = next(
                        (
                            item.get("value")
                            for item in each.get("Details")
                            if item.get("title") == "Delivery CPT quantity"
                        ),
                        None,
                    )

                    t_locs = next(
                        (
                            item
                            for item in each.get("Details")
                            if item.get("title") == "Location"
                        ),
                        None,
                    )
                    if t_locs:
                        t_loc_options = [
                            option["value"] for option in t_locs["options"]
                        ]
                    else:
                        t_loc_options = None

                    spec_type = next(
                        (
                            item.get("value")
                            for item in each.get("Details")
                            if item.get("title") == "Specimen type"
                        ),
                        None,
                    )

                    model = {
                        "Billable": True if finance == "Billable" else False,
                        "CptCode": cpt_code,
                        "Dates": [f"{order_date}T12:00:00.000Z"],
                        "DefaultValues": None,
                        "DeliveryCptCode": dcc,
                        "DeliveryQuantity": dcq,
                        "FlowsheetId": None,
                        "Frequency": None,
                        "FrequencyOptions": None,
                        "ICDs": [],
                        "Id": f'{each.get("Id")}_{selected_set.get("Id")}',
                        "Instructions": f"{instr}<br />",
                        "IsNgsTest": each.get("IsNgsTest"),
                        "LocationId": f"{location}",
                        "Name": each.get("Id"),
                        "NgsTestRequest": None,
                        "NgsTestVendor": None,
                        "OrderSetName": f"{order_name}",
                        "OrderType": type_name,
                        "OrderingPhysician": parsed_provider,
                        "OrderingPhysicianId": f"{patient_provider_id}",
                        "PlannedDuration": None,
                        "ProtocolComponentId": None,
                        "ProviderIdList": [],
                        "ProviderList": [],
                        "Quantity": "1",
                        "RequisitionNumber": "",
                        "ShowProviders": True,
                        "TestId": None,
                        "TestLocation": (
                            t_locs.get("value") if t_locs is not None else None
                        ),
                        "TestLocationOptions": t_loc_options,
                        "Unit": (
                            spec_type.get("Value") if spec_type is not None else None
                        ),
                        "Value": None,
                    }
                    order_models.append(model)

            base_query = {
                "PatientId": patient_id,
                "OrderCreationRequests": order_models,
                "FlowsheetToBeCreated": order_name,
            }
            order_query = {
                "ordersCreationRequestModelJson": json.dumps(base_query),
            }

        else:
            order_types_list = await self._fetch_order_types()
            order_types = order_types_list.get("orders")
            selected_type_list = order_types.get(order_type)
            selected_type_data = next(
                (item for item in selected_type_list if item.get("Id") == order_name),
                None,
            )
            if selected_type_data is None:
                raise IntegrationAPIError(
                    integration_name="oncoemr",
                    status_code=404,
                    message=f"Failed to find order entry for `{order_name}`",
                )

            order_details = selected_type_data.get("Details")
            instructions_data = next(
                (item for item in order_details if item.get("title") == "Instructions")
            )
            instructions = instructions_data.get("value")

            order_model = {
                "PatientId": f"{patient_id}",
                "OrderCreationRequests": [
                    {
                        "Instructions": f"{instructions}<br />",
                        "OrderType": type_names.get(order_type),
                        "Id": f"{order_name}",
                        "LocationId": f"{location}",
                        "FlowsheetId": None,
                        "ICDs": [],
                        "Dates": [f"{order_date}T12:00:00.000Z"],
                        "Name": f"{order_name}",
                        "OrderingPhysicianId": f"{patient_provider_id}",
                        "OrderingPhysician": parsed_provider,
                        "PlannedDuration": "P0D",
                        "ProtocolComponentId": None,
                        "CptCode": None,
                        "Quantity": 0,
                        "StaffMemberUserId": None,
                        "Value": "",
                        "DefaultValues": None,
                        "AdditionalInfo": None,
                        "ImageId": None,
                        "ActivityLocation": None,
                        "ActivityLocationOptions": None,
                    }
                ],
            }
            order_query = {
                "ordersCreationRequestModelJson": json.dumps(order_model),
            }

        path = self.url + "/Orders/Orders/"
        referrer = self.url + "/nav/treatment-plan?PID=" + patient_id
        headers = self.headers.copy()
        headers["Referer"] = referrer

        response = await self._make_request(
            "POST", path, headers=headers, json=order_query
        )
        if response is None or len(response) == 0:
            return {
                "success": True,
            }

        return {
            "success": False,
        }

    async def search_patient_by_names(
            self, first_name: str = "", last_name: str = "", mrn: str = ""
    ) -> list[dict]:
        params = {
            "Length": "0",
        }
        data = {
            "oFindPatient.sResource": "-1",
            "oFindPatient.bTodayOnly": "False",
            "oFindPatient.sLastName": f"{last_name}",
            "oFindPatient.sFirstName": f"{first_name}",
            "oFindPatient.sPatientNumber": f"{mrn}",
            "oFindPatient.sDOB": "",
            "oFindPatient.sSSN": "",
            "oFindPatient.sPhone": "",
            "oFindPatient.sReferringMD": "",
            "oFindPatient.sGuarantor": "",
            "oFindPatient.sPolicy": "",
            "oFindPatient.sPhysician": "",
            "oFindPatient.sEmail": "",
            "X-Requested-With": "XMLHttpRequest",
        }
        path = self.url + "/FindPatient/GetPatientList"
        response = await self._make_request(
            "POST", path, params=params, data=data, headers=self.headers
        )
        view_html = response.get("sViewHtml")

        found_patients = self._parse_patient_search(view_html)

        if len(mrn) != 0:
            exact_patient = next(
                (patient for patient in found_patients if patient.get("mrn") == mrn),
                None,
            )
            # don't return full list if mrn is specified and not found
            if exact_patient is None:
                raise IntegrationAPIError(
                    integration_name=self.integration_name,
                    status_code=404,
                    error_code="not_found",
                    message=f"No patient found with MRN: `{mrn}`",
                )

            found_patients = [exact_patient]

        return found_patients

    @staticmethod
    def _parse_patient_search(html_content):
        """
        Parses HTML content containing a patient table (#tblPatientList)
        and extracts patient details.

        Args:
            html_content: A string containing the HTML source.

        Returns:
            A list of dictionaries, where each dictionary represents a patient
            with keys: 'name', 'dob', 'mrn', 'supervising_md', 'patient_id', 'anchor_mrn'.
            Returns an empty list if the table is not found or has no data.
        """
        soup = OncoEmrIntegration._create_soup(html_content)
        patient_list = []

        # Find the table by its ID
        table = soup.find("table", id="tblPatientList")
        if not table:
            print("Table with id 'tblPatientList' not found.")
            return patient_list

        # Find the table body
        tbody = table.find("tbody")
        if not tbody:
            print("Table body 'tbody' not found.")
            return patient_list

        # Find all table rows within the body
        rows = tbody.find_all("tr")

        # Regular expression to extract the patient ID from the onclick attribute
        onclick_pattern = re.compile(r'selectPatient\("([^"]+)"')

        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 4:  # Ensure we have the expected number of columns
                try:
                    # --- Name and IDs (from the first cell's <a> tag) ---
                    name_anchor = cells[0].find("a")
                    name = name_anchor.get_text(strip=True) if name_anchor else None
                    anchor_mrn = name_anchor.get("mrn") if name_anchor else None
                    patient_id = None
                    if name_anchor and name_anchor.get("onclick"):
                        match = onclick_pattern.search(name_anchor["onclick"])
                        if match:
                            patient_id = match.group(1)

                    # --- DOB (from the second cell) ---
                    dob_raw = cells[1].get_text(strip=True)
                    dob = dob_raw if dob_raw and dob_raw != " " else None

                    # --- MRN (from the third cell) ---
                    mrn_raw = cells[2].get_text(strip=True)
                    mrn = mrn_raw if mrn_raw and mrn_raw != " " else None

                    # --- Supervising MD (from the fourth cell) ---
                    md_raw = cells[3].get_text(strip=True)
                    supervising_md = (
                        md_raw if md_raw and md_raw != " " else None
                    )  # Handle empty MD field

                    patient_data = {
                        "name": name,
                        "dob": dob,
                        "mrn": mrn,
                        "supervising_md": supervising_md,
                        "patient_id": patient_id,  # Extracted from onclick
                        "anchor_mrn": anchor_mrn,  # Extracted from <a> tag's MRN attribute
                    }
                    patient_list.append(patient_data)
                except Exception as e:
                    print(f"Error processing row: {row}. Error: {e}")
            else:
                print(
                    f"Skipping row with unexpected number of cells ({len(cells)}): {row}"
                )

        return patient_list

    @staticmethod
    def _verify_note_str(data):
        # The pattern: "background" followed by \u0001, then "DH_" followed by alphanumeric characters,
        # then another \u0001, then another "DH_" pattern (same or different)
        pattern = r"^background\u0001(DH_[A-Z0-9]+)\u0001(DH_[A-Z0-9]+)$"

        match = re.match(pattern, data)
        return bool(match)

    @staticmethod
    def _apply_template_to_dict(
            template_model: FollowupNoteTemplateModel | ConsultationNoteTemplateModel,
            target_dict: Dict[str, str],
            radio_buttons_mapping: Dict,
            checkboxes_mapping: Dict,
            textfields_mapping: Dict,
    ) -> Dict[str, str]:
        """
        Apply the template model to the target dictionary, handling both text fields and radio buttons.

        Args:
            template_model: The FollowupNoteTemplateModel with user inputs
            target_dict: The dictionary with the actual field names to modify

        Returns:
            Updated dictionary with applied changes
        """
        result_dict = target_dict.copy()

        # Convert the model to a dict for easier processing
        model_dict = template_model.model_dump()

        # Process regular text fields
        for model_field, field_content in model_dict.items():
            # Skip patient_id and radio button fields
            if model_field == "patient_id" or model_field in radio_buttons_mapping:
                continue

            # Skip if no text content to add or not a field content object
            if not isinstance(field_content, dict) or not field_content.get("text"):
                continue

            # Get the corresponding field in the target dict
            if model_field in textfields_mapping:
                target_field = textfields_mapping[model_field]

                # Only proceed if the target field exists in the dictionary
                if target_field in result_dict:
                    if field_content.get("append", True) and result_dict[target_field]:
                        # Append to existing text with a newline
                        result_dict[target_field] = (
                            f"{result_dict[target_field]}\n{field_content['text']}"
                        )
                    else:
                        # Replace the existing text
                        result_dict[target_field] = field_content["text"]

        # Process radio button fields
        for field_name, mapping in radio_buttons_mapping.items():
            selected_value = model_dict.get(field_name)

            if selected_value:
                options_mapping = mapping["options"]

                # Skip if the selected value is not in the options
                if selected_value not in options_mapping:
                    continue

                # Set all options to false first
                for option, field_key in options_mapping.items():
                    if field_key in result_dict:
                        # Set all options to empty or false
                        result_dict[field_key] = ""

                # Then set the selected option to true
                if selected_value in options_mapping:
                    selected_key = options_mapping[selected_value]
                    if selected_key in result_dict:
                        # Set the selected option to true or some value indicating selection
                        result_dict[selected_key] = "true"

        # Process checkbox fields
        for field_name, field_key in checkboxes_mapping.items():
            checkbox_value = model_dict.get(field_name)

            if checkbox_value is not None and field_key in result_dict:
                if checkbox_value:
                    # If checkbox is checked, set to "true"
                    result_dict[field_key] = "true"
                else:
                    # If checkbox is not checked, explicitly set to "false"
                    result_dict[field_key] = "false"

        return result_dict

    @staticmethod
    def _remove_html_tags(text):
        """
        Sanitize HTML content to prevent XSS attacks while preserving rich text formatting

        Args:
            text: Raw HTML content

        Returns:
            Sanitized HTML content with rich text preserved
        """
        if not text:
            return ""

        # Convert line break elements to consistent format before parsing
        text = re.sub(r"<br\s*/?>", "<br>", text, flags=re.IGNORECASE)
        text = re.sub(r"</p>", "</p><br>", text, flags=re.IGNORECASE)
        text = re.sub(r"</div>", "</div><br>", text, flags=re.IGNORECASE)

        # Allow rich text tags
        allowed_tags = ['b', 'strong', 'i', 'em', 'u', 'a', 'br', 'p', 'div', 'span', 'ul', 'ol', 'li']
        allowed_attributes = {
            'a': ['href', 'title'],
            'div': ['style'],
            'span': ['style'],
            'ul': ['style'],
            'ol': ['style'],
            'li': ['style']
        }

        soup = BeautifulSoup(text, 'html.parser')

        # Remove disallowed tags
        for tag in soup.find_all():
            if tag.name not in allowed_tags:
                tag.unwrap()
            else:
                # Remove disallowed attributes
                allowed_attrs = allowed_attributes.get(tag.name, [])
                attrs_to_remove = [attr for attr in tag.attrs if attr not in allowed_attrs]
                for attr in attrs_to_remove:
                    del tag[attr]

        result = str(soup)

        # Clean up excess line breaks
        result = re.sub(r"<br>\s*<br>", "<br>", result)
        result = re.sub(r"(&nbsp;)+", " ", result, flags=re.IGNORECASE)

        return result.strip()

    @staticmethod
    def _extract_form_data_bs(full_html_string):
        """
        Extracts form data ONLY for elements with IDs starting with 'FD_',
        using BeautifulSoup for parsing the entire HTML page. Creates key-value pairs
        and formats the result.
        Args:
            full_html_string: The entire HTML content of the page as a string.
        Returns:
            A string formatted as key%01value%02key%01value... or an empty string if no data found.
        """
        soup = BeautifulSoup(full_html_string, "html.parser")
        form_data_dict = (
            {}
        )  # Use a dictionary to store data (handles potential ID clashes)
        # --- Find all relevant elements by ID pattern ---
        # This is more efficient than iterating through ALL tags
        fd_elements = soup.find_all(id=lambda x: x and x.startswith("FD_"))
        for element in fd_elements:
            element_id = element["id"]  # We know ID exists and starts with FD_
            tag_name = element.name.lower()
            # --- Textareas ---
            if tag_name == "textarea":
                # Get the raw content including HTML tags
                # Use .string, .text, or join the contents to preserve HTML
                raw_content = ""

                # Method 1: If the textarea has mixed content (text nodes and tags)
                for content in element.contents:
                    raw_content += f"{str(content)}"

                # Now clean up the HTML tags while preserving line breaks
                form_data_dict[element_id] = raw_content
            # --- Inputs (Text, Checkbox, Radio, Hidden) ---
            elif tag_name == "input":
                input_type = element.get("type", "").lower()
                if input_type == "text":
                    value = element.get("value", "")
                    # Important: Don't overwrite a checkbox/radio state if an input text has the same ID
                    # (though usually separate IDs like FD_chk... and FD_itb... are used)
                    if not (
                            element_id in form_data_dict
                            and form_data_dict[element_id] in ["true", "false"]
                    ):
                        form_data_dict[element_id] = value
                elif input_type in ["checkbox", "radio"]:
                    is_checked = element.has_attr("checked")
                    form_data_dict[element_id] = "true" if is_checked else "false"
                # Add other input types like 'hidden' if necessary
                # elif input_type == 'hidden':
                #     value = element.get('value', '')
                #     form_data_dict[element_id] = value
            # Add handling for other tag types like 'select' if needed
        # --- Format the output ---
        if not form_data_dict:
            return {}
            # Return empty string if nothing found
        return form_data_dict

    @staticmethod
    def _parse_patient_table(html_content: str) -> List[Dict]:
        """
        Parse HTML table of patient data using BeautifulSoup.

        Args:
            html_content: HTML string containing the table

        Returns:
            List of dictionaries where each dictionary represents a patient row
            with all values as strings
        """
        soup = OncoEmrIntegration._create_soup(html_content)

        # Find the patient visits table
        table = soup.find("table", id="tblPatientVisits")
        if not table:
            return []

        # Extract headers
        headers = []
        header_row = table.find("tr")
        if header_row:
            for th in header_row.find_all("th"):
                # Get text or id as fallback
                header_text = th.get_text().strip()
                if not header_text and th.get("id"):
                    header_text = th.get("id").replace("th", "")
                headers.append(header_text)

        # Process data rows
        patients = []
        for row in table.find_all("tr")[1:]:  # Skip header row
            patient_data = {}

            # Extract patient ID and name from row attributes
            pid = row.get("pid", "")
            p_name = row.get("pnam", "")
            location = row.get("location", "")

            patient_data["patient_id"] = pid
            patient_data["patient_name"] = p_name
            patient_data["location"] = location

            # Extract cell data
            cells = row.find_all("td")
            for i, cell in enumerate(cells):
                if i < len(headers):
                    # Clean the header name for use as a key
                    header_key = (
                        headers[i]
                        .replace(" ", "_")
                        .replace("(", "")
                        .replace(")", "")
                        .lower()
                    )

                    # Handle time and patient info specially
                    if i == 0:
                        # Time cell
                        time_link = cell.find("a", class_="gts")
                        if time_link:
                            patient_data["appointment_time"] = (
                                time_link.get_text().strip()
                            )
                        else:
                            patient_data["appointment_time"] = cell.get_text().strip()
                    elif "patient" in header_key or cell.find("a", id=lambda x: x and x.startswith("ancp")):
                        # Patient info cell - look for patient link and MRN
                        patient_link = cell.find("a", id=lambda x: x and x.startswith("ancp"))
                        if patient_link:
                            patient_data["patient_display"] = (
                                patient_link.get_text().strip()
                            )

                            # Extract MRN from span within patient link
                            mrn_span = patient_link.find("span")
                            if mrn_span:
                                patient_data["mrn"] = mrn_span.get_text().strip()
                    else:
                        # Get all text, preserving internal structure but as a string
                        patient_data[header_key] = cell.get_text().strip()

                        # Extract room status if available
                        if header_key == "room":
                            room_link = cell.find("a", class_="room-name")
                            if room_link:
                                patient_data["room_status"] = (
                                    room_link.get_text().strip()
                                )

            patients.append(patient_data)

        return patients

    @staticmethod
    def _get_current_date(pattern: str = "%m/%d/%Y"):
        """
        Get the current date formatted as 'MM/DD/YYYY' (e.g., '03/18/2025')

        Returns:
            str: Current date in 'MM/DD/YYYY' format with leading zeros
        """
        current_date = datetime.now()

        # Use strftime with format specifiers for leading zeros
        formatted_date = current_date.strftime(pattern)

        return formatted_date

    async def _fetch_patient_treatment_plan(self, patient_id: str):
        params = {
            "patientId": patient_id,
            "disableTpUiChanges": "false",
        }
        path = self.url + "/TreatmentPlan/ModelJson"
        response = await self._make_request(method="POST", url=path, params=params, headers=self.headers)
        return response
    
    async def _fetch_patient_orders_json(self, patient_id: str, order_id: str):
        payload = {
            "OrderIds": [order_id],
            "PatientIds": [patient_id],
            "includeHasSchedulerResource": False,
        }
        path = self.url + "/PatientOrders2"
        response = await self._make_request(method="POST", url=path, json=payload, headers=self.headers)
        return response

    async def _fetch_activity_order_dialog(self, patient_id: str, order_id: str):
        params = {
            'TID': '',
            'PCID': f'{order_id}',
            'DT': f'{self._get_current_date("%m-%d-%Y")}',
            'CID': f'{order_id}',
            'FRM': 'Treatment Plan',
            '__modal': 'true',
            '__OS': f'{self.group_id}~{self.user_id}~{patient_id}',
            '_SK': '',
            '__NL': '0',
        }
        path = self.url + "/WebForms/pages_pd/PD_TPActivityEditDB.aspx"
        response = await self._make_request(method="GET", url=path, params=params, headers=self.headers)
        return response

    async def set_new_cpt_code(self, patient_id: str, cpt_code: str):
        await self._verify_patient_exists(patient_id=patient_id)

        # go over the treatment plan and find the order info for the md visit
        treatment_plan = await self._fetch_patient_treatment_plan(patient_id=patient_id)
        general_flowsheet: dict = next(fs for fs in treatment_plan["flowsheets"] if fs["name"] == "General")

        try:
            today_index = treatment_plan["dates"].index(treatment_plan["today"])
            md_candidates = [
                comp for comp in general_flowsheet["components"]
                if comp["cells"][today_index] is not None
                and comp["cells"][today_index]["value"] != "*"
            ]
        except ValueError:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                message=f"No visit/activity found for patient ID today [{treatment_plan['today']}].",
                status_code=400,
                error_code="not_found"
            )

        # Find the component with matching doctor last name
        doctors = await self.fetch_physicians()
        md_component = None
        for component in md_candidates:
            cells = component["cells"]
            today_cell = cells[today_index]
            cell_value = today_cell.get("value", "")
            if "view" in cell_value.lower():
                # this is to ignore hidden events
                continue

            provider_name = cell_value.split("/")[0]
            if any(provider_name in doc["last_name"] for doc in doctors):
                print(today_cell)
                md_component = component
                break

        if md_component is None:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                message=f"No MD component found for patient ID today [{treatment_plan['today']}]."
                        f"\nCandidates: {md_candidates}",
                status_code=500,
                error_code="server_error"
            )

        order_id = md_component["protCompID"]
        order_data = await self._fetch_patient_orders_json(patient_id=patient_id, order_id=order_id)
        if len(order_data) == 0:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                message=f"No orders found for order id {order_id}. [{patient_id}]",
                status_code=500,
                error_code="server_error"
            )

        item_1 = order_data[0].get('Item1')
        modal_html = await self._fetch_activity_order_dialog(patient_id=patient_id, order_id=order_id)
        modal_soup = self._create_soup(modal_html)

        # validate new code
        code_select_elem = modal_soup.select_one("select#ddlChargeCodes")
        select_options_elems = code_select_elem.find_all("option")
        charge_codes = [option.get("value") for option in select_options_elems]

        if cpt_code not in charge_codes:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                message=f"Invalid CPT code: `{cpt_code}`",
                status_code=400,
                error_code="request_error"
            )

        location_name = modal_soup.select_one("span#lblLocation").text.strip()
        flowsheet_name = modal_soup.select_one("span#lblFlowsheet").text.strip()
        row_id = modal_soup.select_one("input#orderComponentId").get("value")
        physician_name = modal_soup.select_one("span#spanOrderingMD").text.strip()
        cpt_quantity = modal_soup.select_one("input[name='txtCPTQty']").get("value", "1")
        note_id = modal_soup.select_one("input#txtNoteID").get("value", "")
        cycle_day_info = modal_soup.select_one("input#txtCD").get("value", "")
        kit_qty = modal_soup.select_one("input#txtKitQty").get("value", "0")
        supply_kit = modal_soup.select_one("input#txtSupplyKit").get("value", "")

        date_in = self._get_current_date("%m/%d/%Y")

        # build request to save new cptCode
        p0_body = [
            {
                'action': 'save',
                'patientId': f'{patient_id}',
                'rowId': f'{row_id}',
                'originalOrderSetName': f'{flowsheet_name}',
                'originalLocationName': f'{location_name}',
                'activityName': f'{item_1.get("OrderName")}',
                'icd': f'{item_1.get("IcdTenCodesCommaDelimited")}',
                'newDate': f'{date_in} 12:00 AM',
                'selectedMD': f'{physician_name}',
                'selectedMDID': f'{item_1.get("OrderingClinicianUserId")}',
                'value': f'{item_1.get("OrderingClinicianUserId")}',
                'changeFor': 'DateOnly',
                'priority': f'{item_1.get("Priority")}',
                'frequency': '1',
                'instructions': f'{item_1.get("Instructions")}',
                'orderSetId': '-1',
                'orderSetName': f'{flowsheet_name}',
                'cptCode': f'{cpt_code}',
                'cptQuantity': f'{cpt_quantity}',
                'supplyKit': f'{supply_kit}',
                'kitQuantity': f'{kit_qty}',
                'locationId': f'{item_1.get("LocationId")}',
                'locationName': f'{location_name}',
                'duration': f'{item_1.get("PlannedDurationMinutes")}',
                'sequence': f'{item_1.get("Sequence")}',
                'cycleDayInfo': f'{cycle_day_info}',
                'noteId': f'{note_id}',
                'dataName': '',
                'signoffParam': '',
                'changeReason': '',
                'comment': '',
                'mdpList': '',
                'isExtender': 'false',
                'orderingMDUID': f'{item_1.get("OrderingClinicianUserId")}',
                'newOrderingMDUID': f'{item_1.get("OrderingClinicianUserId")}',
                'referral': '',
                'requiresAuth': 'False',
                'isActivityLocationInHouse': False,
                'isActivityLocationOutside': False,
                'activityLocation': ''
            }
        ]
        payload = {
            "AJAX": 1,
            "__OS": f'{self.group_id}~{self.user_id}~{patient_id}',
            "P0": json.dumps(p0_body),
        }
        params = {
            'M': 'sSaveRecordRS',
        }
        path = self.url + "/pages_pd/PD_TPActivityEditDB.aspx"

        response = await self._make_request(method="POST", url=path, params=params, data=payload, headers=self.headers)
        return response

    @staticmethod
    def _create_soup(html_content) -> BeautifulSoup:
        return BeautifulSoup(html_content, "html.parser")
