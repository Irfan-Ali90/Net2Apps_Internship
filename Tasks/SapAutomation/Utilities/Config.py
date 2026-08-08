from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Testcases.Rating_Scale_Reverse import Rating_Scale_Reverse
from Testcases.Rating_Scale_Automation import Rating_Scale_Automation

def run_rating_scale():
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    reverse = Rating_Scale_Reverse()
    webdatas = reverse.Rating_Scale_reverse()

    automation = Rating_Scale_Automation()
    automation.automate(sheet, webdatas)


if __name__ == "__main__":
    run_rating_scale()