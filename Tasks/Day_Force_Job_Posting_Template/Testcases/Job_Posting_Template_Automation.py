from Testcases.Job_Posting_Template_Reverse import Job_Posting_Reverse
from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Utilities.Common_Methods import Automation_Helper
from Utilities.Common_Methods import Common_Methods
from Controllers.Job_Posting_Template_Controllers import Job_Posting_Template_Load_Controllers

class Job_Posting_Template_Automation:

    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)
    autohelper = Automation_Helper()
    common = Common_Methods()

    def automation(self, reverse_data):

        loader = Job_Posting_Template_Load_Controllers()

        #Sec 2
        datalist1 = loader.Job_Posting_Template_Description_Load()

        #Sec 3
        datalist2 = loader.Job_Posting_Template_Configure_Load()

        #Getting row_index, So we know which row to color:
        pending_list = loader.Job_Posting_Template_Processing_Load()

        row_index = {}
        for p in pending_list:
            row_index[p.Processing_Object] = getattr(p, "sheet_row", None)

        #section 3
        model3_sheet = {}
        for config in datalist2:
            model3_sheet.setdefault(config.Object_Name_Configure, []).append(config)
            #Name, Model

        #section 2 web object
        web_objects = {}

        #section 3 web object
        web_configs = {}

        for web in reverse_data:
            model2 = web[0]
            model3 = web[1]

            #look up on basis of name to get model
            web_objects[model2.Object_Name] = model2

            if model3.Language:
                web_configs.setdefault(model3.Object_Name_Configure, []).append(model3)

        for sheet_model2_data in datalist1:

            #name of obj in sec 2
            model_name = sheet_model2_data.Object_Name

            #give this name to sheet look up
            sheet_model3_list = model3_sheet.get(model_name, [])

            #pass name for model 2 look up
            web_model2 = web_objects.get(model_name)

            #and same for model 3 look up
            web_model3 = web_configs.get(model_name, [])

            # Case 1: if element is not in web:
            if web_model2 is None:
                #Call creater
                self.autohelper.create_new_obj(sheet_model2_data, sheet_model3_list)
                continue

            # If Exists, Now we compare:

            # For section 2:
            Section2_Compare = (
                    self.common.return_None_S2(sheet_model2_data.Description)
                    ==
                    self.common.return_None_S2(web_model2.Description)
            )

            # For Section 3:
            Section3_Compare = True

            for i, sheet_comp in enumerate(sheet_model3_list):

                # if web data is less than sheet data of model 3
                if i >= len(web_model3):
                    Section3_Compare = False
                    break

                web_comp = web_model3[i]

                # now we compare it with the sheet3 model and web model3
                if (self.common.return_None(sheet_comp.Language) != self.common.return_None(web_comp.Language) or
                        self.common.return_None(sheet_comp.Job_Posting_Configure_Name) != self.common.return_None(web_comp.Job_Posting_Configure_Name) or
                        self.common.return_None(sheet_comp.Job_Posting_Configure_Description) != self.common.return_None(web_comp.Job_Posting_Configure_Description) or
                        self.common.return_None(sheet_comp.Header) != self.common.return_None(web_comp.Header) or
                        self.common.return_None(sheet_comp.Footer) != self.common.return_None(web_comp.Footer)):
                    Section3_Compare = False
                    break

            if Section2_Compare and Section3_Compare: #If both are True Pass
                pass  # MARK THEM
            else:
                # UPDATE THEM:
                self.autohelper.update_old_obj(
                    sheet_model2_data,
                    sheet_model3_list,
                    web_model2,
                    web_model3
                )

def main():
    loader = Job_Posting_Template_Load_Controllers()

    pending_list = loader.Job_Posting_Template_Processing_Load()

    pending_names = []
    for model in pending_list:
        pending_names.append(model.Processing_Object)

    reverse_list = Job_Posting_Reverse().Job_Posting_Reverse(pending_names)
    automation_obj = Job_Posting_Template_Automation()
    automation_obj.automation(reverse_list)


if __name__ == "__main__":
    main()