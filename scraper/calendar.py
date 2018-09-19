from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from scraper import Scraper
#from ..model import Calendar as CalendarModel

class Calendar(Scraper):
    def __init__(self, wait=30, driver=None):
        super().__init__(wait, driver)

    def run(self):
        url = 'https://oakland.legistar.com/Calendar.aspx'
        self.get(url)

        rows = self.driver.find_elements(By.XPATH, '//tbody/tr')

        for i, row in enumerate(rows):
            print(i, str(row))
            cols = row.find_elements(By.XPATH, 'td')
            for j, col in enumerate(cols):
                print(j, col.text)

def main():
    cal = Calendar()
    cal.run()
    cal.close()

if __name__ == "__main__":
    main()