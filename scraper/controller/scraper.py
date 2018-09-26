from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Scraper(object):
    def __init__(self, base_url, wait=30, driver=None):
        self.base_url = base_url
        self.wait_time = wait
        if driver is None:
            # default to firefox
            self.driver = webdriver.Firefox()
        else:
            self.driver = driver
        
        self.driver.implicitly_wait(wait)

    def elt_get_href(self, elt):
        try:
            link_elt = elt.find_element(By.TAG_NAME, 'a')
            return link_elt.get_attribute('href')
        except:
            return None

    """
    modified from https://gist.github.com/dariodiaz/3104601
    """
    def highlight(self, element, sleep_time=0.3):
        """Highlights (blinks) a Selenium Webdriver element"""
        parent = element._parent
        def apply_style(s):
            parent.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element, s)
        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        time.sleep(sleep_time)
        apply_style(original_style)

    def get(self, url):
        self.driver.get(url)

    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def wait(self):
        self.driver.implicitly_wait(self.wait_time)



