from TestCases.EMAIL_NOTIFICATION_TEMPLATES_REVERSE import Email_Notification_Templates_Reverse
from Utilities.Selenium_and_Gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Models.Models_classes import Email_Notification_Template_Model

class Email_Notification_Template_Fill_Controller:
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    def Email_Notification_Template_Fill_Controller(self, datalist):
        #Before Filling in the sheets, Clean em! :
        self.helper.clear_sheet(Sheet_Title, worksheet)

        start = 4
        end = start + len(datalist) + 1
        row_number = 0
        data = []
        for model in datalist:
            row_number += 1
            model.Item_ID = row_number
            model.Processing_Status = "Processed"

            row = [
                model.Item_ID,
                model.Processing_Status,
                model.Template_Name,
                model.Status,
                model.Subject,
                model.Priority,
                model.Body,
                model.Option,
            ]
            data.append(row)

        self.sheet.update(range_name=f"A{start}:I{end}", values=data)


class Email_Notification_Template_Load_Controller:
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    def Email_Notification_Template_Load_Controller(self):
        datalist = []
        start = 4
        end = len(self.sheet.col_values(1))

        data = self.sheet.get(f"A{start}:I{end}")

        for i, row in enumerate(data, start=4):
            if len(row) >= 8 and row[1] == "Pending":
                Email_Template_Loader_Model = Email_Notification_Template_Model()
                Email_Template_Loader_Model.Item_ID = row[0]
                Email_Template_Loader_Model.Processing_Status = row[1]
                Email_Template_Loader_Model.Template_Name = row[2]
                Email_Template_Loader_Model.Status = row[3]
                Email_Template_Loader_Model.Subject = row[4]
                Email_Template_Loader_Model.Priority = row[5]
                Email_Template_Loader_Model.Body = row[6]
                Email_Template_Loader_Model.Option = row[7]
                Email_Template_Loader_Model.row_number = i

                datalist.append(Email_Template_Loader_Model)

        return datalist

def main():
    rev = Email_Notification_Templates_Reverse()
    datalist = rev.Email_Notification_Reverse()

    Obj = Email_Notification_Template_Fill_Controller()
    Obj.Email_Notification_Template_Fill_Controller(datalist)



if __name__ == "__main__":
    main()