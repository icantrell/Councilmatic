from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Scraper(object):
    def __init__(self, wait=30, driver=None):
        if driver is None:
            # default to firefox
            self.driver = webdriver.Firefox()
        else:
            self.driver = driver
        
        self.driver.implicitly_wait(wait)

    def get(self, url):
        self.driver.get(url)

    def close(self):
        try:
            self.driver.quit()
        except:
            pass


