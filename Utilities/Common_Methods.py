from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.Selenium_and_gspread import Selenium_Helper
from gspread_formatting import CellFormat, Color, format_cell_ranges
import time


class Validation_helpers:

    def find_index(self, loaded_model, candidates, fields, used_indices=None):
        used_indices = used_indices or set()

        for index, candidate in enumerate(candidates):
            if index in used_indices:
                continue

            match = True

            for field in fields: #[ratingscale]

                if getattr(loaded_model, field) != getattr(candidate, field):
                    match = False
                    break

            if match: #Technically speaking we are doing if comp = comp give me its index
                return index

        return None


class Common_Methods:

    def applying_formatting(self, sheet, given_list):
        green = CellFormat(backgroundColor=Color(0.6, 1, 0.6))
        red = CellFormat(backgroundColor=Color(1, 0.6, 0.6))

        green_cells = [(cell, green) for cell, color in given_list if color == "green"]
        red_cells = [(cell, red) for cell, color in given_list if color == "red"]

        if green_cells:
            format_cell_ranges(sheet, green_cells)
        if red_cells:
            format_cell_ranges(sheet, red_cells)


class Rating_Scale_Operation_Helper:

    SCORE_INPUT_XPATH = "//input[@size='7']"
    LABEL_INPUT_XPATH = "//input[@size='34']"
    DESCRIPTION_TEXTAREA_XPATH = "//textarea[@cols='42']"

    def update_scale(self, description_model, option_models, exists):
        helper = Selenium_Helper()
        driver = helper.driver

        if exists:
            self.update_rating(driver, description_model, option_models)
        else:
            self.create_rating(driver, description_model, option_models)


    # CREATE

    def create_rating(self, driver, description_model, option_models):
        wait = WebDriverWait(driver, 10)

        # click on create new rating
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='17:_link']"))).click()
        time.sleep(1)


        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Build your own')]"))
        ).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='OK']"))).click()
        time.sleep(1)

        count = len(option_models)
        row = 1
        #LET US SAY IF WE HAVE MORE THAN ONE SCORE
        while row < count:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add New Score')]"))).click()
            row = row + 1

        time.sleep(1)
        scores = driver.find_elements(By.XPATH, self.SCORE_INPUT_XPATH)
        labels = driver.find_elements(By.XPATH, self.LABEL_INPUT_XPATH)
        descriptions = driver.find_elements(By.XPATH, self.DESCRIPTION_TEXTAREA_XPATH)

        for i, option in enumerate(option_models):
            scores[i].send_keys(option.option_score)
            labels[i].send_keys(option.option_label)
            descriptions[i].send_keys(option.option_description)

        driver.find_element(By.XPATH, "//input[@id='48:_txtFld']").send_keys(description_model.Rating_Scale_Name)
        time.sleep(1)
        driver.find_element(By.XPATH, "//textarea[@id='50:_txtArea']").send_keys(description_model.Rating_Scale_Description)

        driver.find_element(By.XPATH, "//a[@id='38:_link']").click()
        time.sleep(1)

        driver.refresh()
        time.sleep(1)


    # UPDATE

    def update_rating(self, driver, description_model, option_models):
        wait = WebDriverWait(driver, 20)

        row_name = description_model.Rating_Scale_Name

        links = driver.find_elements(By.XPATH, "//a[@class='fd-link fd-link--compact']")
        matched_link = None
        for link in links:
            if link.text == row_name:
                matched_link = link
                break

        matched_link.click()
        time.sleep(1)

        delete_buttons = driver.find_elements(
            By.XPATH, "//a[@class='fd-link fd-link--compact ratingScaleSmallIconPadding deleteIcon']"
        )

        current_count = len(delete_buttons)
        needed_count = len(option_models)

        if current_count > needed_count: #IF WE HAVE MORE SCORES THAN SHEET
            excess = current_count - needed_count
            for _ in range(excess):
                delete_buttons = driver.find_elements(
                    By.XPATH, "//a[@class='fd-link fd-link--compact ratingScaleSmallIconPadding deleteIcon']"
                )
                delete_buttons[-1].click()
                time.sleep(1)

        elif current_count < needed_count: #IF WE NEED MORE SCORES ADD
            missing = needed_count - current_count
            for _ in range(missing):
                wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add New Score')]"))).click()
            time.sleep(1)

        scores = driver.find_elements(By.XPATH, self.SCORE_INPUT_XPATH)
        labels = driver.find_elements(By.XPATH, self.LABEL_INPUT_XPATH)
        descriptions = driver.find_elements(By.XPATH, self.DESCRIPTION_TEXTAREA_XPATH)


        for i, option in enumerate(option_models):
            scores[i].clear()
            scores[i].send_keys(option.option_score)
            time.sleep(1)
            labels[i].clear()
            labels[i].send_keys(option.option_label)
            time.sleep(1)
            descriptions[i].clear()
            descriptions[i].send_keys(option.option_description)

        name_field = driver.find_element(By.XPATH, "//input[@id='48:_txtFld']")
        name_field.clear()
        name_field.send_keys(row_name)
        time.sleep(1)

        desc_field = driver.find_element(By.XPATH, "//textarea[@id='50:_txtArea']")
        desc_field.clear()
        desc_field.send_keys(description_model.Rating_Scale_Description)
        time.sleep(1)

        driver.find_element(By.XPATH, "//a[@id='38:_link']").click()
        time.sleep(1)

        driver.refresh()