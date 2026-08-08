from gspread_formatting import CellFormat, Color, format_cell_ranges
import copy
import re
import time
from urllib.parse import unquote, quote
from Utilities.Selenium_and_Gspread import Selenium_Helper
import requests
from bs4 import BeautifulSoup
from Utilities.Get_And_Post_Response import Get_And_Post_Requests


class Common_Methods:

    def return_None_S2(self, data):
        if data is None:
            return "None"
        return data

    def return_None(self, data):
        if data is None:
            return None

        data = str(data).replace('\xa0', ' ').strip()

        if data == '':
            return None

        return data

    def normalize_text(self, value):
        # normalize_text
        if value is None:
            return ""
        text = str(value)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = text.replace('\xa0', ' ')
        return text.strip()

    def ConditionHandler(self, value):

        if isinstance(value, bool):
            return value

        if value is None:
            return None

        v = str(value).strip()

        if v.upper() == "TRUE":
            return True
        if v.upper() == "FALSE":
            return False
        if v.lower() == "none":
            return None

        return None

    def applying_formatting(self, sheet, given_list):
        green = CellFormat(backgroundColor=Color(0.6, 1, 0.6))
        red = CellFormat(backgroundColor=Color(1, 0.6, 0.6))

        green_cells = []
        red_cells = []

        for cell, color in given_list:
            if color == "green":
                green_cells.append((cell, green))
            elif color == "red":
                red_cells.append((cell, red))

        if green_cells:
            format_cell_ranges(sheet, green_cells)
        if red_cells:
            format_cell_ranges(sheet, red_cells)

    def Mark_Processed(self, object_name, row_index, processed_updates):
        row = row_index.get(object_name)

        if row:
            processed_updates.append({
                "range": f"B{row}",
                "values": [["Processed"]]
            })
        else:
            print(f"[WARN] Could not find sheet row for '{object_name}' to mark Processed")


