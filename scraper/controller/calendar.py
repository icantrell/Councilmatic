from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
import unittest, time, re

from .scraper import Scraper
from ..model.calendar import Calendar as CalendarModel

class Calendar(Scraper):
    def __init__(self, base_url='https://oakland.legistar.com/Calendar.aspx', wait=30, driver=None):
        super().__init__(base_url, wait, driver)    

    def get_search_input_elt(self, highlight=False, sleep_time=2):
        search_input_elt = self.driver.find_element(By.XPATH, "//input[@name='ctl00$ContentPlaceHolder1$txtSearch']")
        if highlight:
            self.highlight(search_input_elt, sleep_time=sleep_time)

        return search_input_elt

    def get_date_sel_elt(self, highlight=False, sleep_time=2):
        date_sel_elt = self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstYears_Input')
        if highlight:
            self.highlight(date_sel_elt, sleep_time=sleep_time)

        return date_sel_elt

    def get_notes_ckbx(self):
        return self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_chkOptions_0')

    def get_closed_caption_ckbx(self):
        return self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_chkOptions_1')

    def get_pagination_links(self, highlight=False, sleep_time=2):
        link_elts = self.driver.find_elements(By.XPATH,
            "//tr[@class='rgPager']//td[@class='NumericPages']/div[@class='rgNumPart']/a")

        if highlight:
            for link_elts in link_elts:
                self.highlight(link_elts, sleep_time=sleep_time)

        return link_elts

    def query(self, search_str=None, date_sel=None, 
                dept=None, notes=False, closed_caption=False,
                sleep_time=10):
        self.get(self.base_url)

        if search_str is not None and search_str != "":
            search_input_elt = self.get_search_input_elt()
            search_input_elt.send_keys(search_str)
            search_input_elt.submit()
            time.sleep(sleep_time)

        if date_sel is not None and date_sel != "":
            date_sel_elt = Select(self.get_date_sel_elt())
            date_sel_elt.select_by_visible_text(date_sel)
            time.sleep(sleep_time)
        
        return self.scrape_page()

    def scrape_page(self):
        calendar_list = []

        #find div that holds table with events info and extract the rows of the table.
        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_divGrid']//tbody/tr")

        for i, row in enumerate(rows):
            #print(i, str(row))
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

            """
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
            """
            
            #create calendar event data storage object.
            calendar = CalendarModel(name, meeting_date, calendar_link, 
                                        meeting_time, meeting_location, 
                                        meeting_details, agenda, 
                                        minutes, video, eComment)
            #add to event list
            calendar_list.append(calendar)

        return calendar_list        

    def run(self):
        calendar_list = self.query(search_str="lead")

        cl_json = CalendarModel.to_map_list_json(calendar_list)

        print(cl_json)

def main():
    cal = Calendar()
    cal.run()
    cal.close()

if __name__ == "__main__":
    main()