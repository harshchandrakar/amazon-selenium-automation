from unittest.result import failfast
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from pymongo import MongoClient
import pymongo

CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"


client = MongoClient(CONNECTION_STRING)

dbname = client['scrapeData']
collection_name = dbname["datas"]

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'performance': 'ALL'}
# chrome_options = Options()
# chrome_options.add_experimental_option('w3c', False)

data = pd.read_csv('scrapping-project\AmazonData.csv')

asin = data.iloc[:100, 2]
country = data.iloc[:100, -1]
# print(asin)
# print(country)

driver = webdriver.Chrome(
    ChromeDriverManager().install(), desired_capabilities=d)

for i in range(100):
    count = 0
    finalData = {
        "title": "NA",
        "url": "NA",
        "price": "NA",
        "desc": "NA"

    }
    driver.get(f'https://www.amazon.{country[i]}/dp/{asin[i]}')
    # driver.get(f'https://www.amazon.de/dp/000101742X')

    try:
        product_title = driver.find_element(By.ID, "productTitle")
        finalData["title"] = product_title.text
    except NoSuchElementException:
        count += 1
    try:
        image_url = driver.find_element(
            By.CLASS_NAME, "a-dynamic-image").get_attribute("src")
        finalData["url"] = image_url
    except NoSuchElementException:
        count += 1
    try:
        price = driver.find_element(By.CLASS_NAME, "a-price")
        finalData["price"] = price.text
    except NoSuchElementException:
        count += 1
    try:
        desc = driver.find_element(By.ID, "detailBullets_feature_div")
        finalData["desc"] = desc.text
    except NoSuchElementException:
        count += 1

    if (count == 4):
        print(f'https://www.amazon.{country[i]}/dp/{asin[i]} not available')
    else:
        collection_name.insert_one(finalData)
        print(finalData)
    print("="*100)
