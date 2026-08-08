import gspread
from selenium import webdriver
from Testcases.Rating_Scale_Reverse import Rating_Scale_Reverse
from Utilities.Common_Methods import Validation_helpers
from Controllers.Rating_Scale_Controllers import Rating_Scale_load_Controllers,Rating_Scale_fill_Controllers
from Utilities.Selenium_and_gspread import Selenium_Helper
from Testcases.Rating_Scale_Validation import Validation



helper = Selenium_Helper()

sheet = helper.open_sheet(
    "10. codebotforT1_sfadmin_REC_Workbook",
    "Rating Scale"
)

helper.clear_sheet(
    "10. codebotforT1_sfadmin_REC_Workbook",
    "Rating Scale"
)
# Fill sheet



# Validate
reverse = Rating_Scale_Reverse()
datalist = reverse.Rating_Scale_reverse()

controller = Rating_Scale_fill_Controllers()
controller.Rating_Scale_Processing_Rating_Scale_fill_controller(sheet, datalist)
controller.Rating_Scale_Rating_Scale_Description_fill_controller(sheet, datalist)
controller.Rating_Scale_Option_Score_fill_controller(sheet, datalist)


# Fill controllers...
validator = Validation()
validator.validate(sheet, datalist)
