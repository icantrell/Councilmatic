from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from .scraper import Scraper
from ..model.calendar import Calendar as CalendarModel

class Calendar(Scraper):
    def __init__(self, default_url='https://oakland.legistar.com/Calendar.aspx', wait=30, driver=None):
        super().__init__(default_url, wait, driver)    

    def get_search_input_elt(self, highlight=False, sleep_time=2):
        search_input_elt = self.driver.find_element(By.XPATH, "//input[@name='ctl00$ContentPlaceHolder1$txtSearch']")
        if highlight:
            self.highlight(search_input_elt, sleep_time=sleep_time)

        return search_input_elt     

    def get_dates(self):
        input_id = "ctl00_ContentPlaceHolder1_lstYears_Input"
        select_li_xpath_str = "//div[@id='ctl00_ContentPlaceHolder1_lstYears_DropDown']//ul[@class='rcbList']/li[@class='rcbItem']"

        return self.get_select_text(input_id, select_li_xpath_str)

    def set_date(self, date_str, sleep_time=1):
        input_id = "ctl00_ContentPlaceHolder1_lstYears_Input"
        select_xpath_str = "//div[@id='ctl00_ContentPlaceHolder1_lstYears_DropDown']//ul[@class='rcbList']/li[@class='rcbItem'][text() = '%s']" % date_str
        self.set_select_elt(input_id, select_xpath_str, sleep_time)

    def get_depts(self):
        input_id = "ctl00_ContentPlaceHolder1_lstBodies_Input"
        select_li_xpath_str = "//div[@id='ctl00_ContentPlaceHolder1_lstBodies_DropDown']//ul[@class='rcbList']/li[@class='rcbItem']"

        return self.get_select_text(input_id, select_li_xpath_str)   

    def set_dept(self, dept_name, sleep_time=10):
        input_id = "ctl00_ContentPlaceHolder1_lstBodies_Input"
        select_xpath_str = "//div[@id='ctl00_ContentPlaceHolder1_lstBodies_DropDown']//ul[@class='rcbList']/li[@class='rcbItem'][text() = '%s']" % date_str
        self.set_select_elt(input_id, select_xpath_str, sleep_time)

    def get_pagination_links(self, highlight=False, sleep_time=2):
        link_elts = self.driver.find_elements(By.XPATH,
            "//tr[@class='rgPager']//td[@class='NumericPages']/div[@class='rgNumPart']/a")

        if highlight:
            for link_elts in link_elts:
                self.highlight(link_elts, sleep_time=sleep_time)

        return link_elts

    def set_notes_ckbx(self, val=False):
        id_str = "ctl00_ContentPlaceHolder1_chkOptions_0"
        self.set_chbx(id_str, val)

    def set_closed_caption_ckbx(self, val=False):
        id_str = "ctl00_ContentPlaceHolder1_chkOptions_1"
        self.set_chbx(id_str, val)

    def wait_for_login_link(self, wait_time=10):
        self.wait_for(id_str="ctl00_hypSignIn", wait_time=wait_time)

    def query(self, search_str=None, date_sel=None, 
                dept=None, notes=False, closed_caption=False,
                sleep_time=5, wait_time=5):
        self.set_notes_ckbx(notes)
        self.set_closed_caption_ckbx(closed_caption)

        if date_sel is not None and date_sel != "":
            self.set_date(date_sel)     
            self.sleep(sleep_time)  
            self.wait_for_login_link(wait_time) 

        if search_str is not None and search_str != "":
            search_input_elt = self.get_search_input_elt()
            search_input_elt.send_keys(search_str)
            search_input_elt.submit()
            self.sleep(sleep_time)
            self.wait_for_login_link(wait_time) 
        
        return self.scrape_pages(sleep_time=sleep_time)

    def get_video_link(self, base_url, video_elt):
        if video_elt is None:
            return None

        link_elt = video_elt.find_element(By.TAG_NAME, 'a')
        if link_elt is None:
            return None

        onclick_str = link_elt.get_attribute('onclick')
        if onclick_str is None or onclick_str == "":
            return None 

        video_links = re.findall(r"'(.*?)'",  onclick_str)
        if video_links is None or len(video_links) == 0:
            return None

        return "%s%s" % (base_url, video_links[0])

    def _scrape_page(self):
        calendar_list = []

        #find div that holds table with events info and extract the rows of the table.
        rows = self.driver.find_elements(By.XPATH, 
                    "//div[@id='ctl00_ContentPlaceHolder1_divGrid']//table[@class='rgMasterTable']/tbody/tr[@class='rgRow']")

        for row in rows:
            #get each column of the row
            cols = row.find_elements(By.XPATH, 'td')

            # extract data
            name = cols[0].text
            meeting_date = cols[1].text

            calendar_link = self.elt_get_href(cols[2])

            meeting_time = cols[3].text

            meeting_location = cols[4].text
            meeting_details = self.elt_get_href(cols[5])
            agenda = self.elt_get_href(cols[6])
            minutes = self.elt_get_href(cols[7])

            video = self.get_video_link(self.base_url, cols[8])
            eComment = self.elt_get_href(cols[9])
            
            #create calendar event data storage object.
            calendar = CalendarModel(
                name, meeting_date, calendar_link, 
                meeting_time, meeting_location, 
                meeting_details, agenda, 
                minutes, video, eComment)
            #add to event list
            calendar_list.append(calendar)

        return calendar_list        

    def scrape_page(self, num_of_retries=3, sleep_time=3):
        return self.retry(
            fnc=self._scrape_page, 
            num_of_retries=num_of_retries,
            sleep_time=sleep_time,
            err_msg="Scaping page failed"
        )

    def go_to_cal_page(self):
        self.get(self.default_url)

    def run(self):
        self.go_to_cal_page()

        #calendar_list = self.query(search_str="lead", date_sel="2018", notes=True)
        #calendar_list = self.query(date_sel="2018")
        calendar_list = self.query(date_sel="2018", closed_caption=True)

        cl_json = CalendarModel.to_map_list_json(calendar_list)

        print(cl_json)

def main():
    cal = Calendar()
    cal.run()
    cal.close()

if __name__ == "__main__":
    main()