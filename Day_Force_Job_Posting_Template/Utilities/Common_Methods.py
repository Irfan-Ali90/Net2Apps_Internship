from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Get_And_Post_Response import Get_And_Post_Response
from gspread_formatting import CellFormat, Color, format_cell_ranges
import re
import uuid
import requests
from datetime import datetime, timedelta, timezone


class Common_Methods:

    def return_None_S2(self, data):
        if data == '': #if none then empty string
            return None
        return data

    def return_None(self, data):
        if data is None:
            return None

        data = str(data).replace('\xa0', ' ').strip()

        if data == '':
            return None

        return data

    # moved in from Validation - shared coloring logic
    def applying_formatting(self, sheet, given_list):
        green = CellFormat(backgroundColor=Color(0.6, 1, 0.6))
        red = CellFormat(backgroundColor=Color(1, 0.6, 0.6))

        green_cells = [(cell, green) for cell, color in given_list if color == "green"]
        red_cells = [(cell, red) for cell, color in given_list if color == "red"]

        if green_cells:
            format_cell_ranges(sheet, green_cells)
        if red_cells:
            format_cell_ranges(sheet, red_cells)

    def Mark_Processed(self, object_name, row_index, processed_updates):
        row = row_index.get(object_name)

        if row:
            processed_updates.append({
                "range": f"B{row}",
                "values": [["Processed"]]
            })
        else:
            print(f"[WARN] Could not find sheet row for '{object_name}' to mark Processed")




