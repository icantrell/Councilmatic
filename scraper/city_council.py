from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from scraper import Scraper
from model.city_council import CityCouncil as CityCouncilModel

class CityCouncil(Scraper):
    def __init__(self, base_url='https://oakland.legistar.com/Calendar.aspx', wait=30, driver=None):
        #Started selenium on legistar calendar webpage. Since the city council page generates an ID for the url
        #and I am not sure that the ID is persistent or changing.
        super().__init__(base_url, wait, driver)    

    def run(self):
        #do a GET request to base url.
        self.get(self.base_url)
        #go to city council page
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Calendar'])[1]/following::span[3]").click()

        #click on "people" button
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Calendar (0)'])[1]/following::span[3]").click()
        #wait for load
        self.wait()

        city_council_list = []
        
        #find div that holds table with council members info and extract the rows of the table.
        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_gridPeople']/table/tbody/tr")

        for i, row in enumerate(rows):
            print(i, str(row))
            #get each column of the row.
            cols = row.find_elements(By.TAG_NAME, 'td')

            #extract data
            name = cols[0].text
  
            title = cols[1].text
            
            start_date = cols[2].text

            end_date = cols[3].text

            email = cols[4].text
            website = cols[5].text
            appointed_by = cols[6].text

            print("name: ", name)
            print("title: ", title)
            print("start_date: ", start_date)
            print("end_date: ", end_date) 
            print("email: ", email)
            print("website: ", website)
            print("appointed_by ", appointed_by)

            #create data storage object
            city_council = CityCouncilModel(name, title, start_date, 
                                        end_date, email, 
                                        website, appointed_by)

            city_council_list.append(city_council)

        #turn to json
        cl_json = CityCouncilModel.to_map_list_json(city_council_list)

        print(cl_json)

def main():
    cc = CityCouncil()
    cc.run()
    cc.close()

if __name__ == "__main__":
    main()