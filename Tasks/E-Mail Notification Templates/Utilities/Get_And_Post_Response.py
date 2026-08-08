class Get_And_Post_Requests:

    Base_Url =  "https://hcm41.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=sys_notification&_s.crb="

    def get_all_email_notification_templates(self, session, scrub):
        url = f"{self.Base_Url}{scrub}"
        return session.get(url)

    def get_all_elements_info(self, session, scrub, name):
        url = (
            "https://hcm41.sapsf.com/acme?"
            "bplte_company=codebotforD&"
            "fbacme_o=admin&"
            f"_s.crb={scrub}&"
            "pess_old_admin=true&"
            "ap_param_action=sys_notification&"
            f"nts_action={name}"
        )

        return session.get(url)
