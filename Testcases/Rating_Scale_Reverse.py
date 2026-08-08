from Models.Rating_Scale_Models import Processing_Rating_Scale_section_Model,Rating_Scale_Description_section_Model,Option_Score_section_Model
from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sap_Login import LoginMethod
import re
import time

class Rating_Scale_Reverse:

    #Using argument pending_names cuz we want to call only those temp who are pending in auto/val
    def Rating_Scale_reverse(self, pending_names=None):

        #In this list we store the model data or the scraped data we got!
        scraped_list = []
        item_id = 1

        helper = Selenium_Helper()
        # Login
        login = LoginMethod()
        login.Login()

        # Get current URL after login
        url = helper.driver.current_url

        match = re.search(r"_s\.crb=([^&]+)", url)

        if match:
            scrub = match.group(1)

            rating_url = (
                "https://hcm41.sapsf.com/acme?"
                "fbacme_o=admin&"
                "pess_old_admin=true&"
                "ap_param_action=form_rating_scale&"
                "itrModule=talent&"
                f"_s.crb={scrub}"
            )

            helper.driver.get(rating_url)
            time.sleep(10)

        else:
            print("Scrub ID not found.")


        all_links = helper.get_elements("//a[@class='fd-link fd-link--compact']")
        all_names = [link.text.strip() for link in all_links]

        #Since when we first fill it will be none so simply make an empty list and put the names in it.
        if pending_names is None:
            target_indices = []

            for i in range(len(all_names)):
                target_indices.append(i)

        else:
            #Incase its called and not empty we make a set, and search the names from the list,
            #and put them in the list
            pending_set = set()

            for name in pending_names:
                pending_set.add(name.strip())

            target_indices = []

            for i, name in enumerate(all_names):
                if name in pending_set:
                    target_indices.append(i)

            print(
                f"Reverse: {len(target_indices)} of {len(all_names)} rating scales are pending - scraping only those.")

        #Looping through the named list:
        for i in target_indices:

            # Refresh the list after every page refresh
            links = helper.get_elements("//a[@class='fd-link fd-link--compact']")
            links[i].click()

            # Name & Description
            name_text = helper.get_element_attribute("48:_txtFld", "value", "id")
            description_text = helper.get_element_attribute("50:_txtArea", "value", "id")

            # Option fields
            scores = helper.get_elements("//input[@maxlength='10']")
            labels = helper.get_elements("//input[@size='34']")
            descriptions = helper.get_elements("//textarea[@rows='2']")

            # Section 1
            model1 = Processing_Rating_Scale_section_Model()
            model1.item_id = str(item_id)
            model1.Processing_Status = "Processed"
            model1.Processing_Rating_Scale = name_text

            # Section 2
            model2 = Rating_Scale_Description_section_Model()
            model2.item_id = str(item_id)
            model2.Rating_Scale_Name = name_text
            model2.Rating_Scale_Description = description_text

            # Section 3
            for j in range(len(scores)):

                model3 = Option_Score_section_Model()
                model3.item_id = str(item_id)
                model3.rating_scale = name_text
                model3.option_score = scores[j].get_attribute("value")
                model3.option_label = labels[j].get_attribute("value")
                model3.option_description = descriptions[j].text

                scraped_list.append([model1, model2, model3])

            item_id += 1

            helper.driver.refresh()

        return scraped_list