class Automation_Helper:


    #if sesson already exist return that one.
    def ensure_session(self):
        if getattr(self, "_session", None):
            return

        helper = Selenium_Helper()

        url = helper.driver.current_url
        match = re.search(r"/u/([^/]+)/Common", url)

        if not match:
            print("Scrub ID not found - is the driver actually logged in / on the right page?")
            return

        self.scrub = match.group(1)

        session = requests.Session()
        for cookie in helper.driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])


        #token we will use in headers, same for all iterations.
        csrf = helper.driver.execute_script(
            "return window.Dayforce?.AppSettingsData?.csrfRequestToken;"
        )

        self.session = session
        self._session = session  # FIX: was never set before, so downstream `getattr(self, "_session", None)`
                                  # checks in create_new_obj/update_old_obj always failed and returned early
                                  # without ever calling the Dayforce API. Also makes the cache guard above work.

        #this is also static in api calls
        self.client_id = 112075
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://usstage261.dayforcehcm.com",
            "Referer": f"https://usstage261.dayforcehcm.com/MyDayforce/u/{self.scrub}/Common/#Sm9iUG9zdGluZ1RlbXBsYXRlQ29uZmlndXJhdGlvbg%3D%3D",
        }
        self.culture_lookup = None

    #we have to send this to payload, so if doesnt exist we send this newly created one.
    def effective_start_now(self):
        pk_tz = timezone(timedelta(hours=5))
        return datetime.now(pk_tz).isoformat(timespec="milliseconds")

    #using this function to get a dict that we will use to get language on basis of cultureID
    def get_culture_lookup(self):
        if self.culture_lookup is not None:
            return self.culture_lookup

        api = Get_And_Post_Response()
        response = api.get_client_culture(self.session, self.scrub)
        culture_json = response.json()

        lookup = {}
        for culture in culture_json["Result"]:
            lookup[culture["LongName"]] = culture["CultureId"]

        self.culture_lookup = lookup
        return lookup

    # CREATE Method
    def create_new_obj(self, model1, model2_list):

        #same session to be used
        self.ensure_session()
        if not getattr(self, "_session", None):
            return

        api = Get_And_Post_Response()
        culture_lookup = self.get_culture_lookup()

        payload1 = [
            {
                "ClientEntityId": str(uuid.uuid4()), #new client id created everytime.
                "ClientId": None,
                "DescriptionFooter": None,
                "DescriptionHeader": None,
                "EffectiveEnd": None,
                "EffectiveStart": None,
                "EntityState": 1,
                "ExtendedProperties": [],
                "JobPostingTemplateId": None,
                "LastModifiedTimestamp": None,
                "LongName": model1.Description,
                "OriginalValues": None,
                "ShortName": model1.Object_Name,
            }
        ]

        #send this payload to create sec 1 items/elements (name,desc)
        response1 = api.persist_job_posting_template_changes(
            self.session, self.scrub, self.headers, payload1
        )

        if response1.status_code != 200:
            print(f"[CREATE] Section 1 failed: {response1.status_code} - {response1.text}")
            return False

        result1 = response1.json()
        try:
            new_template_id = result1["EntityKeys"][0]["Key"]
        except (KeyError, IndexError, TypeError):
            print(f"[CREATE] Could not read new JobPostingTemplateId from response: {result1}")
            return

        for model2 in model2_list:
            culture_id = culture_lookup.get(model2.Language) #get ID on basis of lang

            if culture_id is None:
                normalized = model2.Language.strip().lower()
                for name, cid in culture_lookup.items():
                    if name.strip().lower() == normalized:
                        culture_id = cid
                        break

            if culture_id is None:
                print(f"[CREATE] Unknown Language '{model2.Language}' - no CultureId match, skipping this language")
                print(f"[CREATE] Valid Language values for this client are: {sorted(culture_lookup.keys())}")
                continue

            payload2 = {  #same payload and define and if we dont want pop and if we wand insert
                "Entities": [
                    {
                        "ClientEntityId": str(uuid.uuid4()),
                        "ClientId": None,
                        "CultureId": culture_id,
                        "DescriptionFooter": model2.Footer,
                        "DescriptionHeader": model2.Header,
                        "EntityState": 1,
                        "KeyId": new_template_id,
                        "LastModifiedTimestamp": None,
                        "LongName": model2.Job_Posting_Configure_Description,
                        "ShortName": model2.Job_Posting_Configure_Name,
                    }
                ],
                "EntityName": "Dayforce.Web.Recruiting.Models.Recruiting.JobPostingTemplateEntity",
            }

            response2 = api.update_entity_culture_data(
                self.session, self.scrub, self.headers, payload2
            )

            print("Payload 2:")
            print(payload2)
            print(response2.status_code)
            print(response2.text)

            if response2.status_code != 200:
                print(f"[CREATE] Section 2 ({model2.Language}) failed: "
                      f"{response2.status_code} - {response2.text}")

        return True


    # UPDATE

    def update_old_obj(self, sheet2data, sheet3list, webmodel2, webmodel3):

        self.ensure_session()
        if not getattr(self, "_session", None):
            return

        api = Get_And_Post_Response()

        # MAKING SURE THAT ONLY UPDATES SECTION 2, IF ANYTHING IS CHANGED IN IT:
        if sheet2data.Object_Name != webmodel2.Object_Name or sheet2data.Description != webmodel2.Description:

            effective_start = getattr(webmodel2, "EffectiveStart", None)
            if effective_start is None:
                effective_start = self.effective_start_now()

            #secion 1 payload:
            payload1 = [
                {
                    "ClientEntityId": str(uuid.uuid4()),
                    "ClientId": self.client_id,
                    "DescriptionFooter": None,
                    "DescriptionHeader": None,
                    "EffectiveEnd": None,
                    "EffectiveStart": effective_start,
                    "EntityState": 2,
                    "ExtendedProperties": [],
                    "JobPostingTemplateId": webmodel2.Item_ID,
                    "LastModifiedTimestamp": None,
                    "LongName": sheet2data.Description,
                    "OriginalValues": None,
                    "ShortName": sheet2data.Object_Name,
                }
            ]

            response1 = api.persist_job_posting_template_changes(
                self.session, self.scrub, self.headers, payload1
            )

            if response1.status_code != 200:
                print(f"[UPDATE] Section 1 failed: {response1.status_code} - {response1.text}")
                return
        #sec 3
        common = Common_Methods()
        culture_lookup = self.get_culture_lookup()

        for i, model3sheet in enumerate(sheet3list):

            #if sheet has more lang than (lang doesnt exits)
            if i >= len(webmodel3):
                culture_id = culture_lookup.get(model3sheet.Language)

                if culture_id is None:
                    normalized = model3sheet.Language.strip().lower()
                    for name, cid in culture_lookup.items():
                        if name.strip().lower() == normalized:
                            culture_id = cid
                            break

                if culture_id is None:
                    continue

                payload2 = {
                    "Entities": [
                        {
                            "ClientEntityId": str(uuid.uuid4()),
                            "ClientId": None,
                            "CultureId": culture_id,
                            "DescriptionFooter": model3sheet.Footer,
                            "DescriptionHeader": model3sheet.Header,
                            "EntityState": 1,
                            "KeyId": webmodel2.Item_ID,
                            "LastModifiedTimestamp": None,
                            "LongName": model3sheet.Job_Posting_Configure_Description,
                            "ShortName": model3sheet.Job_Posting_Configure_Name,
                        }
                    ],
                    "EntityName": "Dayforce.Web.Recruiting.Models.Recruiting.JobPostingTemplateEntity",
                }

                response = api.update_entity_culture_data(
                    self.session, self.scrub, self.headers, payload2
                )

                if response.status_code != 200:
                    print(f"[UPDATE] Adding language '{model3sheet.Language}' to "
                          f"'{model3sheet.Object_Name_Configure}' failed: {response.status_code} - {response.text}")

                continue

            #Case 2: Language itself is changed:
            web = webmodel3[i]
            if common.return_None(model3sheet.Language) != common.return_None(web.Language):

                delete_payload = {
                    "Entities": [
                        {
                            "ClientEntityId": str(uuid.uuid4()),
                            "ClientId": self.client_id,
                            "CultureId": web.CultureId,
                            "DescriptionFooter": web.Footer,
                            "DescriptionHeader": web.Header,
                            "EntityState": 3,
                            "KeyId": int(web.Item_ID),
                            "LastModifiedTimestamp": None,
                            "LongName": web.Job_Posting_Configure_Description,
                            "ShortName": web.Job_Posting_Configure_Name,
                        }
                    ],
                    "EntityName": "Dayforce.Web.Recruiting.Models.Recruiting.JobPostingTemplateEntity",
                }

                delete_response = api.update_entity_culture_data(
                    self.session, self.scrub, self.headers, delete_payload
                )

                print("Payload 2 (delete old language):")

                if delete_response.status_code != 200:
                    print(f"[UPDATE] Deleting old language '{web.Language}' for "
                          f"'{model3sheet.Object_Name_Configure}' failed: {delete_response.status_code} "
                          f"- {delete_response.text}")
                    continue

                culture_id = culture_lookup.get(model3sheet.Language)
                if culture_id is None:
                    normalized = model3sheet.Language.strip().lower()
                    for name, cid in culture_lookup.items():
                        if name.strip().lower() == normalized:
                            culture_id = cid
                            break

                if culture_id is None:
                    continue
                #Create a new row for that changed/deleted lang row.
                create_payload = {
                    "Entities": [
                        { #copy function to define payload once
                            "ClientEntityId": str(uuid.uuid4()),
                            "ClientId": None,
                            "CultureId": culture_id,
                            "DescriptionFooter": model3sheet.Footer,
                            "DescriptionHeader": model3sheet.Header,
                            "EntityState": 1,
                            "KeyId": webmodel2.Item_ID,
                            "LastModifiedTimestamp": None,
                            "LongName": model3sheet.Job_Posting_Configure_Description,
                            "ShortName": model3sheet.Job_Posting_Configure_Name,
                        }
                    ],
                    "EntityName": "Dayforce.Web.Recruiting.Models.Recruiting.JobPostingTemplateEntity",
                }

                create_response = api.update_entity_culture_data(
                    self.session, self.scrub, self.headers, create_payload
                )


                if create_response.status_code != 200:
                    print(f"[UPDATE] Recreating '{model3sheet.Object_Name_Configure}' with new "
                          f"language '{model3sheet.Language}' failed: {create_response.status_code} "
                          f"- {create_response.text}")

                continue

            #Now if langugae is same, but other stuff is changed:
            changed = (
                common.return_None(model3sheet.Job_Posting_Configure_Name) != common.return_None(web.Job_Posting_Configure_Name) or
                common.return_None(model3sheet.Job_Posting_Configure_Description) != common.return_None(web.Job_Posting_Configure_Description) or
                common.return_None(model3sheet.Header) != common.return_None(web.Header) or
                common.return_None(model3sheet.Footer) != common.return_None(web.Footer)
            )

            if not changed:
                continue

            payload2 = {
                "Entities": [
                    {
                        "ClientEntityId": str(uuid.uuid4()),
                        "ClientId": self.client_id,
                        "CultureId": web.CultureId,
                        "DescriptionFooter": model3sheet.Footer,
                        "DescriptionHeader": model3sheet.Header,
                        "EntityState": 2,
                        "KeyId": int(web.Item_ID),
                        "LastModifiedTimestamp": None,
                        "LongName": model3sheet.Job_Posting_Configure_Description,
                        "ShortName": model3sheet.Job_Posting_Configure_Name,
                    }
                ],
                "EntityName": "Dayforce.Web.Recruiting.Models.Recruiting.JobPostingTemplateEntity",
            }

            response = api.update_entity_culture_data(
                self.session, self.scrub, self.headers, payload2
            )

            print("Payload 2 (update):")

            if response.status_code != 200:
                print(f"[UPDATE] Section 2 ({model3sheet.Language}) failed: "
                      f"{response.status_code} - {response.text}")