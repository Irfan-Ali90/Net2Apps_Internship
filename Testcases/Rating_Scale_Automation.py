#TASK: Automation of Rating Scale (create/update whatever doesn't match SAP)

from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Testcases.Rating_Scale_Reverse import Rating_Scale_Reverse
from Utilities.Common_Methods import Validation_helpers
from Controllers.Rating_Scale_Controllers import Rating_Scale_load_Controllers
from Utilities.Common_Methods import Rating_Scale_Operation_Helper


class Rating_Scale_Automation:

    def automate(self, sheet, webdatas, section2, section3):
        helper = Validation_helpers()
        R_helper = Rating_Scale_Operation_Helper()

        webmodel2 = [webdata[1] for webdata in webdatas]
        webmodel3 = [webdata[2] for webdata in webdatas]

        used_indices = set()

        for loaded_model in section2:
            matched = True

            index2 = helper.find_index(loaded_model, webmodel2, ["Rating_Scale_Name"])
            exists = index2 is not None

            if exists:
                web_model2 = webmodel2[index2]
                matched = (
                    loaded_model.Rating_Scale_Name == web_model2.Rating_Scale_Name
                    and loaded_model.Rating_Scale_Description == web_model2.Rating_Scale_Description
                )

            item_options = []

            for model in section3:

                if model.rating_scale == loaded_model.Rating_Scale_Name:
                    item_options.append(model)

            for opt in item_options:
                index3 = helper.find_index(opt, webmodel3, ["rating_scale", "option_score"], used_indices)

                if index3 is None:
                    matched = False
                    continue

                used_indices.add(index3)
                web_model3 = webmodel3[index3]

                if not (
                    opt.rating_scale == web_model3.rating_scale
                    and opt.option_score == web_model3.option_score
                    and opt.option_label == web_model3.option_label
                    and opt.option_description == web_model3.option_description
                ):
                    all_matched = False

            if not exists or not matched:
                R_helper.update_scale(loaded_model, item_options, exists)

        print("Automation completed.")


def main():
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    loader = Rating_Scale_load_Controllers()

    section2 = loader.Rating_Scale_Rating_Scale_Description_load_controller(sheet)
    section3 = loader.Rating_Scale_Option_Score_load_controller(sheet)
    pending_names = [model.Rating_Scale_Name for model in section2]

    reverse = Rating_Scale_Reverse()
    webdatas = reverse.Rating_Scale_reverse(pending_names)

    automation = Rating_Scale_Automation()
    automation.automate(sheet, webdatas, section2, section3)


if __name__ == "__main__":
    main()