from selenium import webdriver
from selenium.webdriver.common.by import By
from gspread_formatting import CellFormat, Color, format_cell_ranges
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
import os

class Selenium_Helper:
    driver = webdriver.Chrome()

    def open_website(self, url, time=0):
        self.driver.get(url)
        self.driver.implicitly_wait(time)

    def Bytypefinder(self, bytype):
        bytype = bytype.lower().strip()

        if bytype == "id":
            return By.ID

        elif bytype == "class":
            return By.CLASS_NAME

        elif bytype == "xpath":
            return By.XPATH

        elif bytype == "linktext":
            return By.LINK_TEXT

        elif bytype == "css":
            return By.CSS_SELECTOR

    def get_element(self, path, bytype=By.XPATH):
        element = self.driver.find_element(self.Bytypefinder(bytype), path)
        return element

    def get_element_text(self, path, bytype=By.XPATH):
        element = self.driver.find_element(self.Bytypefinder(bytype), path)
        return element.text

    def get_element_attribute(self, path, attr, bytype=By.XPATH):
        element = self.driver.find_element(self.Bytypefinder(bytype), path)
        return element.get_attribute(attr)

    def get_element_and_enter_data(self, path, data, bytype=By.XPATH):
        element = self.get_element(path, bytype)
        element.clear()
        element.send_keys(data)

    def click_element(self, path, bytype=By.XPATH):
        element = self.driver.find_element(self.Bytypefinder(bytype), path)
        element.click()

    def is_element_visible(self, path, bytype=By.XPATH):
        element = self.driver.find_element(self.Bytypefinder(bytype), path)
        print(element.is_enabled())

    def get_elements(self, path, bytype=By.XPATH):
        elements = self.driver.find_elements(self.Bytypefinder(bytype), path)
        return elements

    def get_elements_text(self, path, bytype=By.XPATH):
        text = []
        elements = self.driver.find_elements(self.Bytypefinder(bytype), path)
        for e in elements:
            text.append(e.text)
        return text

    def get_elements_attribute(self, path, attr, bytype=By.XPATH):
        elements = self.driver.find_elements(self.Bytypefinder(bytype), path)
        attribute_content = []
        for e in elements:
            attribute_content.append(e.get_attribute(attr))
        return attribute_content

    def open_sheet(self, sheet_name, worksheet_name):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        api_path = os.path.join(base_dir, "Api.json")
        gc = gspread.service_account(filename=api_path)
        sheet = gc.open(sheet_name).worksheet(worksheet_name)
        return sheet

    def clear_sheet(self, sheet_name, worksheet_name, header_rows=3):
        sheet = self.open_sheet(sheet_name, worksheet_name)
        last_row = sheet.row_count
        last_col = sheet.col_count
        last_col_letter = gspread.utils.rowcol_to_a1(1, last_col).rstrip('1')

        start_row = header_rows + 1
        range_to_clear = f"A{start_row}:{last_col_letter}{last_row}"
        sheet.batch_clear([range_to_clear])

    def applying_formatting(self, given_list):
        green = CellFormat(backgroundColor=Color(0.6, 1, 0.6))
        red = CellFormat(backgroundColor=Color(1, 0.6, 0.6))

        green_cells = [(cell, green) for cell, color in given_list if color == "green"]
        red_cells = [(cell, red) for cell, color in given_list if color == "red"]

        if green_cells:
            format_cell_ranges(self.sheet, green_cells)
        if red_cells:
            format_cell_ranges(self.sheet, red_cells)

    def wait_until_clickable(self, path, timeout=10, bytype="xpath"):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((self.Bytypefinder(bytype), path))
        )