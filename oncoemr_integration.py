import html
import json
import random
import re
import string
import time
from datetime import datetime
from typing import List, Dict

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from submodule_integrations.models.integration import Integration
from submodule_integrations.oncoemr.oncoemr_mapping import FOLLOWUP_TEXTFIELDS_MAPPING, FOLLOWUP_RADIO_BUTTONS_MAPPING, \
    FOLLOWUP_CHECKBOXES_MAPPING
from submodule_integrations.oncoemr.oncoemr_models import FollowupNoteTemplateModel
from submodule_integrations.utils.errors import IntegrationAuthError, IntegrationAPIError


class OncoEmrIntegration(Integration):
    def __init__(self, domain: str, token: str, network_requester=None, user_agent: str = UserAgent().random):
        super().__init__("oncoemr")
        self.user_agent = user_agent
        # self.network_requester = None
        # self.url = None
        #     self.headers = None
        #
        # async def create(self, domain: str, token: str, network_requester=None):
        self.url = domain if "https://" in domain else f"https://{domain}"
        self.network_requester = network_requester

        self.headers = {
            "Host": domain.replace('https://', ''),
            "User-Agent": self.user_agent,
            "Cookie": token,
            "Accept": "*/*",
            "Accept-Encoding": "gzip",
        }

    async def _make_request(self, method: str, url: str, **kwargs):
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
            r_headers = response.headers
            # print(r_headers)
            # msg = r_headers.get("x-message")
            raise IntegrationAPIError(
                self.integration_name,
                f"{await response.text()}",
                response.status,
                response.reason,
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

    async def fetch_visit_list(self, doctor_id: str):
        path = f"{self.url}/VisitList/UpdateVisitList"

        first_param = {
            'sVisitDate': f'{self._get_current_date()}',
            'sLocID': 'LH_0656Z562B7MPBVX00BWM,LH_Jz650539279_231,LH_05VZHYDQDHE9Q8ZR6JVR,LH_05WTYN7QPR6Z278Q3JJ5,'
                      'LH_05ZX251VZCCD1JQ4ZGPA,LH_05W6RDMVZC3VHKW66PG8,LH_066125GZ9C5TB1BYZ1Y4,LID_11,'
                      'LH_066MF8G1VDJ9QYREXY3S,LH_05XWNAJ0B7XFCNHBTHY8,LH_066MF7RTY4TKERW6BSCR,LH_Dz114987565_14,'
                      'LH_05WTXV0QP8BGANTZ7CXE,LH_05Y2K2AGQ14EACKY9W1Z,LH_065JAJHQTD1624H1W3A7,'
                      'LH_066EYKHVYP8N4YKDD1X6,LH_0676CF8XHFBE7VRWW5DK,LH_0676CBZG9MX4J8BQB54N,LH_Az592719580_14,'
                      'LH_05W6RF8TKNYPJCTWQCWF,LH_069D7FCGHG444ETPFNGS,LH_0697Q1JKWQW88CEBMNQT,'
                      'LH_069Z6WFMJFNK5R71AFT2,LH_0697R6W8XN9NCB8Y9MGJ,LH_0697Q3PJHWN3B11CM23H,'
                      'LH_069D7M9KXA4BGKQE6WQ7,LH_068MR68N5Q16W5ND0GZJ,LH_068EYQBFEVMJ5538KQ7W,'
                      'LH_069MQSC6JHA99GBWZE6N,LH_069MQT2FJW2AGQKV88NZ,LH_068Y7NK5CB11V1FAWKG0,'
                      'LH_068MR7BE0MW3VKWVNNZW,LH_068MR8V261CJ4PYA7CDQ,LH_068N3K1Q1MTVK8DC8QVJ,'
                      'LH_068MR97AR0VNHM3A7HMB,LH_069BNGP94KBQE1GNGY9X,LH_069G4REM396V056SQZZZ',
            'sResource': f'{doctor_id}',
            'bNewLocation': False,
            'bNewResource': True,
            'sMDUID': 'UID_Jz650539279_110,UID_064X0KDB4BK4RNS2186G,UID_JB804617236_37,UID_Jz111795195_31,'
                      'UID_064FSWMXCMTT0YVQZX19,UID_AS230126710_737,UID_JB87247623_83',
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
            'sUID': 'UID_067YNQBAS60SNR4XCB6H',
            'sGID': 'GH_Jz169169247_2',
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
            'locationId': 'LH_0656Z562B7MPBVX00BWM',
            '_PP': '1',
            '_': str(int(time.time() * 1000)),
        }
        path = self.url + "/WebForms/pages_pd/PD_Demographics.aspx"
        response = await self._make_request("GET", url=path, params=params, headers=self.headers)
        return response

    async def fetch_patient_demographics(self, patient_id: str):
        demographics = await self._basic_patient_demographics_data(patient_id)
        status_info = await self._patient_status_info(patient_id)

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

        due_elem = demo_soup.find('td', string='Due')
        due_value_elem = due_elem.select_one('td.gen_text')
        due_value = due_value_elem.text.strip() if due_elem else None
        balance_elem = demo_soup.find('td', string='Balance')
        balance_value_elem = balance_elem.select_one('td.gen_text')
        balance_value = balance_value_elem.text.strip() if balance_elem else None
        copay_elem = demo_soup.find('td', string='CoPay')
        copay_value_elem = copay_elem.select_one('td.gen_text')
        copay_value = copay_value_elem.text.strip() if copay_value_elem else None

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
            "due": due_value,
            "balance": balance_value,
            "copay": copay_value,
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
            "locationId": "LH_0656Z562B7MPBVX00BWM",
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

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Referer": f"{self.url}/",
        }
        response = await self._make_request("GET", note_path, headers=headers)
        return {
            "data": note_data,
            "file": response,
        }

    async def fetch_patient_notes(self, patient_id: str):
        notes = await self._get_all_notes(patient_id)
        note_files = []

        for note in notes:
            data = await self._get_note_pdf_file(
                patient_id=patient_id,
                note_id=note.get('note_id'),
            )
            data["name"] = note.get('name')
            note_files.append(data)

        return note_files

    async def _followup_note_page(self, patient_id: str):
        path = self.url + "//WebForms/PD_DocOncoNoteDB.aspx"
        params = {
            "FID": "DO_06APW5AY04PK7CHWD1EP",
            "__OS": f"GH_Jz169169247_2~UID_067YNQBAS60SNR4XCB6H~{patient_id}",
            "_SK": "",
            "__full": "true"
        }
        response = await self._make_request("GET", path, params=params, headers=self.headers)
        return response

    async def make_followup_note(self, template: FollowupNoteTemplateModel):
        patient_id = template.patient_id
        note_page = await self._followup_note_page(patient_id=patient_id)

        soup = self._create_soup(note_page)
        nc_start = note_page.find('BEGIN divTABDx/HPI') - 320
        nc_end = note_page.find('END divTABFax') + nc_start
        note_elem = soup.select_one("div#noteContent")
        note_content = note_page[nc_start:nc_end]

        existing_data = self.extract_form_data_bs(note_page)

        filled_template = self.apply_template_to_dict(template_model=template, target_dict=existing_data)
        output_parts = [f"{k}%01{v}" for k, v in filled_template.items()]
        output_string = "%02".join(output_parts)

        param_string = f"""
DH_06AX3GVPM7CS4W5F04JE%02
DH_06AX3GVPM7CS4W5F04JE%02
AsteraMedOncFollowUp-2023v9%02
Astera MedOnc Follow Up - 2023 v8%02
3%2F26%2F2025%02
DO_06APW5AY04PK7CHWD1EP%02
background%02
%02
%02
%02
GH_Jz169169247_2%02
{patient_id}%02
%02
%02
PRINT%02
Note_06AX3GT91YY56XMHP3B1%02
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
        print(response)
        return response

    @staticmethod
    def apply_template_to_dict(template_model: FollowupNoteTemplateModel, target_dict: Dict[str, str]) -> Dict[str, str]:
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
            if model_field == "patient_id" or model_field in FOLLOWUP_RADIO_BUTTONS_MAPPING:
                continue

            # Skip if no text content to add or not a field content object
            if not isinstance(field_content, dict) or not field_content.get("text"):
                continue

            # Get the corresponding field in the target dict
            if model_field in FOLLOWUP_TEXTFIELDS_MAPPING:
                target_field = FOLLOWUP_TEXTFIELDS_MAPPING[model_field]

                # Only proceed if the target field exists in the dictionary
                if target_field in result_dict:
                    if field_content.get("append", True) and result_dict[target_field]:
                        # Append to existing text with a newline
                        result_dict[target_field] = f"{result_dict[target_field]}\n{field_content['text']}"
                    else:
                        # Replace the existing text
                        result_dict[target_field] = field_content["text"]

        # Process radio button fields
        for field_name, mapping in FOLLOWUP_RADIO_BUTTONS_MAPPING.items():
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
        for field_name, field_key in FOLLOWUP_CHECKBOXES_MAPPING.items():
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
        text = text.replace('<br>', '\n').replace('<br>', '\n') # Convert breaks to newlines
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip() # Also strip leading/trailing whitespace

    @staticmethod
    def extract_form_data_fd_only(html_string):
        """
        Extracts form data ONLY for elements with IDs starting with 'FD_',
        creating key-value pairs and formatting the result.
        Decodes HTML entities and strips tags from textareas.
        """
        form_data_dict = {} # Use a dictionary to automatically handle potential duplicates
        # --- Textareas ---
        # Regex captures ID and the raw inner content
        textareas = re.findall(r'<textarea.*?id="([^"]*)".*?>(.*?)</textarea>', html_string, re.DOTALL)
        for id_val, raw_value in textareas:
            if id_val.startswith('FD_'):
                # Decode HTML entities (like <) first
                decoded_value = html.unescape(raw_value)
                # Remove HTML tags, convert <br> to newline (or remove if not desired)
                cleaned_value = OncoEmrIntegration.remove_html_tags(decoded_value)
                form_data_dict[id_val] = cleaned_value
        # --- Text Inputs (including hidden-like ones with value) ---
        # Capture type="text" inputs with an ID and potentially a value
        text_inputs = re.findall(r'<input.*?type="text".*?id="([^"]*)".*?(?:value="([^"]*)")?.*?>', html_string, re.IGNORECASE | re.DOTALL)
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
            id_match = re.search(r'id="(FD_[^"]*)"', input_tag, re.IGNORECASE) # Filter ID here
            if id_match:
                input_id = id_match.group(1)
                type_match = re.search(r'type="(checkbox|radio)"', input_tag, re.IGNORECASE)
                if type_match: # It's a checkbox or radio with an FD_ id
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
    def remove_html_tags(text):
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
    def extract_form_data_bs(full_html_string):
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
        form_data_dict = {} # Use a dictionary to store data (handles potential ID clashes)
        # --- Find all relevant elements by ID pattern ---
        # This is more efficient than iterating through ALL tags
        fd_elements = soup.find_all(id=lambda x: x and x.startswith('FD_'))
        for element in fd_elements:
            element_id = element['id'] # We know ID exists and starts with FD_
            tag_name = element.name.lower()
            # --- Textareas ---
            if tag_name == 'textarea':
                # Use get_text() which handles basic entity decoding and gets text within tags
                raw_text = element.get_text()
                # Further clean up <br> and potential leftover tags
                cleaned_value = OncoEmrIntegration.remove_html_tags(raw_text)
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
