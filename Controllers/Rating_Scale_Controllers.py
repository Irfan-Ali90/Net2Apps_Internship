# FILLER CONTROLLER (fills data in our sheets)

from Testcases.Rating_Scale_Reverse import Rating_Scale_Reverse
from Utilities.Selenium_and_gspread import Selenium_Helper
from Utilities.Sheet_Title import Sheet_Title, worksheet
from Models.Rating_Scale_Models import Processing_Rating_Scale_section_Model, Rating_Scale_Description_section_Model,Option_Score_section_Model


class Rating_Scale_fill_Controllers:

    # Fill data in Section 1
    def Rating_Scale_Processing_Rating_Scale_fill_controller(self, sheet, datalist):

        Selenium_Helper().clear_sheet(Sheet_Title, worksheet)

        data = []
        #for dupes vales if same item_id occurs it skips that model/template
        written = set()

        for model in datalist:
            if model[0].item_id in written:
                continue

            written.add(model[0].item_id)

            row = [
                model[0].item_id,
                model[0].Processing_Status,
                model[0].Processing_Rating_Scale
            ]
            data.append(row)

        start_row = len(sheet.col_values(1)) + 1
        end_row = start_row + len(data) - 1

        sheet.update(
            range_name=f"A{start_row}:C{end_row}",
            values=data
        )

    # Fill data in Section 2
    def Rating_Scale_Rating_Scale_Description_fill_controller(self, sheet, datalist):
        data = []
        #SAME HERE!
        written = set()

        for model in datalist:
            if model[1].item_id in written:
                continue

            written.add(model[1].item_id)

            row = [
                model[1].Rating_Scale_Name,
                model[1].Rating_Scale_Description
            ]
            data.append(row)

        start_row = len(sheet.col_values(5)) + 1
        end_row = start_row + len(data) - 1

        sheet.update(
            range_name=f"E{start_row}:F{end_row}",
            values=data
        )


    # Fill data in Section 3
    def Rating_Scale_Option_Score_fill_controller(self, sheet, datalist):
        data = []

        #NOT USING SET HERE CUZ WE WANT DUPE VALUES
        for model in datalist:
            row = [
                model[2].rating_scale,
                model[2].option_score,
                model[2].option_label,
                model[2].option_description
            ]
            data.append(row)

        start_row = len(sheet.col_values(8)) + 1
        end_row = start_row + len(data) - 1

        sheet.update(
            range_name=f"H{start_row}:K{end_row}",
            values=data
        )

class Rating_Scale_load_Controllers:
    # Loader for Section 1(DONT NEED IT)
    def Rating_Scale_Processing_Rating_Scale_load_controller(self, sheet):
        datalist = []

        start_row = 4
        end_row = len(sheet.col_values(1))

        rows = sheet.get(f"A{start_row}:C{end_row}")

        for idx, row in enumerate(rows, start=4):
            if len(row) >= 3 and row[1] == "Pending":
                model = Processing_Rating_Scale_section_Model()
                model.item_id = row[0]
                model.Processing_Status = row[1]
                model.Processing_Rating_Scale = row[2]
                model.sheet_row = idx
                datalist.append(model)

        return datalist


    def Rating_Scale_Rating_Scale_Description_load_controller(self, sheet):
        datalist = []

        start_row = 4
        end_row = len(sheet.col_values(5))

        rows = sheet.get(f"A{start_row}:F{end_row}")

        for idx, row in enumerate(rows, start=4):
            row = row + [""] * (6 - len(row))

            if row[1] == "Pending":
                model = Rating_Scale_Description_section_Model()
                model.item_id = row[0]
                model.Rating_Scale_Name = row[4]
                model.Rating_Scale_Description = row[5]
                model.sheet_row = idx
                datalist.append(model)
        return datalist


    def Rating_Scale_Rating_Scale_Description_load_all_controller(self, sheet):
        datalist = []

        start_row = 4
        end_row = len(sheet.col_values(5))

        rows = sheet.get(f"A{start_row}:F{end_row}")

        for idx, row in enumerate(rows, start=4):
            row = row + [""] * (6 - len(row)) #if let say we do have empty list use them too

            if row[4].strip():
                model = Rating_Scale_Description_section_Model()
                model.item_id = row[0]
                model.Rating_Scale_Name = row[4]
                model.Rating_Scale_Description = row[5]
                model.sheet_row = idx
                datalist.append(model)
        return datalist

    # Loader for Section 3
    def Rating_Scale_Option_Score_load_controller(self, sheet):
        datalist = []

        start_row = 4
        end_row = len(sheet.col_values(8))

        rows = sheet.get(f"A{start_row}:K{end_row}")

        for idx, row in enumerate(rows, start=4):
            row = row + [''] * (11 - len(row))

            if row[7].strip():
                model = Option_Score_section_Model()
                model.item_id = row[0]
                model.rating_scale = row[7]
                model.option_score = row[8]
                model.option_label = row[9]
                model.option_description = row[10]
                model.sheet_row = idx
                datalist.append(model)

        return datalist

def main():
    helper = Selenium_Helper()

    reverse = Rating_Scale_Reverse()
    datalist = reverse.Rating_Scale_reverse()

    sheet = helper.open_sheet(Sheet_Title, worksheet)

    helper.clear_sheet(Sheet_Title, worksheet)

    #FILLERS
    controller = Rating_Scale_fill_Controllers()
    controller.Rating_Scale_Processing_Rating_Scale_fill_controller(sheet, datalist)
    controller.Rating_Scale_Rating_Scale_Description_fill_controller(sheet, datalist)
    controller.Rating_Scale_Option_Score_fill_controller(sheet, datalist)


if __name__ == "__main__":
    main()