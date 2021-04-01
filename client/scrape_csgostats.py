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

    if browser is None:
        players = [
            Player("76561198039683050", "omacha"), 
            Player("76561198076430753", "pit_phil")
        ]
        
        for p in players:
            matches = get_match_list_for_userid(browser, p.id)
            for m in matches:
                get_match(browser, m)
    else:
        print("browser is not defined")
except Exception:
    raise
finally:
    destroy_browser(browser)
    browser = None
