# app.py
import os

import boto3
from io import StringIO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import pandas as pd

options = Options()
options.binary_location = './headless-chromium'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)


def lambda_handler(event, context):
    driver.get("http://www.python.org")
    return {
        "statusCode": 200,
        "body": driver.title
    }

# def lambda_handler(event, context):
#     """
#     Invoke AWS Lambda Function
#     :param event:
#     :param context:
#     :return:
#     """
#
#     driver.get("https://www.hockey-reference.com/")
#
#     actions = ActionChains(driver)
#     nav_bar = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div[2]/ul[1]/li[3]/a')
#     actions.move_to_element(nav_bar).perform()
#
#     WebDriverWait(driver, 20).until(
#         expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#header_leagues > div:nth-child("
#                                                            "2) > div:nth-child(1) > "
#                                                            "a:nth-child(6)"))).click()
#     driver.find_element(By.CSS_SELECTOR, "th.poptip:nth-child(2)").click()
#
#     scores_url = driver.current_url
#     df = pd.read_html(scores_url, index_col=0, header=1)[0]
#
#     # Make sure we are using player totals instead of stats per team if they were moved mid-season
#     df = df.drop_duplicates(subset=['Player'], keep='first', ignore_index=True)
#
#     # Write scores to s3
#     csv_buffer = StringIO()
#     df.to_csv(csv_buffer)
#
#     s3_resource = boto3.resource('s3')
#     s3_resource.Object(os.environ['bucket'], 'scores.csv').put(Body=csv_buffer.getvalue())
#
#     selection_bar = driver.find_element(By.CSS_SELECTOR, "li.full:nth-child(6) > a:nth-child(1)")
#     actions.move_to_element(selection_bar).perform()
#
#     WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,
#                                                                       "li.full:nth-child(6) > div:nth-child(2) > "
#                                                                       "ul:nth-child(1) > li:nth-child(2) > a:nth-child("
#                                                                       "1)"))).click()
#
#     advanced_stats_url = driver.current_url
#     as_df = pd.read_html(advanced_stats_url, index_col=0, header=1)[0]
#
#     as_df = as_df.drop_duplicates(subset=['Player'], keep='first', ignore_index=True)
#
#     as_df.to_csv(csv_buffer)
#
#     s3_resource = boto3.resource('s3')
#     s3_resource.Object(os.environ['bucket'], 'advanced_stats.csv').put(Body=csv_buffer.getvalue())
#
#     driver.quit()
