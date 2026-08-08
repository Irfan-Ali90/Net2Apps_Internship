from Utilities.Selenium_and_Gspread import Selenium_Helper
from Controllers.Email_Notification_Template_Controllers import Email_Notification_Template_Load_Controller
from TestCases.EMAIL_NOTIFICATION_TEMPLATES_REVERSE import Email_Notification_Templates_Reverse
from Utilities.Common_Methods import Common_Methods
from Utilities.Sheet_Title import Sheet_Title, worksheet

#Validation
class EMAIL_NOTIFICATION_TEMPLATES_Validation:
    def Email_Notification_Templates_validation(self, sheet, reverse, datalist):

        common = Common_Methods()

        #Now first compare names, if they are not same make the whole row red.
        model_lookup = {}
        for web_data in reverse:
            model = web_data
            if model.Template_Name not in model_lookup:
                model_lookup[model.Template_Name] = model

        color_list = []

        for sheet_data in datalist:
            sheet_row = sheet_data.row_number
            match = model_lookup.get(sheet_data.Template_Name)

            if match is None:
                color_list.append((f"C{sheet_row}", "red"))
                color_list.append((f"D{sheet_row}", "red"))
                color_list.append((f"E{sheet_row}", "red"))
                color_list.append((f"F{sheet_row}", "red"))
                color_list.append((f"G{sheet_row}", "red"))
                color_list.append((f"H{sheet_row}", "red"))
            #Since they are not same, now compare them.
            else:
                color_list.append((f"C{sheet_row}", "green" if sheet_data.Template_Name == match.Template_Name else "red"))
                color_list.append((f"D{sheet_row}", "green" if common.ConditionHandler(sheet_data.Status) == common.ConditionHandler(match.Status) else "red"))
                color_list.append((f"E{sheet_row}", "green" if common.normalize_text(sheet_data.Subject) == common.normalize_text(match.Subject) else "red"))
                color_list.append((f"F{sheet_row}", "green" if common.ConditionHandler(sheet_data.Priority) == common.ConditionHandler(match.Priority) else "red"))
                color_list.append((f"G{sheet_row}", "green" if common.normalize_text(sheet_data.Body) == common.normalize_text(match.Body) else "red"))
                color_list.append((f"H{sheet_row}", "green" if common.ConditionHandler(sheet_data.Option) == common.ConditionHandler(match.Option) else "red"))

        common.applying_formatting(sheet, color_list)


def main():
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    # Load pending rows FIRST so we know exactly which templates to scrape.
    loader = Email_Notification_Template_Load_Controller()
    datalist = loader.Email_Notification_Template_Load_Controller()

    pending_names = set()

    for row in datalist:
        pending_names.add(row.Template_Name)

    if not pending_names:
        print("No Pending rows found — nothing to validate.")
        return

    revobj = Email_Notification_Templates_Reverse()
    reverse_data = revobj.Email_Notification_Reverse(pending_template_names=pending_names)

    obj = EMAIL_NOTIFICATION_TEMPLATES_Validation()
    obj.Email_Notification_Templates_validation(sheet, reverse_data, datalist)


if __name__ == "__main__":
    main()