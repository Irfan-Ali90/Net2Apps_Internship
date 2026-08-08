from Utilities.Selenium_and_gspread import Selenium_Helper
import time
from selenium.common.exceptions import TimeoutException


class Login:

    def Day_Force_Login(self):

        url = "https://usstage261.dayforcehcm.com/MyDayforce/MyDayforce.aspx"

        helper = Selenium_Helper()
        helper.open_website(url)

        #Enter Company ID:
        helper.get_element_and_enter_data("//input[@id='txtCompanyId']","sipartnereycan01stage")
        time.sleep(1)

        #click Continue to Username:
        helper.click_element("//input[@id='MainContent_loginUI_cmdLogin']")
        time.sleep(1)

        #Enter Username:
        helper.get_element_and_enter_data( "//input[@id='txtNewUserName']", "wajimam@net2apps.com")
        time.sleep(1)

        #click continue to password:
        helper.click_element( "//input[@id='MainContent_loginUI_cmdLogin']")
        time.sleep(1)

        #Enter Password:
        helper.get_element_and_enter_data("//input[@id='txtNewUserPass']", "Welcome123!")
        time.sleep(1)

        #Click On Login:
        helper.wait_until_clickable("//input[@id='MainContent_loginUI_cmdLogin']")
        helper.click_element("//input[@id='MainContent_loginUI_cmdLogin']")
        time.sleep(20)


        #Quit Cookies menu
        try:
            helper.wait_until_clickable("//div[@id='onetrust-close-btn-container']/button", timeout=3)
            helper.click_element("//div[@id='onetrust-close-btn-container']/button")
        except TimeoutException:
            pass #always print


        #Click On Skip:
        helper.wait_until_clickable("//span[@aria-labelledby='Button_2_label']",60)
        helper.click_element("//span[@aria-labelledby='Button_2_label']")

        #Click On Test-role001:
        helper.wait_until_clickable("//input[@id='Framework_UI_Form_RadioButton_9']",50)
        helper.click_element("//input[@id='Framework_UI_Form_RadioButton_9']")

        #Click on Next:
        helper.wait_until_clickable("//span[@id='evrDialog-button']")
        helper.click_element("//span[@id='evrDialog-button']")
        time.sleep(10)


