from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd

# Re-write this line to use your own browser driver.
driver = webdriver.Firefox()

driver.get("https://www.hockey-reference.com/")

actions = ActionChains(driver)
nav_bar = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div[2]/ul[1]/li[3]/a')
actions.move_to_element(nav_bar).perform()

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#header_leagues > div:nth-child("
                                                                                   "2) > div:nth-child(1) > "
                                                                                   "a:nth-child(6)"))).click()
driver.find_element(By.CSS_SELECTOR, "th.poptip:nth-child(2)").click()

scores_url = driver.current_url
df = pd.read_html(scores_url, index_col=0, header=1)[0]

# Make sure we are using player totals instead of stats per team if they were moved mid-season
df = df.drop_duplicates(subset=['Player'], keep='first', ignore_index=True)

df.to_csv("..\\data\\scores.csv")

selection_bar = driver.find_element(By.CSS_SELECTOR, "li.full:nth-child(6) > a:nth-child(1)")
actions.move_to_element(selection_bar).perform()

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                  "li.full:nth-child(6) > div:nth-child(2) > "
                                                                  "ul:nth-child(1) > li:nth-child(2) > a:nth-child("
                                                                  "1)"))).click()

advanced_stats_url = driver.current_url
as_df = pd.read_html(advanced_stats_url, index_col=0, header=1)[0]

as_df = as_df.drop_duplicates(subset=['Player'], keep='first', ignore_index=True)

as_df.to_csv("..\\data\\advanced_stats.csv")

driver.quit()