class Automation_Methods:

    #To convert different results in proper results
    #Like in sheet its TRUE but in payload we need True
    def to_bool(self, value):
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        return str(value).strip().lower() in {
            "true",
            "1",
            "yes",
            "on",
            "checked"
        }

    # CORE_PAYLOAD
    CORE_PAYLOAD = {
        "bplte_p_scrollpos": "0",
        "bplte_handleto": "true",
        "bplte_company": "codebotforD",
        "bplte_orapool": "dbPool2",
        "bplte_userid": "sfadmin",
        "fbacme_o": "admin",
        "cal_subject_key": "",
        "cal_starttime_key": "",
        "cal_foldermap_id_key": "",
        "bplte_previewurl": "",
        "pp_cal_session_id": "",
        "pp_pm_owner": "",
        "fb2toolbar_scan_option_val": "",
        "admin_os": "none",
        "admin_ns": "",
        "_s.crb": None,
        "pess_old_admin": "true",
        "ap_param_action": "sys_notification",
        "nts_action": None,

        "chk_DisabledUser": "on",
        "chk_DocumentCreation": "on",
        "chk_DocumentRoute": "on",
        "chk_DocumentReject": "on",
        "chk_DocumentCompleted": "on",
        "chk_DocumentSendCopy": "on",
        "chk_DocumentSkipRoute": "on",
        "chk_DocumentExitStep": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_DOC_DELETED": "on",
        "chk_360Approval": "on",
        "chk_360Feedback": "on",
        "chk_360ExtFeedback": "on",
        "chk_360Kickoff": "on",
        "chk_360Complete": "on",
        "chk_360Rject": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_360SENDBACK_INTERN_PART_EMAIL": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_360SENDBACK_EXTERN_PART_EMAIL": "on",
        "chk_CompetencyJobcode360CalcDone": "on",
        "chk_ObjCreate": "on",
        "chk_ObjDelete": "on",
        "chk_ObjChanged": "on",
        "chk_SUCCESSLINE_CONTINUOUSFEEDBACK_ADMIN_NOTIFICATION_SETTING_FEEDBACK_RECEIVED": "on",
        "chk_SUCCESSLINE_CONTINUOUSFEEDBACK_ADMIN_NOTIFICATION_SETTING_FEEDBACK_RECEIVED_MANAGER": "on",
        "chk_SUCCESSLINE_CONTINUOUSFEEDBACK_ADMIN_NOTIFICATION_SETTING_CONTINUOUS_FEEDBACK_REQUEST": "on",
        "chk_DEVELOPMENT_MENTEE_SEND_MENTORING_REQ_TO_MENTOR": "on",
        "chk_DEVELOPMENT_MENTEE_CANCEL_MENTORING_REQ_TO_MENTOR": "on",
        "chk_DEVELOPMENT_AUTO_DECLINE_MENTORING_REQ": "on",
        "chk_DEVELOPMENT_MENTORING_MATCHED_CONFIRM_TO_MENTEE": "on",
        "chk_DEVELOPMENT_MENTORING_MATCHED_CONFIRM_TO_MENTOR": "on",
        "chk_DEVELOPMENT_MENTORING_MATCHED_CONFIRM_TO_MENTEE_OPENENROLL": "on",
        "chk_DEVELOPMENT_MENTORING_REQ_DECLINED_BY_MENTOR": "on",
        "chk_DEVELOPMENT_MENTORSHIP_CLOSED": "on",
        "chk_DEVELOPMENT_MENTORSHIP_RESTARTED": "on",
        "chk_DEVELOPMENT_MENTOR_BECOME_UNAVAILABLE_TO_MENTOR": "on",
        "chk_DEVELOPMENT_MENTOR_BECOME_UNAVAILABLE_TO_MENTEE": "on",
        "chk_DEVELOPMENT_MENTOR_BECOME_AVAILABLE_TO_MENTOR": "on",
        "chk_DEVELOPMENT_MENTOR_BECOME_AVAILABLE_TO_MENTEE": "on",
        "chk_DEVELOPMENT_MENTOR_7DAY_AVAILABILITY_REMINDER": "on",
        "chk_DEVELOPMENT_MENTOR_1DAY_AVAILABILITY_REMINDER": "on",
        "chk_DEVELOPMENT_MENTORING_JAM_ADMIN_INVITATION": "on",
        "chk_DEVELOPMENT_MENTORING_JAM_ADMIN_FAIL": "on",
        "chk_DEVELOPMENT_MENTORING_JAM_PIC_UPLOAD_FAIL": "on",
        "chk_DEVELOPMENT_MENTORING_JAM_INVITE_FAIL": "on",
        "chk_DEVELOPMENT_MENTORING_JAM_INVITE_MENTOR_MENTEE_GRP": "on",
        "chk_DEVELOPMENT_MENTOR_SEND_APPROVAL_REQ": "on",
        "chk_DEVELOPMENT_MENTOR_REQ_APPROVED_BY_MANAGER": "on",
        "chk_DEVELOPMENT_MENTOR_REQ_DECLINED_BY_MANAGER": "on",
        "chk_DEVELOPMENT_MENTOR_REQ_DECLINED_BY_MANAGER_WITH_COMMENT": "on",
        "chk_DEVELOPMENT_MENTOR_REQ_APPROVED_BY_ADM_OWN": "on",
        "chk_DEVELOPMENT_MENTOR_REQ_DECLINED_BY_ADM_OWN": "on",
        "chk_DEVELOPMENT_MENTOR_REQ_DECLINED_BY_ADM_OWN_WITH_COMMENT": "on",
        "chk_DEVELOPMENT_OVERVIEW_ASSIGN_MATCHED_CONFIRM_TO_MENTOR": "on",
        "chk_DEVELOPMENT_OVERVIEW_ASSIGN_MATCHED_CONFIRM_TO_MENTEE": "on",
        "chk_DEVELOPMENT_OVERVIEW_ASSIGN_MATCHED_REMOVAL": "on",
        "chk_DEVELOPMENT_EXTRA_MENTOR_INVITATION": "on",
        "chk_DEVELOPMENT_EXTRA_MENTEE_INVITATION": "on",
        "chk_DEVELOPMENT_OVERVIEW_PARTICIPANT_REMOVAL_AFTER_PROGRAM_START": "on",
        "chk_PERFORMANCE_MASSCREATE": "on",
        "chk_DocumentDue": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_DUE_360": "on",
        "chk_DocumentLate": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_LATE_360_EP": "on",
        "chk_ADMIN_KBA_WELCOME_MESSAGE": "on",
        "chk_PasswordChange": "on",
        "chk_DocumentTransfer": "on",
        "chk_DocumentSignature": "on",
        "chk_STEPDueNotification": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_STEP_DUE_360": "on",
        "chk_STEPOverDueNotification": "on",
        "chk_ADMIN_FUNCBLOCK_NOTIFICATION_SETTING_STEP_OVERDUE_360": "on",
        "chk_BudgetCascaded": "on",
        "chk_ReportExportFailed": "on",
        "chk_ReportExportWarning": "on",
        "chk_ReportExportSucceeded": "on",
        "chk_EZNoteNotify": "on",
        "chk_RECRUITING_ExtToIntCandConvertSuccess": "on",
        "chk_RECRUITING_IntToExtCandConvertSuccess": "on",
        "chk_NewOperatorAssignment": "on",
        "chk_RECRUITING_ImminentPurgeCandidate": "on",
        "chk_CUBETREE_MOBILE_EMAIL_ACTIVATION": "on",
        "chk_BadgeRecipientNotify": "on",
        "chk_BadgeRecipientsManagerNotify": "on",
        "chk_EMPFILE_ManagerTransferRequest": "on",
        "chk_EMPFILE_ManagerTransferApproved": "on",
        "chk_EMPFILE_ManagerTransferDeclined": "on",
        "chk_RECRUITING_AgencyNotification": "on",
        "chk_RECRUITING_shareCandidateSearch": "on",
        "chk_CALIBRATION_REQUEST_RATINGS_EMAIL": "on",
        "chk_CALIBRATION_SESSION_APPROVED_EMAIL": "on",
        "chk_CALIBRATION_AUTO_ROUTE_FORMS_EMAIL": "on",
        "chk_CALIBRATION_SESSION_ACTIVATED_EMAIL": "on",
        "chk_CALIBRATION_RATING_CHANGES_EMAIL": "on",
        "chk_CALIBRATION_SESSION_REOPENED_EMAIL": "on",
        "chk_PERFORMANCE_REQUEST_FEEDBACK_NOTIFICATION": "on",
        "chk_PERFORMANCE_FEEDBACK_REQUEST_REMINDER_NOTIFICATION": "on",
        "chk_PERFORMANCE_PROCESS_KICKOFF_MANAGER_NOTIFICATION": "on",
        "chk_PERFORMANCE_PROCESS_UPDATES_MANAGER_NOTIFICATION": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_OFFER_RECEIVED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_OFFER_DECLINED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_OFFER_DECLINED_2": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_OFFER_ACCEPTED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_OFFER_REJECTED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_ASSIGNMENT_APPLIED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_CO_OWNER_CHANGED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_ASSIGNMENT_PUBLISHED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_APPLICATION_ONGOING": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_APPLICATION_COMPLETED": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_FEEDBACK_REQUEST": "on",
        "chk_OMP_ASSIGNMENT_EMAIL_INVITATION_INVITE": "on",
        "chk_TIMEANDLABOR_TIME_ACCOUNT_PAYOUT_PLANNED_VALUES_NOTIFICATION": "on",
        "chk_TIMEANDLABOR_TIME_ACCOUNT_PAYOUT_ACTUAL_VALUES_NOTIFICATION": "on",

        "nts_batchopt_interval": "12",
        "nts_invisible_specific_form": "",
        "nts_enforce_email": "",
        "nts_switch_locale": "en_US",
    }

    KNOWN_NONSTANDARD = {"MassCreateCompensation", "DocumentCompleted"}

    KNOWN_WITH_BATCH_BLOCK = {"DocumentCreation"}

    TEMPLATE_EXTRA_FIELDS = {
        "DisabledUser": {},
        "DocumentCreation": {},
        "DocumentRoute": {},
        "MassCreateCompensation": {
            "include_name": "on",
        },
        "EMPFILE_BENEFIT_NEW_ENROLLMENT_ALLOWANCE_REIMBURSEMENT": {},
        "TIMEANDLABOR_TIME_ACCOUNT_PURCHASE_APPROVE_NOTIFICATION": {},
        "EMPFILE_BENEFIT_EDIT_ENROLLMENT_PENSIONS_SAVINGS_PLAN": {},
        "TIMEANDLABOR_TIME_ACCOUNT_PAYOUT_ACTUAL_VALUES_NOTIFICATION": {},
    }

    BATCH_BLOCK = {
        "nts_bintvl_form_id_1597": "12", "nts_bintvl_form_id_1422": "12",
        "nts_bintvl_form_id_1381": "12", "nts_bintvl_form_id_1441": "12",
        "nts_bintvl_form_id_1146": "12", "nts_bintvl_form_id_1440": "12",
        "nts_bintvl_form_id_1461": "12", "nts_enabled_form_id_1644": "on",
        "nts_batched_form_id_1644": "on", "nts_bintvl_form_id_1644": "12",
        "nts_bintvl_form_id_1265": "12", "nts_bintvl_form_id_1460": "12",
        "nts_bintvl_form_id_181": "12", "nts_bintvl_form_id_1380": "12",
        "nts_bintvl_form_id_1595": "12", "nts_bintvl_form_id_1596": "12",
        "nts_bintvl_form_id_221": "12", "nts_bintvl_form_id_1241": "12",
        "nts_bintvl_form_id_201": "12", "nts_enabled_form_id_1657": "on",
        "nts_batched_form_id_1657": "on", "nts_bintvl_form_id_1657": "12",
        "nts_enabled_form_id_1638": "on", "nts_batched_form_id_1638": "on",
        "nts_bintvl_form_id_1638": "12", "nts_bintvl_form_id_1300": "12",
        "nts_bintvl_form_id_1321": "12", "nts_bintvl_form_id_1286": "12",
        "nts_bintvl_form_id_821": "12", "nts_bintvl_form_id_1287": "12",
        "nts_enabled_form_id_1635": "on", "nts_batched_form_id_1635": "on",
        "nts_bintvl_form_id_1635": "12", "nts_bintvl_form_id_1285": "12",
        "nts_bintvl_form_id_1401": "12", "nts_enabled_form_id_1662": "on",
        "nts_batched_form_id_1662": "on", "nts_bintvl_form_id_1662": "12",
        "nts_bintvl_form_id_361": "12", "nts_enabled_form_id_1636": "on",
        "nts_batched_form_id_1636": "on", "nts_bintvl_form_id_1636": "12",
        "nts_bintvl_form_id_1421": "12", "nts_bintvl_form_id_47": "12",
        "nts_bintvl_form_id_45": "12", "nts_bintvl_form_id_42": "12",
        "nts_bintvl_form_id_1576": "12", "nts_bintvl_form_id_1577": "12",
        "nts_bintvl_form_id_1578": "12", "nts_enabled_form_id_1661": "on",
        "nts_batched_form_id_1661": "on", "nts_bintvl_form_id_1661": "12",
        "nts_bintvl_form_id_1481": "12", "nts_bintvl_form_id_46": "12",
        "nts_bintvl_form_id_341": "12", "nts_bintvl_form_id_44": "12",
        "nts_bintvl_form_id_461": "12", "nts_enabled_form_id_1645": "on",
        "nts_batched_form_id_1645": "on", "nts_bintvl_form_id_1645": "12",
        "nts_enabled_form_id_1646": "on", "nts_batched_form_id_1646": "on",
        "nts_bintvl_form_id_1646": "12", "nts_bintvl_form_id_43": "12",
        "nts_bintvl_form_id_602": "12", "nts_enabled_form_id_1637": "on",
        "nts_batched_form_id_1637": "on", "nts_bintvl_form_id_1637": "12",
        "nts_enabled_form_id_1640": "on", "nts_batched_form_id_1640": "on",
        "nts_bintvl_form_id_1640": "12", "nts_enabled_form_id_1642": "on",
        "nts_batched_form_id_1642": "on", "nts_bintvl_form_id_1642": "12",
        "nts_enabled_form_id_1643": "on", "nts_batched_form_id_1643": "on",
        "nts_bintvl_form_id_1643": "12", "nts_enabled_form_id_1659": "on",
        "nts_batched_form_id_1659": "on", "nts_bintvl_form_id_1659": "12",
        "nts_bintvl_form_id_861": "12", "nts_bintvl_form_id_1080": "12",
        "nts_bintvl_form_id_1242": "12", "nts_enabled_form_id_1647": "on",
        "nts_batched_form_id_1647": "on", "nts_bintvl_form_id_1647": "12",
        "nts_bintvl_form_id_481": "12", "nts_bintvl_form_id_1240": "12",
        "nts_bintvl_form_id_1615": "12", "nts_bintvl_form_id_1599": "12",
        "nts_bintvl_form_id_1600": "12", "nts_enabled_form_id_1660": "on",
        "nts_batched_form_id_1660": "on", "nts_bintvl_form_id_1660": "12",
        "nts_enabled_form_id_1666": "on", "nts_batched_form_id_1666": "on",
        "nts_bintvl_form_id_1666": "12", "nts_enabled_form_id_1664": "on",
        "nts_batched_form_id_1664": "on", "nts_bintvl_form_id_1664": "12",
        "nts_enabled_form_id_1665": "on", "nts_batched_form_id_1665": "on",
        "nts_bintvl_form_id_1665": "12", "nts_enabled_form_id_1667": "on",
        "nts_batched_form_id_1667": "on", "nts_bintvl_form_id_1667": "12",
        "nts_enabled_form_id_1669": "on", "nts_batched_form_id_1669": "on",
        "nts_bintvl_form_id_1669": "12", "nts_enabled_form_id_1671": "on",
        "nts_batched_form_id_1671": "on", "nts_bintvl_form_id_1671": "12",
        "nts_bintvl_form_id_1598": "12", "nts_bintvl_form_id_1616": "12",
        "nts_bintvl_form_id_561": "12", "nts_bintvl_form_id_621": "12",
        "nts_bintvl_form_id_21": "12", "nts_enabled_form_id_1639": "on",
        "nts_batched_form_id_1639": "on", "nts_bintvl_form_id_1639": "12",
        "nts_enabled_form_id_1658": "on", "nts_batched_form_id_1658": "on",
        "nts_bintvl_form_id_1658": "12", "nts_bintvl_form_id_1147": "12",
        "nts_bintvl_form_id_1480": "12", "nts_bintvl_form_id_781": "12",
        "nts_bintvl_form_id_782": "12", "nts_bintvl_form_id_1280": "12",
        "nts_bintvl_form_id_9": "12", "nts_bintvl_form_id_22": "12",
        "nts_bintvl_form_id_881": "12", "nts_bintvl_form_id_10": "12",
        "nts_bintvl_form_id_661": "12", "nts_bintvl_form_id_106": "12",
        "nts_enabled_form_id_1670": "on", "nts_batched_form_id_1670": "on",
        "nts_bintvl_form_id_1670": "12", "nts_bintvl_form_id_921": "12",
        "nts_bintvl_form_id_1403": "12", "nts_bintvl_form_id_501": "12",
        "nts_enabled_form_id_1641": "on", "nts_batched_form_id_1641": "on",
        "nts_bintvl_form_id_1641": "12", "nts_enabled_form_id_1663": "on",
        "nts_batched_form_id_1663": "on", "nts_bintvl_form_id_1663": "12",
        "nts_bintvl_form_id_1420": "12", "nts_enabled_form_id_1648": "on",
        "nts_batched_form_id_1648": "on", "nts_bintvl_form_id_1648": "12",
        "nts_bintvl_form_id_1650": "12", "nts_enabled_form_id_1651": "on",
        "nts_batched_form_id_1651": "on", "nts_bintvl_form_id_1651": "12",
        "nts_enabled_form_id_1654": "on", "nts_batched_form_id_1654": "on",
        "nts_bintvl_form_id_1654": "12", "nts_enabled_form_id_1653": "on",
        "nts_batched_form_id_1653": "on", "nts_bintvl_form_id_1653": "12",
        "nts_enabled_form_id_1655": "on", "nts_batched_form_id_1655": "on",
        "nts_bintvl_form_id_1655": "12", "nts_enabled_form_id_1668": "on",
        "nts_batched_form_id_1668": "on", "nts_bintvl_form_id_1668": "12",
        "nts_enabled_form_id_1652": "on", "nts_batched_form_id_1652": "on",
        "nts_bintvl_form_id_1652": "12", "nts_enabled_form_id_1656": "on",
        "nts_batched_form_id_1656": "on", "nts_bintvl_form_id_1656": "12",
        "nts_enabled_form_id_81": "on", "nts_batched_form_id_81": "on",
        "nts_bintvl_form_id_81": "12",
    }

    #(We can use this without instance, we can also use self)
    #But since its not like return a variable its fine to use this
    @staticmethod
    def double_encode_scrub(single_encoded_scrub):
        # double_encode_scrub
        return quote(single_encoded_scrub, safe="")

    def ensure_session(self):
        if getattr(self, "_session", None):
            return

        helper = Selenium_Helper()

        url = helper.driver.current_url
        match = re.search(r"_s\.crb=([^&]+)", url)

        if not match:
            print("Scrub ID not found - is the driver actually logged in / on the right page?")
            return

        self.scrub = match.group(1)

        print(f"[session] Captured scrub token (single-encoded): {self.scrub!r}")

        self.update_url = (
            "https://hcm41.sapsf.com/acme?"
            "fbacme_o=admin&"
            "pess_old_admin=true&"
            "ap_param_action=sys_notification&"
            f"_s.crb={self.scrub}"
        )
        helper.driver.get(self.update_url)
        time.sleep(2)

        session = requests.Session()
        for cookie in helper.driver.get_cookies():
            session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain"),
                path=cookie.get("path", "/")
            )

        self.session = session

        self.headers = {
            "User-Agent": helper.driver.execute_script("return navigator.userAgent;"),
            "Referer": helper.driver.current_url,
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,"
                "image/webp,*/*;q=0.8"
            ),
        }

        print(f"[session] POST url: {self.update_url}")

    def get_live_subject(self, html_text):
        # get subject
        soup = BeautifulSoup(html_text, "html5lib")
        email_subject = soup.find("input", attrs={"type": "text", "size": "50"})
        if email_subject is None:
            return None
        return email_subject.get("value", "")

    def get_live_body(self, html_text):
        # get body
        soup = BeautifulSoup(html_text, "html5lib")
        body_field = soup.find("textarea", attrs={"name": "nts_email_body"})
        if body_field is None:
            return None
        return body_field.get_text()

    def get_live_checkbox(self, html_text, checkbox_name):
        # get checkbox
        soup = BeautifulSoup(html_text, "html5lib")
        checkbox = soup.find("input", attrs={"type": "checkbox", "name": checkbox_name})
        if checkbox is None:
            return None
        return checkbox.has_attr("checked")

    def get_live_status(self, html_text, internal_name):
        # get status
        return self.get_live_checkbox(html_text, f"chk_{internal_name}")

    def get_all_live_checkbox_states(self, html_text):
        # get all states
        soup = BeautifulSoup(html_text, "html5lib")
        states = {}
        for checkbox in soup.find_all("input", attrs={"type": "checkbox"}):
            name = checkbox.get("name", "")
            if not name.startswith("chk_"):
                continue
            template_name = name[len("chk_"):]
            states[template_name] = checkbox.has_attr("checked") #probably thinks k template is not a string
        return states

    def build_payload(self, internal_name, sheet_data, live_states=None, overrides=None,
                       phase="save"):
        payload = dict(self.CORE_PAYLOAD) #we dont want the data to be chnaged so we make a copy
        overrides = overrides or {} #precaution so we dont get any error

        payload["_s.crb"] = self.scrub
        payload["nts_action"] = internal_name

        #These 3 are always like this in payload for some reason.
        payload["nts_notif_by_form"] = "on"
        payload["nts_invisible_specific_form"] = ""
        payload["nts_switch_form"] = "12000"

        #It works like we get 2 items save and enforce if save get rid of save and viceversa
        if phase == "save":
            payload["nts_save"] = "Save Changes" #this act as our save button
            payload.pop("nts_enforce_email", None)
        else:
            payload.pop("nts_save", None)
            payload["nts_enforce_email"] = ""

        status = self.to_bool(sheet_data.Status)
        priority = self.to_bool(overrides.get("Priority", sheet_data.Priority))
        option = self.to_bool(overrides.get("Option", getattr(sheet_data, "Option", False)))

        if internal_name in self.KNOWN_WITH_BATCH_BLOCK:
            payload.update(self.BATCH_BLOCK)

        #now we focus on status:
        if live_states is not None:
            for template_name, is_checked in live_states.items():
                key = f"chk_{template_name}"
                if is_checked:
                    payload[key] = "on"
                else:
                    payload.pop(key, None)

        status_key = f"chk_{internal_name}"
        if status:
            payload[status_key] = "on"
        else:
            payload.pop(status_key, None)

        #Anamoly Templates
        if internal_name not in self.KNOWN_NONSTANDARD:
            payload["nts_email_subject"] = overrides.get("Subject", sheet_data.Subject)
            payload["nts_email_body"] = overrides.get("Body", sheet_data.Body)

            if priority:
                payload["nts_email_hpopt"] = "on"
            else:
                payload.pop("nts_email_hpopt", None)

            if option:
                payload["nts_email_batchopt"] = "on"
            else:
                payload.pop("nts_email_batchopt", None)

        payload.update(self.TEMPLATE_EXTRA_FIELDS.get(internal_name, {}))

        return payload

    #To make sure we build the payload with new values before chaning the status as it a differet save mechanism
    #So technically we are doing k let say we saved and now we chnage the status but before lets see what was saved
    def toggle_status(self, internal_name, sheet_data, status_on, live_states,
                       settle_seconds=1.5):
        time.sleep(settle_seconds)

        API = Get_And_Post_Requests()
        post_save_page = API.get_all_elements_info(self.session, self.scrub, internal_name)

        overrides = {}
        if internal_name not in self.KNOWN_NONSTANDARD:
            live_subject = self.get_live_subject(post_save_page.text)
            live_body = self.get_live_body(post_save_page.text)
            live_priority = self.get_live_checkbox(post_save_page.text, "nts_email_hpopt")
            live_option = self.get_live_checkbox(post_save_page.text, "nts_email_batchopt")

            if live_subject is not None:
                overrides["Subject"] = live_subject
            if live_body is not None:
                overrides["Body"] = live_body
            if live_priority is not None:
                overrides["Priority"] = live_priority
            if live_option is not None:
                overrides["Option"] = live_option

            print(f"[{internal_name}] Post-save re-scrape -> "
                  f"subject={live_subject!r} priority={live_priority!r} option={live_option!r}")

        fresh_live_states = self.get_all_live_checkbox_states(post_save_page.text)

        payload = self.build_payload(
            internal_name, sheet_data, live_states=fresh_live_states, overrides=overrides,
            phase="status",
        )

        status_key = f"chk_{internal_name}"
        if status_on:
            payload[status_key] = "on"
        else:
            payload.pop(status_key, None)

        files = {"nts_file": ("", "", "application/octet-stream")}

        print(f"[{internal_name}] Toggling status -> {'on' if status_on else 'off'}")

        print("URL:", self.update_url)
        print("PAYLOAD:", payload)

        response = self.session.post(
            self.update_url,
            data=payload,
            files=files,
            headers=self.headers,
            allow_redirects=False,
        )
        print(f"[{internal_name}] Status toggle response: {response.status_code}")
        return response

    def ObjectUpdate(self, match, sheet_data):
        self.ensure_session()

        internal_name_raw = getattr(match, "Internal_Name", None) #for safety if we didnt found this we get None, not a crash
        if internal_name_raw is None:
            print("ERROR: no Internal_Name on match")
            return None

        internal_name = internal_name_raw.removeprefix("chk_")

        API = Get_And_Post_Requests()
        pre_page = API.get_all_elements_info(self.session, self.scrub, internal_name)
        live_states = self.get_all_live_checkbox_states(pre_page.text)
        print(f"[{internal_name}] Live grid scraped: {len(live_states)} checkboxes")

        payload = self.build_payload(
            internal_name, sheet_data, live_states=live_states,
            phase="save",
        )
        files = {"nts_file": ("", "", "application/octet-stream")}


        print("URL:", self.update_url)
        print("METHOD: POST")
        print("PAYLOAD:", payload)
        print("HEADERS:", self.headers)


        response = self.session.post(
            self.update_url,
            data=payload,
            files=files,
            headers=self.headers,
            allow_redirects=False,
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text[:1000])

        status = self.to_bool(sheet_data.Status)
        status_response = self.toggle_status(internal_name, sheet_data, status, live_states)

        #Verification Part, Did It Saved or Not?
        persisted = None
        status_persisted = None
        if internal_name not in self.KNOWN_NONSTANDARD:
            verify_response = API.get_all_elements_info(
                self.session, self.scrub, internal_name
            )

            #This is just a verification to see what was updated still like ours more like debigging code,
            #if we remove this section it will still work.
            live_subject = self.get_live_subject(verify_response.text)
            live_status = self.get_live_status(verify_response.text, internal_name)

            expected_subject = (sheet_data.Subject or "").strip()
            subject_persisted = bool(live_subject) and live_subject.strip() == expected_subject
            persisted = subject_persisted

            status_persisted = (live_status is not None) and (live_status == status)

            print(f"[{internal_name}] Expected subject: {sheet_data.Subject!r}")
            print(f"[{internal_name}] Actual live subject: {live_subject!r}")
            print(f"[{internal_name}] Expected status: {status!r}")
            print(f"[{internal_name}] Actual live status: {live_status!r}")

        if persisted is False:
            print(f"  WARNING: {internal_name} subject/body did NOT persist.")
        if status_persisted is False:
            print(f"  WARNING: {internal_name} status did NOT persist.")

        return response