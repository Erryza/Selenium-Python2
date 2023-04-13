from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://demoqa.com/webtables")

# read count rows
tRow = driver.find_elements(
    By.XPATH, "//div[@role='rowgroup']")
length = len(tRow)

for countRows in range(length):
    try:
        # delete data
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[@id='delete-record-{countRows+1}']"))).click()
    except TimeoutException:
        break

# read file json
with open("data.json") as data:
    fileData = json.load(data)

for rowsData in fileData:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, "addNewRecordButton"))).click()

    # input data
    for var, val in rowsData.items():
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.ID, var)))
        driver.find_element(By.ID, var).send_keys(val)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.ID, "submit"))).click()
    sleep(10)
