from Utilities.Email_Template_Login import LoginMethod
from Utilities.Selenium_and_Gspread import Selenium_Helper
from Utilities.Get_And_Post_Response import Get_And_Post_Requests
from Models.Models_classes import Email_Notification_Template_Model
from bs4 import BeautifulSoup
import re
import time
import requests

class Email_Notification_Templates_Reverse:
    def Email_Notification_Reverse(self, pending_template_names=None):

        if pending_template_names is not None:
            pending_filter = set(pending_template_names)
        else:
            pending_filter = None

        # Login:
        login = LoginMethod()
        login.Login()

        # Selenium Helper:
        helper = Selenium_Helper()

        # Get_And_Post helper:
        API = Get_And_Post_Requests()

        # Using Scrub ID:
        # Testing Scrub:
        url = helper.driver.current_url

        match = re.search(r"_s\.crb=([^&]+)", url)

        if match:
            scurb_id = match.group(1)
            email_template_url = (
                "https://hcm41.sapsf.com/acme?"
                "fbacme_o=admin&"
                "pess_old_admin=true&"
                "ap_param_action=sys_notification&"
                f"_s.crb={scurb_id}"
            )

            helper.driver.get(email_template_url)
            time.sleep(2)

        # Now Real Work Begins:

        # Session Cookie Stealing ('^') :
        cookies = helper.driver.get_cookies()

        session = requests.Session()

        # Copy Selenium cookies
        for cookie in cookies:
            session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain"),
                path=cookie.get("path", "/")
            )

        headers = {
            "User-Agent": helper.driver.execute_script(
                "return navigator.userAgent;"
            ),
            "Referer": helper.driver.current_url,
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,"
                "image/webp,*/*;q=0.8"
            ),
        }

        request = session.get(
            url,
            headers=headers,
            allow_redirects=False
        )

        # cookies stolen now onto the actual data and payload stuff:

        # Get Request:
        request = API.get_all_email_notification_templates(session, scurb_id)

        # Using Beautiful Soup to get the elements(name,id):
        html = request.text

        soup = BeautifulSoup(html, 'html5lib')

        checkboxes = soup.find_all("input", type="checkbox")

        Datalist = []
        names = []
        statuses = []
        template_names = []
        internal_names = []
        for checkbox in checkboxes:
            name = checkbox.get("name")

            if name.startswith('chk_'):
                internal_names.append(name)
                email_name = name.removeprefix("chk_")
                names.append(email_name)

                status = checkbox.has_attr("checked")
                statuses.append(status)

                a_tag = checkbox.find_next_sibling("a")
                template_name = a_tag.get_text(strip=True) if a_tag else None
                template_names.append(template_name)

        skipped = 0

        for i, name in enumerate(names):

            if pending_filter is not None and template_names[i] not in pending_filter:
                skipped += 1
                continue

            # Model Creation:
            Email_Notification_Model = Email_Notification_Template_Model()

            request = API.get_all_elements_info(session, scurb_id, name)

            soup = BeautifulSoup(request.text, "html5lib")

            # Now extract data of particular sections:

            #--------------------Template Name-------------------------------

            Email_Notification_Model.Template_Name = template_names[i]

            #--------------------Internal Name-------------------------------
            Email_Notification_Model.Internal_Name = internal_names[i]

            #--------------------Status Checkbox:----------------------------
            Email_Notification_Model.Status = statuses[i]

            # --------------------PRIORITY STATUS:------------------------------------
            priority_checkbox = soup.find(
                "input",
                attrs={"type": "checkbox", "name": "nts_email_hpopt"}
            )

            if priority_checkbox is None:
                priority = "None"  # field doesn't exist on this template at all
            else:
                priority = priority_checkbox.has_attr("checked")

            Email_Notification_Model.Priority = priority

            #--------------------Email Subject:----------------------------------
            email_subject = soup.find("input", attrs={"type": "text", "size": "50"})

            if email_subject is None:
                subject = "None"
            else:
                subject = email_subject.get("value", "")

            Email_Notification_Model.Subject = subject

            #----------------Body---------------------
            body_text = soup.find("textarea", attrs={"name": "nts_email_body"})

            if body_text is None:
                body = "None"
            else:
                body = body_text.get_text(strip=False)

            Email_Notification_Model.Body = body

            # --------------Email Option---------------------
            email_option = soup.find(
                "input",
                attrs={"type": "checkbox", "name": "nts_email_batchopt"}
            )

            if email_option is None:
                option = "None"  # field doesn't exist on this template at all
            else:
                option = email_option.has_attr("checked")

            Email_Notification_Model.Option = option

            #Appening all stuff of model in datalist:
            Datalist.append(Email_Notification_Model)

        if pending_filter is not None:
            print(f"[reverse] Scraped {len(Datalist)} pending template(s), "
                  f"skipped {skipped} non-pending template(s) (no request made)")

        return Datalist