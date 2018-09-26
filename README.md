# Councilmatic

# Setup

1. Install Anaconda 
  * https://www.anaconda.com/download
2. Create conda env
  * conda env create -f environment.yml
3. Download geckodriver and add to path
  * https://github.com/mozilla/geckodriver/releases
  <br>
note: We used Katalon IDE brower plugin to easy generate some of python selenium statements the normal selenium IDE no longer supports Python code exports.
  
# start up conda env
```
source activate new_councilmatic
```

# update conda env
```
source activate new_councilmatic
conda env update -f=environment.yml
```

# install conda env into jupyter notebook
```
source activate new_councilmatic
python -m ipykernel install --user --name new_councilmatic --display-name "new councilmatic"
```

# To run:
```
python run_calendar.py 
```

# To run in jupyter notebook
```
jupyter notebook calendar.ipynb
``

# Milestones:
1. to have a web scraping library.
  * scraping from https://oakland.legistar.com/Calendar.aspx.
  * need to scrape data from the city council table, city council events(aka city meetings, the calendar page) table and the legislation page.
  * scrapers inherit from the scraper class and use selenium to naviagate to the pages, which might require javascript and access web content inside tables on the page.
  * store in models(that are decoupled from DB).
  <br>
 next milestones...
 might want to have some kind of user interface.(note: almost done with the first milestone)

