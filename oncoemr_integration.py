import asyncio
import re
import html
import json
import time
import random
import string
from datetime import datetime
from typing import List, Dict

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from submodule_integrations.models.integration import Integration
from submodule_integrations.oncoemr.oncoemr_models import FollowupNoteTemplateModel
from submodule_integrations.utils.errors import IntegrationAuthError, IntegrationAPIError
from submodule_integrations.oncoemr.consultation_models import ConsultationNoteTemplateModel
from submodule_integrations.oncoemr.consultation_mappings import CONSULTATION_TEXTFIELDS_MAPPING, \
    CONSULTATION_RADIO_BUTTONS_MAPPING, CONSULTATION_CHECKBOXES_MAPPING
from submodule_integrations.oncoemr.oncoemr_mapping import FOLLOWUP_TEXTFIELDS_MAPPING, FOLLOWUP_RADIO_BUTTONS_MAPPING, \
    FOLLOWUP_CHECKBOXES_MAPPING


class OncoEmrIntegration(Integration):
    def __init__(self, domain: str, token: str, location_id: str, network_requester=None,
                 user_agent: str = UserAgent().random):
        super().__init__("oncoemr")
        self.user_agent = user_agent
        self.url = domain if "https://" in domain else f"https://{domain}"
        self.network_requester = network_requester

        self.headers = {
            "Host": domain.replace('https://', ''),
            "User-Agent": self.user_agent,
            "Cookie": token,
            "Accept": "*/*",
            "Accept-Encoding": "gzip",
        }

        self.user_id = None
        self.group_id = None
        self.location_id = location_id

    @classmethod
    async def create(cls, domain: str, token: str, location_id: str, network_requester=None,
                     user_agent: str = UserAgent().random):
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

    async def _make_request(self, method: str, url: str, **kwargs) -> dict | str | bytes:
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
        patient_basic_info = await self._patient_partial_page_info(patient_id=patient_id)
        header_data = patient_basic_info.get('HeaderData')
        if header_data.get('PatientMrn') or header_data.get('PatientDisplayName'):
            return

        patient_status = await self._patient_status_info(patient_id=patient_id)
        if patient_status.get('id'):
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
                "username": physician["UserName"]
            }

            processed.append(data)

        return processed

    async def fetch_visit_list(self, doctor_id: str, selected_date: str | None):
        doctors_list = await self.fetch_physicians()
        this_doctor = next((doctor for doctor in doctors_list if doctor.get("id") == doctor_id), None)
        if this_doctor is None:
            raise IntegrationAPIError(
                integration_name=self.integration_name,
                error_code="not_found",
                status_code=404,
                message=f"Doctor not found for ID: `{doctor_id}",
            )

        path = f"{self.url}/VisitList/UpdateVisitList"

        if selected_date is None:
            selected_date = self._get_current_date()

        first_param = {
            'sVisitDate': f'{selected_date}',
            'sLocID': -1,
            'sResource': f'{doctor_id}',
            'bNewLocation': False,
            'bNewResource': True,
            'sMDUID': f'{doctor_id}',
            'bShowPatLocCol': 'True',
            'bMDVisitsOnly': 'True',
            'bHideUnscheduled': 'True',
            'olHideFilters': ['chkHideUnscheduled', 'chkVisitsOnly'],
            'bShowVisitsOnly': True
        }

        params = {
            "sVisitListRequest": json.dumps(first_param),
            "_": str(int(time.time() * 1000))  # Current timestamp in milliseconds
        }

        response = await self._make_request("GET", url=path, params=params, headers=self.headers)
        if isinstance(response, dict):
            visit_html = response.get('sViewHtml')
        else:
            visit_html = response

        parsed_visit_list = self._parse_patient_table(visit_html)
        return parsed_visit_list

    async def _basic_patient_demographics_data(self, patient_id: str) -> dict:
        path = self.url + "/pc/demographics"
        params = {
            'patientId': f'{patient_id}',
            'includeDeletedOrMerged': 'false',
        }
        response = await self._make_request("GET", url=path, params=params, headers=self.headers)
        return response

    async def _patient_status_info(self, patient_id: str) -> dict:
        path = self.url + "/PatientPortal/Status"
        params = {
            'patientId': f'{patient_id}',
        }
        response = await self._make_request("GET", url=path, params=params, headers=self.headers)
        return response

    async def _patient_partial_page_info(self, patient_id: str) -> dict:
        path = self.url + "/PartialPage/GetPageInfoForPatient"
        first_param = {
            'sPID': f'{patient_id}',
            'sUID': f'{self.user_id}',
            'sGID': f'{self.group_id}',
            'bNewPatient': True,
            'bCheckAccess': True,
            'sRequestedPage': '$default$',
            'sSessionKey': '',
            'oAttr': {
                'bIsPatientPage': True,
                'bReloadOnNewPatient': False,
                'sHelpFileName': '',
                'sTitle': '',
                'sLocName': '',
                'bShowFind': True,
                'bHidePatient': False,
                'sController': '',
                'sAction': '',
                'sOnload': 'PD_VISITLIST.localStartup'
            }
        }
        params = {
            "sPageInfo": json.dumps(first_param),
            "_": str(int(time.time() * 1000))
        }
        response = await self._make_request("GET", url=path, params=params, headers=self.headers)
        return response

    async def _patient_demographics_html(self, patient_id: str) -> str:
        params = {
            'PID': f'{patient_id}',
            'locationId': f'{self.location_id}',
            '_PP': '1',
            '_': str(int(time.time() * 1000)),
        }
        path = self.url + "/WebForms/pages_pd/PD_Demographics.aspx"
        response = await self._make_request("GET", url=path, params=params, headers=self.headers)
        return response

    async def fetch_patient_demographics(self, patient_id: str):
        await self._verify_patient_exists(patient_id=patient_id)

        demographics = await self._basic_patient_demographics_data(patient_id)
        status_info = await self._patient_status_info(patient_id)

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
        advance_directive = advance_directive_elem.text.strip() if advance_directive_elem else None
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
            "dob": demographics.get('dateOfBirth'),
            "gender": demographics.get('gender'),
            "first_name": demographics.get('firstName'),
            "last_name": demographics.get('lastName'),
            "middle_name": demographics.get('middleName'),
            "preferred_name": demographics.get('preferredName'),
            "pronouns": demographics.get('pronouns'),
            "has_medicare": demographics.get('hasMedicare'),
            "birth_info": demographics.get('birthDetails'),
            "deceased_date": demographics.get('deceasedDate'),
            "preferred_language": demographics.get('preferredLanguageCode'),
            "ethnicity": demographics.get('ethnicityCodes'),
            "mothers_maiden_name": demographics.get('mothersMaidenName'),
            "record_number": demographics.get('mrn'),
            "ssn": demographics.get('ssn'),
            "affiliated_tribe": demographics.get('tribalAffiliation'),
            # "is_tribe_member": demographics.get(''),
            "marital_status": demographics.get('maritalStatusCode'),
            "employer": employer,
            "occupation": occupation,
            # "occupation_date": demographics.get(''),
            "industry": industry,
            "preferred_clinic": pref_clinic,
            "status": status,
            "advance_directive": advance_directive,
            "is_test_patient": demographics.get('isTestPatient'),
            "benefit_status": benefit,
            # "due": due_value,
            # "balance": balance_value,
            # "copay": copay_value,
            "last_login": status_info.get('lastLogin'),
            "user_id": status_info.get('userId'),
            "email": status_info.get('email'),
        }

        return data

    async def _patient_allergies_data(self, patient_id: str) -> list[dict]:
        params = {
            "patientId": patient_id,
        }
        path = self.url + "/pc/allergies"
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        return response

    async def _patient_oncology_data(self, patient_id: str) -> list[dict]:
        params = {
            "patientId": patient_id,
            "showHccStatus": False,
        }
        path = self.url + "/pc/oncology-diagnoses"
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        return response

    async def _get_all_notes(self, patient_id: str) -> list[dict]:
        params = {
            "PID": patient_id,
            "locationId": f"{self.location_id}",
            "_PP": 1,
            "_": str(int(time.time() * 1000)),
        }
        path = self.url + "/WebForms/pages_pd/PD_DocMDMain.aspx"
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        soup = self._create_soup(response)
        note_elems = soup.select("a.PDMenu")
        notes_list = []

        pattern = r'window\.openDocumentViewer\("([^"]+)",\s*"([^"]+)"'
        for note_elem in note_elems:
            name = note_elem.text.strip()
            onclick = note_elem.get('onclick')

            match = re.search(pattern, onclick)

            if match:
                note_id = match.group(2)
            else:
                note_id = None

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
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        records = response.get("documentRecords")
        note_data = next((item for item in records if item.get('id') == note_id), None)
        return note_data

    async def _get_note_pdf_file(self, patient_id: str, note_id: str) -> dict[str, str | bytes]:
        note_data = await self._get_note_data(patient_id, note_id)
        note_path = note_data.get('presignedUrl')

        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Referer": f"{self.url}/",
        # }
        # response = await self._make_request("GET", note_path, headers=headers)
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
            if note.get('note_id'):
                data = await self._get_note_pdf_file(
                    patient_id=patient_id,
                    note_id=note.get('note_id'),
                )
            else:
                data['status'] = 'No Note ID'

            data["name"] = note.get('name')
            note_files.append(data)

        return note_files

    async def _followup_note_page(self, patient_id: str):
        path = self.url + "//WebForms/PD_DocOncoNoteDB.aspx"
        params = {
            "FID": "DO_06APW5AY04PK7CHWD1EP",
            "__OS": f"{self.group_id}~{self.user_id}~{patient_id}",
            "_SK": "",
            "__full": "true"
        }
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        return response

    async def make_followup_note(self, template: FollowupNoteTemplateModel):
        patient_id = template.patient_id
        await self._verify_patient_exists(patient_id=patient_id)

        note_page = await self._followup_note_page(patient_id=patient_id)

        note_soup = self._create_soup(note_page)
        note_guid_elem = note_soup.select_one('input#txtNoteGUID')
        note_guid = note_guid_elem.get('value')

        note_form_id_elem = note_soup.select_one('input#txtFormID')
        note_form_id = note_form_id_elem.get('value')

        existing_data = self._extract_form_data_bs(note_page)

        filled_template = self._apply_template_to_dict(
            template_model=template,
            target_dict=existing_data,
            checkboxes_mapping=FOLLOWUP_CHECKBOXES_MAPPING,
            radio_buttons_mapping=FOLLOWUP_RADIO_BUTTONS_MAPPING,
            textfields_mapping=FOLLOWUP_TEXTFIELDS_MAPPING
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
        param_string = param_string.replace("\n", '').strip()

        query_json = {
            'sNameValues': param_string,
            'assessedDiagnosesData': '',
            'autoSaveCounter': '2',
            'hash': f'{int(time.time() * 1000)}{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}',
        }
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        path = self.url + "/VisitNotes/AutoSaveVisitNote"
        response = await self._make_request("POST", path, json=query_json, headers=headers)

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
            "__full": "true"
        }
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        return response

    async def make_consultation_note(self, template: ConsultationNoteTemplateModel):
        patient_id = template.patient_id
        await self._verify_patient_exists(patient_id=patient_id)

        note_page = await self._initial_consultation_note_page(patient_id=patient_id)

        note_soup = self._create_soup(note_page)
        note_guid_elem = note_soup.select_one('input#txtNoteGUID')
        note_guid = note_guid_elem.get('value')

        note_form_id_elem = note_soup.select_one('input#txtFormID')
        note_form_id = note_form_id_elem.get('value')

        existing_data = self._extract_form_data_bs(note_page)
        filled_template = self._apply_template_to_dict(
            template_model=template,
            target_dict=existing_data,
            checkboxes_mapping=CONSULTATION_CHECKBOXES_MAPPING,
            radio_buttons_mapping=CONSULTATION_RADIO_BUTTONS_MAPPING,
            textfields_mapping=CONSULTATION_TEXTFIELDS_MAPPING
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
        param_string = param_string.replace("\n", '').strip()
        query_json = {
            'sNameValues': param_string,
            'assessedDiagnosesData': '',
            'autoSaveCounter': '1',
            'hash': f'{int(time.time() * 1000)}{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}',
        }

        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        path = self.url + "/VisitNotes/AutoSaveVisitNote"
        response = await self._make_request("POST", path, json=query_json, headers=headers)

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

    async def _get_icd10_code_data(self, code: str):
        params = {
            'searchTerm': code,
            'includeRetired': "false",
            'diseaseId': ''
        }
        path = self.url + "/ICDSearch/Search"
        response = await self._make_request("GET", path, params=params, headers=self.headers)

        codes = response.get("Codes")
        this_data = next((item for item in codes if item.get('Code') == code), None)
        return this_data

    async def set_icd10_code(self, patient_id: str, code: str, add_type: str):
        await self._verify_patient_exists(patient_id=patient_id)

        code = code.upper()
        code_data = await self._get_icd10_code_data(code)
        if code_data is None:
            return {
                'code': code,
                'success': False,
                'message': f"ICD-10 code `{code}` not found."
            }

        params = {
            'AJAX': '1',
            '__OS': f'{self.group_id}~{self.user_id}~{patient_id}',
            'M': 'sSaveRS',
            'P0': f'[{code}{code_data.get("LongDescription")}{add_type}{self._get_current_date()}'
                  f'{patient_id}{code}]',
            '_': f'{time.time() * 1000}',
        }
        path = self.url + "/pages_pd/PD_DiagnosisOncologyICD10DB.aspx"
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        success = response.get("Success")
        return {
            'code': code,
            'success': success,
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
                message=f"No data found for patient `{patient_id}`"
            )

        return response

    async def _fetch_patient_orders(self, patient_id: str):
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

    async def make_order_entry(self, patient_id: str, order_name: str, order_type: str, order_date: str):
        await self._verify_patient_exists(patient_id=patient_id)

        patient_data = await self._patient_info(patient_id)
        patient_provider_id = patient_data.get("PrimaryPhysicianId")

        all_physicians = await self._get_physicians()
        patient_provider = next((item for item in all_physicians if item.get('UserId') == patient_provider_id), None)
        if patient_provider is None:
            raise IntegrationAPIError(
                integration_name="oncoemr",
                status_code=404,
                message=f"Failed to find physician for patient `{patient_id}`"
            )
        parsed_provider = {
            'id': f'{patient_provider_id}',
            'username': f'{patient_provider.get('UserName')}',
            'firstName': f'{patient_provider.get("FirstName")}',
            'lastName': f'{patient_provider.get("LastName")}',
            'displayName': f'{patient_provider.get("LastNameCommaFirstName")}',
            'userType': patient_provider.get('UserType'),
            'isEnabled': patient_provider.get('IsEnabled'),
            'isSuspended': patient_provider.get('IsSuspended'),
            'locationId': f'{patient_provider.get("LocationId")}',
            'npi': f'{patient_provider.get("Npi")}',
            'spi': patient_provider.get('Spi'),
            'UserName': f'{patient_provider.get("LastNameCommaFirstName")}',
            'UserId': f'{patient_provider_id}'
        }

        location = patient_data.get("SelectedUserLocation").get('LocationId')

        try:
            order_date = datetime.strptime(order_date, "%Y-%m-%d")
            order_date = order_date.strftime("%Y-%m-%d")
        except ValueError:
            raise IntegrationAPIError(
                integration_name="oncoemr",
                status_code=400,
                message=f"Invalid date format passed. Expected: [YYYY-MM-DD]. Received: `{order_date}`"
            )

        type_names = {
            "Activities": "Activity",
            "Tests": "Test",
            "Drugs": "Drug",
            "Radiology": "Radiology"
        }

        # logic for order sets
        if order_type == "OrderSets":
            order_sets_list = await self._fetch_order_sets()
            order_sets_list = order_sets_list.get('OrderSets')
            selected_set: dict = next((item for item in order_sets_list if item.get('Name') == order_name), None)

            if selected_set is None:
                raise IntegrationAPIError(
                    integration_name="oncoemr",
                    status_code=404,
                    message=f"Failed to find order set `{order_name}`"
                )

            set_orders = {
                type_names['Activities']: selected_set.get('Activities'),
                type_names['Tests']: selected_set.get('Tests'),
                type_names['Drugs']: selected_set.get('Drugs'),
                type_names['Radiology']: selected_set.get('Radiology')
            }

            order_models = []
            for type_name, type_list in set_orders.items():
                for each in type_list:
                    cpt_code = next(
                        (item.get('value') for item in each.get('Details') if item.get('title') == 'CPT Code'), None
                    )
                    instr = next(
                        (item.get('value') for item in each.get('Details') if item.get('title') == 'Instructions'), None
                    )
                    finance = next(
                        (item.get('value') for item in each.get('Details') if item.get('title') == 'Financial'), None
                    )
                    dcc = next(
                        (item.get('value') for item in each.get('Details') if item.get('title') == 'Delivery CPT code'),
                        None
                    )
                    dcq = next(
                        (item.get('value') for item in each.get('Details') if
                         item.get('title') == 'Delivery CPT quantity'),
                        None
                    )

                    t_locs = next(
                        (item for item in each.get('Details') if item.get('title') == 'Location'), None
                    )
                    if t_locs:
                        t_loc_options = [option['value'] for option in t_locs['options']]
                    else:
                        t_loc_options = None

                    spec_type = next(
                        (item.get('value') for item in each.get('Details') if item.get('title') == 'Specimen type'),
                        None
                    )

                    model = {
                        'Billable': True if finance == "Billable" else False,
                        'CptCode': cpt_code,
                        'Dates': [f'{order_date}T12:00:00.000Z'],
                        'DefaultValues': None,
                        'DeliveryCptCode': dcc,
                        'DeliveryQuantity': dcq,
                        'FlowsheetId': None,
                        'Frequency': None,
                        'FrequencyOptions': None,
                        'ICDs': [],
                        'Id': f'{each.get("Id")}_{selected_set.get("Id")}',
                        'Instructions': f'{instr}<br />',
                        'IsNgsTest': each.get('IsNgsTest'),
                        'LocationId': f'{location}',
                        'Name': each.get('Id'),
                        'NgsTestRequest': None,
                        'NgsTestVendor': None,
                        'OrderSetName': f'{order_name}',
                        'OrderType': type_name,
                        'OrderingPhysician': parsed_provider,
                        'OrderingPhysicianId': f'{patient_provider_id}',
                        'PlannedDuration': None,
                        'ProtocolComponentId': None,
                        'ProviderIdList': [],
                        'ProviderList': [],
                        'Quantity': '1',
                        'RequisitionNumber': '',
                        'ShowProviders': True,
                        'TestId': None,
                        'TestLocation': t_locs.get('value') if t_locs is not None else None,
                        'TestLocationOptions': t_loc_options,
                        'Unit': spec_type.get('Value') if spec_type is not None else None,
                        'Value': None
                    }
                    order_models.append(model)

            base_query = {
                "PatientId": patient_id,
                "OrderCreationRequests": order_models,
                "FlowsheetToBeCreated": order_name
            }
            order_query = {
                "ordersCreationRequestModelJson": json.dumps(base_query),
            }

        else:
            order_types_list = await self._fetch_order_types()
            order_types = order_types_list.get('orders')
            selected_type_list = order_types.get(order_type)
            selected_type_data = next((item for item in selected_type_list if item.get('Id') == order_name), None)
            if selected_type_data is None:
                raise IntegrationAPIError(
                    integration_name="oncoemr",
                    status_code=404,
                    message=f"Failed to find order entry for `{order_name}`"
                )

            order_details = selected_type_data.get("Details")
            instructions_data = next((item for item in order_details if item.get('title') == "Instructions"))
            instructions = instructions_data.get('value')

            order_model = {
                'PatientId': f'{patient_id}',
                'OrderCreationRequests': [
                    {
                        'Instructions': f'{instructions}<br />',
                        'OrderType': type_names.get(order_type),
                        'Id': f'{order_name}',
                        'LocationId': f'{location}',
                        'FlowsheetId': None,
                        'ICDs': [],
                        'Dates': [f'{order_date}T12:00:00.000Z'],
                        'Name': f'{order_name}',
                        'OrderingPhysicianId': f'{patient_provider_id}',
                        'OrderingPhysician': parsed_provider,
                        'PlannedDuration': 'P0D',
                        'ProtocolComponentId': None,
                        'CptCode': None,
                        'Quantity': 0,
                        'StaffMemberUserId': None,
                        'Value': '',
                        'DefaultValues': None,
                        'AdditionalInfo': None,
                        'ImageId': None,
                        'ActivityLocation': None,
                        'ActivityLocationOptions': None
                    }
                ]
            }
            order_query = {
                "ordersCreationRequestModelJson": json.dumps(order_model),
            }

        path = self.url + "/Orders/Orders/"
        referrer = self.url + "/nav/treatment-plan?PID=" + patient_id
        headers = self.headers.copy()
        headers["Referer"] = referrer

        response = await self._make_request("POST", path, headers=headers, json=order_query)
        if response is None or len(response) == 0:
            return {
                "success": True,
            }

        return {
            "success": False,
        }

    async def search_patient_by_names(self, first_name: str = "", last_name: str = "", mrn: str = "") -> list[dict]:
        params = {
            'Length': '0',
        }
        data = {
            'oFindPatient.sResource': '-1',
            'oFindPatient.bTodayOnly': 'False',
            'oFindPatient.sLastName': f'{last_name}',
            'oFindPatient.sFirstName': f'{first_name}',
            'oFindPatient.sPatientNumber': f'{mrn}',
            'oFindPatient.sDOB': '',
            'oFindPatient.sSSN': '',
            'oFindPatient.sPhone': '',
            'oFindPatient.sReferringMD': '',
            'oFindPatient.sGuarantor': '',
            'oFindPatient.sPolicy': '',
            'oFindPatient.sPhysician': '',
            'oFindPatient.sEmail': '',
            'X-Requested-With': 'XMLHttpRequest',
        }
        path = self.url + "/FindPatient/GetPatientList"
        response = await self._make_request("POST", path, params=params, data=data, headers=self.headers)
        view_html = response.get("sViewHtml")

        found_patients = self._parse_patient_search(view_html)

        if len(mrn) != 0:
            exact_patient = next((patient for patient in found_patients if patient.get('mrn') == mrn), None)
            # don't return full list if mrn is specified and not found
            if exact_patient is None:
                raise IntegrationAPIError(
                    integration_name=self.integration_name,
                    status_code=404,
                    error_code='not_found',
                    message=f"No patient found with MRN: `{mrn}`"
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
        table = soup.find('table', id='tblPatientList')
        if not table:
            print("Table with id 'tblPatientList' not found.")
            return patient_list

        # Find the table body
        tbody = table.find('tbody')
        if not tbody:
            print("Table body 'tbody' not found.")
            return patient_list

        # Find all table rows within the body
        rows = tbody.find_all('tr')

        # Regular expression to extract the patient ID from the onclick attribute
        onclick_pattern = re.compile(r'selectPatient\("([^"]+)"')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 4:  # Ensure we have the expected number of columns
                try:
                    # --- Name and IDs (from the first cell's <a> tag) ---
                    name_anchor = cells[0].find('a')
                    name = name_anchor.get_text(strip=True) if name_anchor else None
                    anchor_mrn = name_anchor.get('mrn') if name_anchor else None
                    patient_id = None
                    if name_anchor and name_anchor.get('onclick'):
                        match = onclick_pattern.search(name_anchor['onclick'])
                        if match:
                            patient_id = match.group(1)

                    # --- DOB (from the second cell) ---
                    dob_raw = cells[1].get_text(strip=True)
                    dob = dob_raw if dob_raw and dob_raw != ' ' else None

                    # --- MRN (from the third cell) ---
                    mrn_raw = cells[2].get_text(strip=True)
                    mrn = mrn_raw if mrn_raw and mrn_raw != ' ' else None

                    # --- Supervising MD (from the fourth cell) ---
                    md_raw = cells[3].get_text(strip=True)
                    supervising_md = md_raw if md_raw and md_raw != ' ' else None  # Handle empty MD field

                    patient_data = {
                        'name': name,
                        'dob': dob,
                        'mrn': mrn,
                        'supervising_md': supervising_md,
                        'patient_id': patient_id,  # Extracted from onclick
                        'anchor_mrn': anchor_mrn  # Extracted from <a> tag's MRN attribute
                    }
                    patient_list.append(patient_data)
                except Exception as e:
                    print(f"Error processing row: {row}. Error: {e}")
            else:
                print(f"Skipping row with unexpected number of cells ({len(cells)}): {row}")

        return patient_list

    @staticmethod
    def _verify_note_str(data):
        # The pattern: "background" followed by \u0001, then "DH_" followed by alphanumeric characters,
        # then another \u0001, then the same "DH_" pattern again
        pattern = r'^background\u0001(DH_[A-Z0-9]+)\u0001\1$'

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
                        result_dict[target_field] = f"{result_dict[target_field]}\n{field_content['text']}"
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
    def remove_html_tags(text):
        """Removes HTML tags from a string."""
        # Handle <br> specifically if needed, otherwise remove all tags
        text = text.replace('<br>', '\n').replace('<br>', '\n')  # Convert breaks to newlines
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()  # Also strip leading/trailing whitespace

    @staticmethod
    def _extract_form_data_fd_only(html_string):
        """
        Extracts form data ONLY for elements with IDs starting with 'FD_',
        creating key-value pairs and formatting the result.
        Decodes HTML entities and strips tags from textareas.
        """
        form_data_dict = {}  # Use a dictionary to automatically handle potential duplicates
        # --- Textareas ---
        # Regex captures ID and the raw inner content
        textareas = re.findall(r'<textarea.*?id="([^"]*)".*?>(.*?)</textarea>', html_string, re.DOTALL)
        for id_val, raw_value in textareas:
            if id_val.startswith('FD_'):
                # Decode HTML entities (like <) first
                decoded_value = html.unescape(raw_value)
                # Remove HTML tags, convert <br> to newline (or remove if not desired)
                cleaned_value = OncoEmrIntegration._remove_html_tags(decoded_value)
                form_data_dict[id_val] = cleaned_value
        # --- Text Inputs (including hidden-like ones with value) ---
        # Capture type="text" inputs with an ID and potentially a value
        text_inputs = re.findall(r'<input.*?type="text".*?id="([^"]*)".*?(?:value="([^"]*)")?.*?>', html_string,
                                 re.IGNORECASE | re.DOTALL)
        for id_val, value in text_inputs:
            # Filter by ID prefix
            if id_val.startswith('FD_'):
                # Use the captured value, or empty string if value attribute is missing/empty
                form_data_dict[id_val] = value if value is not None else ""
        # --- Checkboxes and Radios ---
        all_inputs = re.finditer(r'<input.*?>', html_string, re.IGNORECASE | re.DOTALL)
        all_relevant_ids = set()
        checked_ids = set()
        for match in all_inputs:
            input_tag = match.group(0)
            id_match = re.search(r'id="(FD_[^"]*)"', input_tag, re.IGNORECASE)  # Filter ID here
            if id_match:
                input_id = id_match.group(1)
                type_match = re.search(r'type="(checkbox|radio)"', input_tag, re.IGNORECASE)
                if type_match:  # It's a checkbox or radio with an FD_ id
                    all_relevant_ids.add(input_id)
                    # Check if 'checked' attribute exists
                    if re.search(r'\schecked(?:=.*?)?(\s|>|/>)', input_tag, re.IGNORECASE):
                        checked_ids.add(input_id)
        # Add checkbox/radio states to the dictionary
        for id_val in all_relevant_ids:
            value = 'true' if id_val in checked_ids else 'false'
            # Ensure text inputs don't accidentally overwrite checkbox/radio state if IDs clash (unlikely but safe)
            if id_val not in form_data_dict or form_data_dict[id_val] in ['true', 'false']:
                form_data_dict[id_val] = value
        # --- Format the output ---
        # Sort keys for consistent output order (optional, but good practice)
        output_parts = [f"{k}%01{v}" for k, v in sorted(form_data_dict.items())]
        # return form_data_dict, "%02".join(output_parts)
        return form_data_dict

    @staticmethod
    def _remove_html_tags(text):
        """Removes HTML tags from a string, converting <br> to newline."""
        if text is None:
            return ""
        # Convert <br> tags (and their entity forms) to newlines first
        # Using regex for <br> tags as well for robustness
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        # Use regex to remove any remaining tags
        clean = re.compile('<.*?>')
        # Strip leading/trailing whitespace after tag removal
        return re.sub(clean, '', text).strip()

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
        soup = BeautifulSoup(full_html_string, 'html.parser')
        form_data_dict = {}  # Use a dictionary to store data (handles potential ID clashes)
        # --- Find all relevant elements by ID pattern ---
        # This is more efficient than iterating through ALL tags
        fd_elements = soup.find_all(id=lambda x: x and x.startswith('FD_'))
        for element in fd_elements:
            element_id = element['id']  # We know ID exists and starts with FD_
            tag_name = element.name.lower()
            # --- Textareas ---
            if tag_name == 'textarea':
                # Use get_text() which handles basic entity decoding and gets text within tags
                raw_text = element.get_text()
                # Further clean up <br> and potential leftover tags
                cleaned_value = OncoEmrIntegration._remove_html_tags(raw_text)
                form_data_dict[element_id] = cleaned_value
            # --- Inputs (Text, Checkbox, Radio, Hidden) ---
            elif tag_name == 'input':
                input_type = element.get('type', '').lower()
                if input_type == 'text':
                    value = element.get('value', '')
                    # Important: Don't overwrite a checkbox/radio state if an input text has the same ID
                    # (though usually separate IDs like FD_chk... and FD_itb... are used)
                    if not (element_id in form_data_dict and form_data_dict[element_id] in ['true', 'false']):
                        form_data_dict[element_id] = value
                elif input_type in ['checkbox', 'radio']:
                    is_checked = element.has_attr('checked')
                    form_data_dict[element_id] = 'true' if is_checked else 'false'
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
        table = soup.find('table', id='tblPatientVisits')
        if not table:
            return []

        # Extract headers
        headers = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all('th'):
                # Get text or id as fallback
                header_text = th.get_text().strip()
                if not header_text and th.get('id'):
                    header_text = th.get('id').replace('th', '')
                headers.append(header_text)

        # Process data rows
        patients = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            patient_data = {}

            # Extract patient ID and name from row attributes
            pid = row.get('pid', '')
            p_name = row.get('pnam', '')
            location = row.get('Location', '')

            patient_data['patient_id'] = pid
            patient_data['patient_name'] = p_name
            patient_data['location'] = location

            # Extract cell data
            cells = row.find_all('td')
            for i, cell in enumerate(cells):
                if i < len(headers):
                    # Clean the header name for use as a key
                    header_key = headers[i].replace(' ', '_').replace('(', '').replace(')', '').lower()

                    # Handle time and patient info specially
                    if i == 0:
                        # Time cell
                        time_link = cell.find('a', class_='gts')
                        if time_link:
                            patient_data['appointment_time'] = time_link.get_text().strip()
                        else:
                            patient_data['appointment_time'] = cell.get_text().strip()
                    elif i == 1:
                        # Patient info - redundant with row attribute, but keeping for completion
                        patient_link = cell.find('a')
                        if patient_link:
                            patient_data['patient_display'] = patient_link.get_text().strip()

                            # Extract MRN number if present
                            span = patient_link.find('span')
                            if span:
                                patient_data['mrn'] = span.get_text().strip()
                    else:
                        # Get all text, preserving internal structure but as a string
                        patient_data[header_key] = cell.get_text().strip()

                        # Extract room status if available
                        if header_key == 'room':
                            room_link = cell.find('a', class_='room-name')
                            if room_link:
                                patient_data['room_status'] = room_link.get_text().strip()

            patients.append(patient_data)

        return patients

    @staticmethod
    def _get_current_date():
        """
        Get the current date formatted as 'MM/DD/YYYY' (e.g., '03/18/2025')

        Returns:
            str: Current date in 'MM/DD/YYYY' format with leading zeros
        """
        current_date = datetime.now()

        # Use strftime with format specifiers for leading zeros
        formatted_date = current_date.strftime("%m/%d/%Y")

        return formatted_date

    @staticmethod
    def _create_soup(html_content) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')
