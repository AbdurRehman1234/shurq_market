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


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-1])
scripts = os.path.join(parent_dir, "scripts")
localhost = os.path.join(parent_dir, "localhost")
if not os.path.exists(localhost):
    os.mkdir(localhost)


class BrowserDefine:
    """Representing of the selenium webdriver and open the chrome browser"""

    # Download chromedriver
    def chrome_driver_download(self):
        print(f'Step 1- Current Chrome Browser Version : {chromedriver_autoinstaller.get_chrome_version()}')
        print(f'Step 2- Chrome Driver finding / downloading')
        self.chromedriver = chromedriver_autoinstaller.install()

    # Chrome Browser openning in port 9555
    def chrome_open(self):
        print(f'Step 4- Current Working Directory: {parent_dir}')

        # Chrome Browser Select From C Drive
        if os.path.exists(r'C:\Program Files\Google\Chrome\Application\chrome.exe'):
            chrome_dir = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        elif os.path.exists(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
            chrome_dir = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        print(f'Step 5- Chrome Browser Install at: {chrome_dir}')

        # Chrome Browser Open in Local Host
        print('Step 6- Chrome Browser opening...........')
        subprocess.Popen(f'{chrome_dir} --remote-debugging-port=9555 --user-data-dir={localhost}')

    #  Define Driver Object with link of port
    def connexion_to_website(self):
        option = Options()
        option.add_experimental_option("debuggerAddress", f"localhost:9555")
        s = Service(self.chromedriver)
        driver = webdriver.Chrome(service=s, options=option)
        driver.maximize_window()
        print('Step 7- Chrome Browser Link with Selenium')
        return driver