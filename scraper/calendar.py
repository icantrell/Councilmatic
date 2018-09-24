from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from scraper import Scraper
from model.calendar import Calendar as CalendarModel

class Calendar(Scraper):
    def __init__(self, base_url='https://oakland.legistar.com/Calendar.aspx', wait=30, driver=None):
        super().__init__(base_url, wait, driver)    

    def run(self):
        self.get(self.base_url)

        calendar_list = []

        #find div that holds table with events info and extract the rows of the table.
        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_divGrid']//tbody/tr")

        for i, row in enumerate(rows):
            print(i, str(row))
            #get each column of the row
            cols = row.find_elements(By.XPATH, 'td')

            #extract data.
            name = cols[0].text
            meeting_date = cols[1].text

            calendar_link = self.elt_get_href(cols[2])

            meeting_time = cols[3].text

            meeting_location = cols[4].text
            meeting_details = self.elt_get_href(cols[5])
            agenda = self.elt_get_href(cols[6])
            minutes = self.elt_get_href(cols[7])
            video = self.elt_get_href(cols[8])
            eComment = self.elt_get_href(cols[9])

            print("name: ", name)
            print("meeting_date: ", meeting_date)
            print("calendar_link: ", calendar_link)
            print("meeting_time: ", meeting_time)
            print("meeting_location: ", meeting_location) 
            print("meeting_details: ", meeting_details)
            print("agenda: ", agenda)
            print("minutes: ", minutes)
            print("video: ", video)
            print("eComment: ", eComment)
            
            #create calendar event data storage object.
            calendar = CalendarModel(name, meeting_date, calendar_link, 
                                        meeting_time, meeting_location, 
                                        meeting_details, agenda, 
                                        minutes, video, eComment)
            #add to event list
            calendar_list.append(calendar)
        #turn to json
        cl_json = CalendarModel.to_map_list_json(calendar_list)

        print(cl_json)

def main():
    cal = Calendar()
    cal.run()
    cal.close()

if __name__ == "__main__":
    main()