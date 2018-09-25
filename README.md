# Councilmatic

# Setup

1. Install Anaconda 
  * https://www.anaconda.com/download
2. Create conda env
  * conda env create -f environment.yml
3. Download geckodriver and add to path
  * https://github.com/mozilla/geckodriver/releases
note: We used Katalon IDE brower plugin to generate some of python selenium statements the normal selenium IDE no longer supports Python code exports.
  
# start up conda env
```
source activate new_councilmatic
```

# To run:
```
PYTHONPATH=. python scraper/calendar.py 
```

# Milestones:
1. to have a web scraping library.
  * scraping from https://oakland.legistar.com/Calendar.aspx.
  * need to scrape data from the city council table, city council events(aka city meetings, the calendar page) table and the legislation page.
  * scrapers inherit from the scraper class and use selenium to naviagate to the pages, which might require javascript and access web content inside tables on the page.
  * store in models(that are decoupled from DB).
  <br>
 next milestones...
 might want to have some kind of user interface.(note: almost done with the first milestone)

