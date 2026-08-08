from Utilities.Selenium_and_gspread import Selenium_Helper

class LoginMethod:

    def Login(self):
        helper = Selenium_Helper()

        helper.open_website("https://hcm41.sapsf.com", 10)

        # Company
        helper.get_element_and_enter_data("__input0-inner", "codebotforD", "id")

        # Continue
        helper.click_element("continueToLoginBtn", "id")

        # Username
        helper.get_element_and_enter_data("j_username", "sfadmin", "id")

        # Password
        helper.get_element_and_enter_data("j_password", "Sfcode123", "id")

        # Login
        helper.click_element("logOnFormSubmit", "id")

        # Data Privacy Consent
        helper.click_element("dlgButton_4:", "id")