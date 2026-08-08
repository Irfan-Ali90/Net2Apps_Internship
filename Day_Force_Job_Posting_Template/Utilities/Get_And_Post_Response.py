class Get_And_Post_Response:
    BASE_URL = "https://usstage261.dayforcehcm.com/MyDayforce/u"

    def get_client_culture(self, session, scrub):
        url = f"{self.BASE_URL}/{scrub}/Framework/Localization/GetClientCulture/"
        return session.post(url)

    def get_all_job_posting_templates(self, session, scrub):
        url = f"{self.BASE_URL}/{scrub}/Recruiting/Recruiting/GetAllJobPostingTemplates"
        return session.post(url)

    def get_entity_culture_data(self, session, scrub, key_id):
        url = f"{self.BASE_URL}/{scrub}/Framework/Localization/GetEntityCultureData"
        payload = {
            "entityName": "Dayforce.Web.Recruiting.Models.Recruiting.JobPostingTemplateEntity",
            "keyId": key_id,
        }
        return session.post(url, json=payload)

    # POST calls
    def persist_job_posting_template_changes(self, session, scrub, headers, payload):
        url = f"{self.BASE_URL}/{scrub}/Recruiting/Recruiting/PersistJobPostingTemplateChanges"
        return session.post(url, headers=headers, json=payload)

    def update_entity_culture_data(self, session, scrub, headers, payload):
        url = f"{self.BASE_URL}/{scrub}/Framework/Localization/UpdateEntityCultureData/"
        return session.post(url, headers=headers, json=payload)