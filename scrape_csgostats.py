from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from csgostats_net import *
from csgostats import *

try:
    browser = init_browser("https://csgostats.gg/")

    if browser != None:
        matches = get_match_list_for_userid(browser, "76561198039683050")

        idx = 0
        for m in matches:
            get_match(browser, m)

            idx += 1
    else:
        print("browser is not defined")
except Exception:
    raise
finally:
    destroy_browser(browser)
    browser = None