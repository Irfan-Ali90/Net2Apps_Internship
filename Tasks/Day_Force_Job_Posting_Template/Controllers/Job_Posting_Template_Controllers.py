from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Testcases.Job_Posting_Template_Reverse import Job_Posting_Reverse
from Model.Model_Classes import Job_Posting_Processing_Model,Job_Posting_Template_Model,Configure_Job_Posting_Template_Model

class Job_Posting_Template_Fill_Controllers:
    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)


    def Job_Posting_Template_Processing_Fill(self, datalist ):
        self.helper.clear_sheet(Sheet_Title, worksheet)
        start_row = 4
        end_row = start_row + len(datalist) - 1

        data = []
        written = set()
        row_number = 0
        for model in datalist:
            if model[0].Object_Name in written:
                continue

            written.add(model[0].Object_Name)

            row_number += 1
            processing_status = "Processed"

            row = [
                row_number,
                processing_status,
                model[0].Object_Name
            ]
            data.append(row)

        self.sheet.update(range_name=f"A{start_row}:C{end_row}", values=data)

    def Job_Posting_Template_Description_Fill(self,datalist):
        start_row = 4
        end_row = start_row + len(datalist) - 1
        written = set()
        data = []

        for model2 in datalist:
            if model2[0].Object_Name in written:
                continue

            written.add(model2[0].Object_Name)
            row = [
                model2[0].Object_Name,
                model2[0].Description
            ]

            data.append(row)

        self.sheet.update(
            range_name=f"E{start_row}:F{end_row}",
            values=data
        )

    def Job_Posting_Template_Configure_Fill(self,datalist):
        data = []

        for model in datalist:
            row = [
                model[1].Object_Name_Configure,
                model[1].Language,
                model[1].Job_Posting_Configure_Name,
                model[1].Job_Posting_Configure_Description,
                model[1].Header,
                model[1].Footer,
            ]
            data.append(row)

        start_row = 4
        end_row = start_row + len(data) - 1

        self.sheet.update(
            range_name=f"H{start_row}:M{end_row}",
            values=data
        )

class Job_Posting_Template_Load_Controllers:

    helper = Selenium_Helper()
    sheet = helper.open_sheet(Sheet_Title, worksheet)

    #Section 1:
    def Job_Posting_Template_Processing_Load(self):
        datalist = []

        start = 4
        end = len(self.sheet.col_values(1))

        rows = self.sheet.get(f"A{start}:C{end}")

        for idx, row in enumerate(rows, start=4):
            if len(row) >= 3 and row[1] == "Pending":
                model1 = Job_Posting_Processing_Model()
                model1.Item_ID = row[0]
                model1.Processing_Status = row[1]
                model1.Processing_Object = row[2]
                model1.sheet_row = idx
                datalist.append(model1)

        return datalist

    #Section 2:
    def Job_Posting_Template_Description_Load(self):
        datalist =[]

        start = 4
        end = len(self.sheet.col_values(5))

        rows = self.sheet.get(f"A{start}:F{end}")

        for idx, row in enumerate(rows, start=4):
            row = row + [''] * (6 - len(row))
            if len(row) >= 6 and row[1] == "Pending":
                model2 = Job_Posting_Template_Model()
                model2.sheet_row = idx
                model2.Object_Name = row[4]
                model2.Description = row[5]
                datalist.append(model2)

        return datalist

    #Section 3
    # Section 3
    def Job_Posting_Template_Configure_Load(self):
        datalist = []

        start = 4
        end = len(self.sheet.col_values(8))

        rows = self.sheet.get(f"A{start}:M{end}")

        pending_list = self.Job_Posting_Template_Processing_Load()

        pending_lookup = {}

        for model in pending_list:
            pending_lookup[model.Processing_Object] = model.Item_ID

        for idx, row in enumerate(rows, start=4):

            row = row + [''] * (13 - len(row))
            object_name_configure = row[7].strip()

            if object_name_configure and object_name_configure in pending_lookup:
                model3 = Configure_Job_Posting_Template_Model()
                model3.Item_ID = pending_lookup.get(object_name_configure)
                model3.sheet_row = idx
                model3.Object_Name_Configure = row[7]
                model3.Language = row[8]
                model3.Job_Posting_Configure_Name = row[9]
                model3.Job_Posting_Configure_Description = row[10]
                model3.Header = row[11]
                model3.Footer = row[12]

                datalist.append(model3)

        return datalist

def main():
    data = Job_Posting_Reverse()
    datalist = data.Job_Posting_Reverse()

    filler = Job_Posting_Template_Fill_Controllers()
    filler.Job_Posting_Template_Processing_Fill(datalist)
    filler.Job_Posting_Template_Description_Fill(datalist)
    filler.Job_Posting_Template_Configure_Fill(datalist)

if __name__ == "__main__":
    main()