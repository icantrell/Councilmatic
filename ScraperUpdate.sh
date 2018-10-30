#!/usr/bin/env bash
#
# Update CSV Database - To be run be a cron job daily
#
# Written by Howard Matis - October 30, 2018
#
# This script only works on Mac OSX (BSD)
# The command "date" is different depending on flavor of UNIX
# In December the script will run the script for next year;  In January the script will run the previous year.
#
# ------------------------------------------------------------------
#
cd /Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic  #This is installation dependent


LASTYEAR=`date -v-1y  +"%Y"`
CURRENTYEAR=`date +"%Y"`
NEXTYEAR=`date -v+1y  +"%Y"`
CURRENTMONTH=`date +"%m"`
#
#Get a list of current dates
#
python run_calendar.py --show_dates >> temp.tmp
#
# Scrape the current year if it exists
#
if `grep -q "$CURRENTYEAR" "temp.tmp"`; then
    echo "Processing Current Year Scraper File"
    python run_calendar.py -d "$CURRENTYEAR"  > WebPage/website/scraped/year"$CURRENTYEAR".csv
fi
#
# Check if December
#
if [ "$CURRENTMONTH" == "12" ];then
    if `grep -q "$NEXTYEAR" "temp.tmp"`; then
        echo "December - Processing Next Year"
        python run_calendar.py -d "$NEXTYEAR"  > WebPage/website/scraped/year"$NEXTYEAR".csv
    else
        echo "Next year file not ready"
    fi
elif [ "$CURRENTMONTH" == "1" ];then
    if `grep -q "$LASTYEAR" "temp.tmp"`; then
        echo "Current month is January - Processing Last Year"
        python run_calendar.py -d "$LASTYEAR"  > WebPage/website/scraped/year"$LASTYEAR".csv
    else
        echo "Previous Year not available"
    fi
else
    echo "No need to process adjacent year"
fi
#
# Now make the webpage
#
cd Webpage
cd src
python main.py   #Run the main program
python sidebar.py #Get the sidebar

echo "Program completed"
#