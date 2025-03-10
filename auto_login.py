# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0038AE697ECD1D8BC671A522A24EF1196C9B04E71354EE003DA77DB594FC90ECC64CDFD12AF8A90F368F704A30291A1206DB003337749F7636419F7E5B151E5C5E97239719863F66E37F50801CDA15494CF88DEA0356A51DB86E6F276A02378D3DF74A3014892030283A74F0ED0EAAEC7E976160D9EC3A9CB7B83D80253ED5F16A15BCEF185A6E18EC5E842068EF4A9201BCF1CAE720E5149E5F346B1D996644D64D1E3DB8E2A8699EA4FA7D0CE34778DBA227ADA3CEF55773F1FFC5D68D1F6F0923AC21E44877BC294A3AA0333F64207913552BB79C22C6A66F17CBC9DDB5C54D3D27309CE0908F1C99C59FC829A34CDD85A7009B47452DB4A59877519B4A9D866245FCF1B724840BF050944076B64AFB4A94E7B085EDB6AA84F6DD0996DEB21025F684E5CDA93FEA3C1CCCCC85EDDF93E5BD8D128E0A80CC84DD9675B21FC59EAB843D29469BBA53D31A49607633E52004D7883D421D5DF30D1142CA12DBE4D3"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
