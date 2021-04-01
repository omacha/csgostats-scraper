import pickle
from time import sleep
from os.path import exists as file_exists

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def init_browser(url):
    browser = webdriver.Firefox()

    if file_exists('cookies.pkl'):
        browser.get(url)
        with open('cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                browser.add_cookie(cookie)

    return browser


def destroy_browser(browser):
    cookies = browser.get_cookies()
    with open("cookies.pkl", "wb") as wbf:
        pickle.dump(cookies, wbf)
    sleep(5)
    browser.close()


def make_request(browser, url, locator, delay=3):
    if browser.current_url != url:
        browser.get(url)

    try: 
        WebDriverWait(browser, delay).until(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        if len(browser.find_elements_by_class_name("challenge-form")) > 0:
            print("Cloudflare detected")
            while len(browser.find_elements_by_class_name("challenge-form")) > 0:
                sleep(0.5)
            print("Cloudflare test passed")
            return make_request(browser, url, locator, delay)
        else:
            print("Loading took too much time for ", url)
            return False
