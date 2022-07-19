# app.py
import os

import boto3
import logging
from io import StringIO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

options = Options()
options.binary_location = './headless-chromium'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)


def lambda_handler(event, context):
    """
    Invoke AWS Lambda Function
    :param event:
    :param context:
    :return:
    """

    logger.info("Getting driver to hockey-reference.")
    driver.get("https://www.hockey-reference.com/leagues/NHL_2022_skaters-advanced.html")

    advanced_stats_url = driver.current_url

    logger.info("Attempting to read html table into dataframe.")
    as_df = pd.read_html(advanced_stats_url, index_col=0, header=1)[0]

    logger.info("Minor transformations.")
    as_df = as_df.drop_duplicates(subset=['Player'], keep='first', ignore_index=True)

    logger.info("Writing dataframe to stringIO.")
    csv_buffer = StringIO()
    as_df.to_csv(csv_buffer)

    logger.info("Attempting to write to s3 bucket.")
    s3_resource = boto3.resource('s3')
    s3_resource.Object(os.environ['bucket'], 'advanced/advanced_stats.csv').put(Body=csv_buffer.getvalue())

    driver.quit()

    return {
        "fileKey": f'{os.environ["bucket"]}/advanced/advanced_stats.csv',
        "status": "SUCCEEDED"
    }
