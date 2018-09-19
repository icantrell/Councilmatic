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

    def get(self, url):
        self.driver.get(url)

    def close(self):
        try:
            self.driver.quit()
        except:
            pass


