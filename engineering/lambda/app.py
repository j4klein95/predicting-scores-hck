# app.py

import boto3
import botocore
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument('--no-sandbox')
driver = webdriver.Chrome('/var/task/chromedriver',chrome_options=chromeOptions)

def lambda_handler(event, context):
    """
    Invoke AWS Lambda Function
    :param event:
    :param context:
    :return:
    """
