from Utilities.Selenium_and_Gspread import Selenium_Helper
from Controllers.Email_Notification_Template_Controllers import Email_Notification_Template_Load_Controller
from TestCases.EMAIL_NOTIFICATION_TEMPLATES_REVERSE import Email_Notification_Templates_Reverse
from Utilities.Common_Methods import Common_Methods, Automation_Methods
from Utilities.Sheet_Title import Sheet_Title, worksheet


class EMAIL_NOTIFICATION_TEMPLATES_AUTOMATION:
    def EMAIL_NOTIFICATION_TEMPLATES_Automation(self, reverse_data, datalist):

        common = Common_Methods()
        auto_helper = Automation_Methods()

        #Look up on basis of name, web_data is a model so on basis of name we get model
        model_lookup = {}
        for web_data in reverse_data:
            if web_data.Template_Name not in model_lookup:
                model_lookup[web_data.Template_Name] = web_data

        for sheet_data in datalist:
            match = model_lookup.get(sheet_data.Template_Name)

            if match is None:
                print(f"No web match found for '{sheet_data.Template_Name}', skipping")
                continue

            subject_match = common.normalize_text(sheet_data.Subject) == common.normalize_text(match.Subject)
            body_match = common.normalize_text(sheet_data.Body) == common.normalize_text(match.Body)
            status_match = common.ConditionHandler(sheet_data.Status) == common.ConditionHandler(match.Status)
            priority_match = common.ConditionHandler(sheet_data.Priority) == common.ConditionHandler(match.Priority)
            option_match = common.ConditionHandler(sheet_data.Option) == common.ConditionHandler(match.Option)

            condition = all((
                sheet_data.Template_Name == match.Template_Name,
                subject_match,
                body_match,
                status_match,
                priority_match,
                option_match,
            ))

            if not condition:
                auto_helper.ObjectUpdate(match, sheet_data)
                print(f"Model Updated : {match.Template_Name}")
            else:
                print(f"No change needed : {match.Template_Name}")


def main():
    # Load pending rows for scraping
    loader = Email_Notification_Template_Load_Controller()
    datalist = loader.Email_Notification_Template_Load_Controller()

    pending_names = set()

    for row in datalist:
        pending_names.add(row.Template_Name)

    if not pending_names:
        print("No Pending row, nothing to automate.")
        return

    rev = Email_Notification_Templates_Reverse()
    reverse_data = rev.Email_Notification_Reverse(pending_template_names=pending_names)

    objective = EMAIL_NOTIFICATION_TEMPLATES_AUTOMATION()
    objective.EMAIL_NOTIFICATION_TEMPLATES_Automation(reverse_data, datalist)


if __name__ == "__main__":
    main()