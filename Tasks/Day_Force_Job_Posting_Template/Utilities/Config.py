from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Testcases.Job_Posting_Template_Reverse import Job_Posting_Reverse
from Testcases.Job_Posting_Template_Automation import Job_Posting_Template_Automation
from Testcases.Job_Posting_Template_Validation import Validation
from Controllers.Job_Posting_Template_Controllers import Job_Posting_Template_Fill_Controllers


def run_job_posting_template(revalidate_after_automation=True):
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    reverse = Job_Posting_Reverse()
    reverse_data = reverse.Job_Posting_Reverse()

    automation = Job_Posting_Template_Automation()
    automation.automation(reverse_data)

    if revalidate_after_automation:
        reverse_data = reverse.Job_Posting_Reverse()

    validation = Validation()
    validation.Job_Posting_Template_Description_Validation(sheet, reverse_data)
    validation.Job_Posting_Template_Configure_Validation(sheet, reverse_data)


if __name__ == "__main__":
    run_job_posting_template()