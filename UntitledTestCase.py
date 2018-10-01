# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("https://oakland.legistar.com/Calendar.aspx")
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Arrow").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='All Years'])[1]/following::li[1]").click()
        #driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Input").send_keys("2018")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='All Years'])[1]/following::li[2]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Input").send_keys("2017")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='All Years'])[1]/following::li[3]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstYears_Input").send_keys("2016")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='All Departments'])[1]/following::li[1]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").send_keys("* Concurrent Meeting of the Joint Powers Financing Authority and Finance and Management Committee")
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Arrow").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='* Concurrent Meeting of the Joint Powers Financing Authority and Finance and Management Committee'])[1]/following::li[1]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").send_keys("* Concurrent Meeting of the Oakland Redevelopment Successor Agency and the City Council")
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Arrow").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='* Concurrent Meeting of the Oakland Redevelopment Successor Agency and the City Council'])[1]/following::li[2]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").send_keys("* Special Concurrent Meeting of the Oakland Redevelopment Successor Agency and Finance and Management Committee")
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Arrow").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='* Concurrent Meeting of the Joint Powers Financing Authority and Finance and Management Committee'])[1]/preceding::li[1]").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").clear()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_lstBodies_Input").send_keys("All Departments")
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_chkOptions_1").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
