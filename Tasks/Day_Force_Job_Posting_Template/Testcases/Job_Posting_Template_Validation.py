from Testcases.Job_Posting_Template_Reverse import Job_Posting_Reverse
from Controllers.Job_Posting_Template_Controllers import Job_Posting_Template_Load_Controllers
from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Common_Methods import Common_Methods
from Utilities.Sheet_Title import Sheet_Title, worksheet

class Validation:

    # SECTION 2
    def Job_Posting_Template_Description_Validation(self, sheet, reverse_data):
        common = Common_Methods()
        loader = Job_Posting_Template_Load_Controllers()
        datalist = loader.Job_Posting_Template_Description_Load()

        # dedupe web data by Object_Name
        valid_model2 = {}
        for webdata in reverse_data:
            model2 = webdata[0]
            if model2.Object_Name not in valid_model2:
                valid_model2[model2.Object_Name] = model2

        color_list = []
        for sheet_data in datalist:
            row_number = sheet_data.sheet_row
            match = valid_model2.get(sheet_data.Object_Name)

            if match is None:
                color_list.append((f"E{row_number}", "red"))
                color_list.append((f"F{row_number}", "red"))

            else:
                color_list.append((f"E{row_number}", "green" if sheet_data.Object_Name == match.Object_Name else "red"))
                color_list.append((f"F{row_number}", "green" if common.return_None_S2(sheet_data.Description) == match.Description else "red"))

        common.applying_formatting(sheet, color_list)

    # SECTION 3
    def Job_Posting_Template_Configure_Validation(self, sheet, reverse_data):
        common = Common_Methods()
        loader = Job_Posting_Template_Load_Controllers()
        datalist = loader.Job_Posting_Template_Configure_Load()

        # only for those who are pending:
        pending_list = loader.Job_Posting_Template_Processing_Load()

        row_index = {}
        for model in pending_list:
            row_index[model.Processing_Object] = model.sheet_row

        # making web data to be same to allow working with sheet
        web_groups = {}
        for webdata in reverse_data:
            model3 = webdata[1]
            web_groups.setdefault(model3.Object_Name_Configure, []).append(model3)
            #NAME, MODEL

        # same reason
        sheet_groups = {}
        for sheet_data in datalist:
            sheet_groups.setdefault(sheet_data.Object_Name_Configure, []).append(sheet_data)

        color_list = []
        processed_updates = []

        for object_name, sheet_rows in sheet_groups.items():
            web_rows = web_groups.get(object_name) #By default values if key doesnt found

            for position, sheet_data in enumerate(sheet_rows):
                row_number = sheet_data.sheet_row

                #Case 1: Doesnt exist
                if web_rows is None:
                    #whole row red
                    row_colors = {}
                    for col in "HIJKLM":
                        row_colors[col] = "red"

                #If obj exists: but sheet has more rows than web, so color the row red that doesn't exist in web(S2)
                elif position >= len(web_rows):
                    row_colors = {"H": "green"}
                    for col in "IJKLM":
                        row_colors[col] = "red"

                #If both obj is existing and len is same, compare:
                else:
                    match = web_rows[position]
                    row_colors = {
                        "H": "green",
                        "I": "green" if common.return_None(sheet_data.Language) == common.return_None(match.Language) else "red",
                        "J": "green" if common.return_None(sheet_data.Job_Posting_Configure_Name) == common.return_None(match.Job_Posting_Configure_Name) else "red",
                        "K": "green" if common.return_None(sheet_data.Job_Posting_Configure_Description) == common.return_None(match.Job_Posting_Configure_Description) else "red",
                        "L": "green" if common.return_None(sheet_data.Header) == common.return_None(match.Header) else "red",
                        "M": "green" if common.return_None(sheet_data.Footer) == common.return_None(match.Footer) else "red",
                    }

                common.Mark_Processed(sheet_data.Object_Name_Configure, row_index, processed_updates)

                for col, color in row_colors.items():
                    color_list.append((f"{col}{row_number}", color))

        common.applying_formatting(sheet, color_list)

        if processed_updates:
            sheet.batch_update(processed_updates)

def main():
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    loader = Job_Posting_Template_Load_Controllers()

    pending_list = loader.Job_Posting_Template_Processing_Load()

    pending_names = []
    for model in pending_list:
        pending_names.append(model.Processing_Object)

    reverse_data = Job_Posting_Reverse().Job_Posting_Reverse(pending_names)

    obj = Validation()
    obj.Job_Posting_Template_Description_Validation(sheet, reverse_data)
    obj.Job_Posting_Template_Configure_Validation(sheet, reverse_data)


if __name__ == "__main__":
    main()