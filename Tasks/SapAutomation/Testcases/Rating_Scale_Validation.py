#TASK: Validation of Rating Scale (colors the sheet green/red, never touches SAP)

from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Testcases.Rating_Scale_Reverse import Rating_Scale_Reverse
from Utilities.Common_Methods import Validation_helpers, Common_Methods
from Controllers.Rating_Scale_Controllers import Rating_Scale_load_Controllers


class Rating_Scale_Validation:

    def validate(self, sheet, webdatas, section2, section3):
        helper = Validation_helpers()
        common = Common_Methods()

        webmodel2 = [webdata[1] for webdata in webdatas]
        webmodel3 = [webdata[2] for webdata in webdatas]

        used_indices = set()
        color_list = []

        for loaded_model in section2:
            row_number = loaded_model.sheet_row

            index2 = helper.find_index(loaded_model, webmodel2, ["Rating_Scale_Name"])
            exists = index2 is not None

            if not exists:
                color_list.append((f"E{row_number}", "red"))
                color_list.append((f"F{row_number}", "red"))
            else:
                web_model2 = webmodel2[index2]
                color_list.append((f"E{row_number}",
                    "green" if loaded_model.Rating_Scale_Name == web_model2.Rating_Scale_Name else "red"))
                color_list.append((f"F{row_number}",
                    "green" if loaded_model.Rating_Scale_Description == web_model2.Rating_Scale_Description else "red"))

            item_options = []

            for model in section3:

                #PUT SAME NAMES IN A LIST(DUPES)
                if model.rating_scale == loaded_model.Rating_Scale_Name:
                    item_options.append(model)

            for opt in item_options:
                opt_row = opt.sheet_row #from loader
                index3 = helper.find_index(opt, webmodel3, ["rating_scale", "option_score"], used_indices)

                #IF WE DIDNT FOUND ANY INDEX MAKE IT RED:
                if index3 is None:
                    color_list.append((f"H{opt_row}", "red"))
                    color_list.append((f"I{opt_row}", "red"))
                    color_list.append((f"J{opt_row}", "red"))
                    color_list.append((f"K{opt_row}", "red"))
                    continue

                #TO MAKE SURE WE DONT COLOR THE SAME ROW
                used_indices.add(index3)
                web_model3 = webmodel3[index3]

                color_list.append((f"H{opt_row}", "green" if opt.rating_scale == web_model3.rating_scale else "red"))
                color_list.append((f"I{opt_row}", "green" if opt.option_score == web_model3.option_score else "red"))
                color_list.append((f"J{opt_row}", "green" if opt.option_label == web_model3.option_label else "red"))
                color_list.append((f"K{opt_row}", "green" if opt.option_description == web_model3.option_description else "red"))

        common.applying_formatting(sheet, color_list)
        print("Validation completed.")


def main():
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    loader = Rating_Scale_load_Controllers()

    section2 = loader.Rating_Scale_Rating_Scale_Description_load_controller(sheet)
    section3 = loader.Rating_Scale_Option_Score_load_controller(sheet)
    pending_names = [model.Rating_Scale_Name for model in section2]

    reverse = Rating_Scale_Reverse()
    webdatas = reverse.Rating_Scale_reverse(pending_names)

    validation = Rating_Scale_Validation()
    validation.validate(sheet, webdatas, section2, section3)


if __name__ == "__main__":
    main()