import json
import re
import time
from datetime import datetime
from typing import List, Dict

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from submodule_integrations.models.integration import Integration
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
                data = await response.read()

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
            print(r_headers)
            msg = r_headers.get("x-message")
            raise IntegrationAPIError(
                self.integration_name,
                f"{msg}",
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
