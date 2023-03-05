import subprocess
import os
import csv
import re
import time
import datetime
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller


# create directories if they don't exist
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-1])
input_dir = os.path.join(parent_dir, "inputs")
scripts = os.path.join(parent_dir, "scripts")
localhost = os.path.join(parent_dir, "localhost")
input_visualizer = os.path.join(input_dir, "inputs_visualizer")
download_dir = os.path.join(parent_dir, "download")
outputs_dir = os.path.join(parent_dir, "outputs")
if not os.path.exists(outputs_dir):
    os.mkdir(outputs_dir)

outputs_csv_dir = os.path.join(outputs_dir, "csv")
outputs_chart_dir = os.path.join(outputs_dir, "chart")

if not os.path.exists(download_dir):
    os.mkdir(download_dir)
if not os.path.exists(outputs_csv_dir):
    os.mkdir(outputs_csv_dir)
if not os.path.exists(outputs_chart_dir):
    os.mkdir(outputs_chart_dir)
if not os.path.exists(input_visualizer):
    os.mkdir(input_visualizer)
if not os.path.exists(localhost):
    os.mkdir(localhost)


country_dict = {'United States' : 'https://www.amazon.com',
'United Kingdom' : 'https://www.amazon.co.uk',
'Canada' : 'https://www.amazon.ca',
'Germany' : 'https://www.amazon.de',
'France' : 'https://www.amazon.fr',
'Italy' : 'https://www.amazon.it',
'Spain' : 'https://www.amazon.es',
'Japan' : 'https://www.amazon.co.jp',
'China' : 'https://www.amazon.cn',
'India' : 'https://www.amazon.in',
'Australia': 'https://www.amazon.com.au',
'Mexico' : 'https://www.amazon.com.mx',
'Brazil' : 'https://www.amazon.com.br',
'Turkey' : 'https://www.amazon.com.tr',
'UAE' : 'https://www.amazon.ae',
'Singapore' : 'https://www.amazon.sg',
'Netherlands' : 'https://www.amazon.nl',
'Saudi Arabia' : 'https://www.amazon.sa',}


# CSV Reader
def csv_read(csv_filename):
    with open(csv_filename, 'r' , encoding='utf-8') as csv_file:
        csv_reads = csv.reader(csv_file)
        rows = []
        for row in csv_reads:
            rows.append(row)

        return rows[1:]


# Changes The Zip Code
def zip_change(driver, base_url, zipcode):
    print('Changing The ZIP')
    try:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//a[@id="nav-global-location-popover-link"]/div[@id="glow-ingress-block"]/span[contains(., "{}")]'.format(zipcode.split(" ")[0].strip()),
                    )
                )
            )
        
            print('Zipcode is already entered, moving to next step..')
            return True
        except:
            try:
                driver.get(base_url)
                time.sleep(1)

                wait = WebDriverWait(driver, 10)
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav-global-location-popover-link"))).click()
                except:
                    pass

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#GLUXZipUpdateInput"))).clear()
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#GLUXZipUpdateInput"))).send_keys(zipcode)
                    time.sleep(1)
                except:
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#GLUXZipUpdateInput_0"))).clear()
                        time.sleep(1)
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#GLUXZipUpdateInput_0"))).send_keys(
                            zipcode.split(' ')[0].strip())
                        time.sleep(1)
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#GLUXZipUpdateInput_1"))).clear()
                        time.sleep(1)
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#GLUXZipUpdateInput_1"))).send_keys(
                            zipcode.split(' ')[-1].strip())
                        time.sleep(1)
                    except:
                        a = 1
                        pass
            except:
                pass

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#GLUXZipUpdate > span > input"))).click()
                time.sleep(2)
                driver.refresh()
                time.sleep(1)

            except:
                a = 1
                pass
            
            try:
                cookies_accept_button = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//form[@id = "sp-cc"]//span[contains(., "Accept Cookies")]',
                        )
                    )
                )
                
                ActionChains(driver).move_to_element(cookies_accept_button).click().perform()
            except:
                pass
            

            return True
    except:
        return False


# Wait Until The Chart And download The CSv
def csv_download(driver):
    # Wait until chart
    print('Wait until chart appears')
    chart_ele = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="h10-style-container"]:not([class])')))
    driver.execute_script("arguments[0].scrollIntoView();", chart_ele)
    print('2 sec interval')
    time.sleep(5)

    # Shadow Root
    shadow_chart = driver.execute_script("""return document.querySelector('[id="h10-style-container"]:not([class])').shadowRoot.querySelector("div")""")

    # Click on Last ALL TIME
    print('Click On ALL TIME')
    try:
        shadow_chart.find_element(By.CSS_SELECTOR, 'ul').find_elements(By.CSS_SELECTOR, 'li')[-1].click()
        time.sleep(3)
    except:
        time.sleep(2)
        shadow_chart.find_element(By.CSS_SELECTOR, 'ul').find_elements(By.CSS_SELECTOR, 'li')[-1].click()
        time.sleep(1)

    # Shadow Root click on three line
    driver.execute_script("""return document.querySelector('[id="h10-style-container"]:not([class])').shadowRoot.querySelector("[aria-label='View chart menu']")""").click()
    time.sleep(2)
    print('Click On download CSV')
    # Shadow Root click download CSV
    driver.execute_script("""return document.querySelector('[id="h10-style-container"]:not([class])').shadowRoot.querySelector("li[class='highcharts-menu-item']")""").click()
    time.sleep(2)


# CSV Delete IF already Exist
def del_gen_csv(gen_csv_file):
    if os.path.isfile(gen_csv_file):
        os.remove(gen_csv_file)


# Wait Until File downloaded
def wait_4_csv(gen_csv_file):
    time.sleep(2)
    while not os.path.exists(gen_csv_file):
        time.sleep(1)
    print(f"Downloaded >> {gen_csv_file}")
    time.sleep(1)

