from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Day_Force_Login import Login
from Utilities.Get_And_Post_Response import Get_And_Post_Response
from Model.Model_Classes import Job_Posting_Template_Model, Configure_Job_Posting_Template_Model
import re
import time
import requests

class Job_Posting_Reverse:

    def Job_Posting_Reverse(self, pending_names=None):
       
        api = Get_And_Post_Response()

        #Login:
        helper = Selenium_Helper()
        login = Login()
        login.Day_Force_Login()

        #Get the scrub id and open the job template page:
        url = helper.driver.current_url
        match = re.search(r"/u/([^/]+)/Common", url)

        if not match:
            print("Scrub ID not found.")
            return

        scrub = match.group(1)

        job_template_url = (
            f"https://usstage261.dayforcehcm.com/MyDayforce/u/{scrub}"
            "/Common/#Sm9iUG9zdGluZ1RlbXBsYXRlQ29uZmlndXJhdGlvbg%3D%3D"
        )

        helper.driver.get(job_template_url)
        time.sleep(10)

        #COOKIES RESET

        session = requests.Session()

        cookies = helper.driver.get_cookies()

        for cookie in cookies:
            session.cookies.set(
                cookie["name"],
                cookie["value"]
            )

        #VIA CULTURE LOOKUP WE GET ALL LANGUAGES
        response = api.get_client_culture(session, scrub)

        culture_json = response.json()

        language_dict = {}

        for culture in culture_json["Result"]:
            language_dict[culture["CultureId"]] = culture["LongName"]

        #SECTION 1 DATA

        response = api.get_all_job_posting_templates(session, scrub)

        if response.status_code != 200:
            print(f"Request failed: {response.status_code}")
            return

        if "application/json" not in response.headers.get("Content-Type", ""):
            print("Response is not JSON")
            print(response.text)
            return

        raw_data = response.json()

        json_data = raw_data["EntityLists"][0]["Entities"]

        if pending_names is None:
            target_entities = json_data
        else:
            #Make a set, add all non-dup names
            pending_set = set()
            for name in pending_names:
                pending_set.add(name.strip())
            #create a list and search the names in pending_set if they exist add them in list
            target_entities = []
            for entities in json_data:
                if entities["ShortName"].strip() in pending_set:
                    target_entities.append(entities)

            print(f"Reverse: {len(target_entities)} of {len(json_data)} job posting templates are pending - fetching only those.")

        datalist = []

        #Section 1:-
        for entities in target_entities:
            key_value = entities["JobPostingTemplateId"]

            model2 = Job_Posting_Template_Model()
            model2.Item_ID = key_value
            model2.Object_Name = entities["ShortName"]
            model2.Description = entities["LongName"]
            model2.EffectiveStart = entities.get("EffectiveStart")
            model2.EffectiveEnd = entities.get("EffectiveEnd")

            #SECTION 2
            response = api.get_entity_culture_data(session, scrub, key_value)
            config_json = response.json()

            entity_lists = config_json.get("EntityLists", [])
            config_entities = entity_lists[0].get("Entities", []) if entity_lists else []

            #IF ENTITIES EXIST:
            if config_entities:
                for config_data in config_entities:
                    model3 = Configure_Job_Posting_Template_Model()
                    model3.Item_ID = str(config_data["KeyId"])
                    model3.CultureId = config_data["CultureId"]
                    model3.Object_Name_Configure = entities["ShortName"]
                    model3.Language = language_dict.get(config_data["CultureId"], "")
                    model3.Job_Posting_Configure_Name = config_data.get("ShortName", "")
                    model3.Job_Posting_Configure_Description = config_data.get("LongName", "")
                    model3.Header = config_data.get("DescriptionHeader", "")
                    model3.Footer = config_data.get("DescriptionFooter", "")

                    datalist.append([model2, model3])

            #IF IT DOESNT EXIST:
            else:
                model3 = Configure_Job_Posting_Template_Model()
                model3.Object_Name_Configure = entities["ShortName"]
                model3.Language = ""
                model3.Job_Posting_Configure_Name = ""
                model3.Job_Posting_Configure_Description = ""
                model3.Header = ""
                model3.Footer = ""

                datalist.append([model2, model3])

        return datalist