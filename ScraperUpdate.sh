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
# This run using cron
#   0 2 * * * /Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic/ScraperUpdate.sh
#
# ------------------------------------------------------------------
#
#   This is machine dependant
#
DIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic
CRONDIR=/Users/matis/Documents/OpenOakland/Councilmatic-master/Councilmatic/WebPage/website/logs
#
CRONLOG=$CRONDIR/scraperupdate.log
#
cd $DIR
LASTYEAR=`date -v-1y  +"%Y"`
CURRENTYEAR=`date +"%Y"`
NEXTYEAR=`date -v+1y  +"%Y"`
CURRENTMONTH=`date +"%m"`
VERSION="1.1"
#
#Get a list of current dates
#
echo "Version "$VERSION" of ScraperUpdate.sh" > $CRONLOG				#Clear cron log file

python run_calendar.py --show_dates > $CRONDIR/temp.tmp
#
# Scrape the current year if it exists
#
if `grep -q "$CURRENTYEAR" "$CRONDIR/temp.tmp"`; then
    echo "Processing current year scraper file"  >> $CRONLOG
    python run_calendar.py -d "$CURRENTYEAR"  > WebPage/website/scraped/year"$CURRENTYEAR".csv
fi
#
# Check if December
#
if [ "$CURRENTMONTH" == "12" ];then
    if `grep -q "$NEXTYEAR" "$CRONDIR/temp.tmp"`; then
        echo "December - Processing next year"  >> $CRONLOG
        python run_calendar.py -d "$NEXTYEAR"  > WebPage/website/scraped/year"$NEXTYEAR".csv
    else
        echo "Next year file not ready" >> $CRONLOG
    fi
elif [ "$CURRENTMONTH" == "1" ];then
    if `grep -q "$LASTYEAR" "$CRONDIR/temp.tmp"`; then
        echo "Current month is January - Processing last year"
        python run_calendar.py -d "$LASTYEAR"  > WebPage/website/scraped/year"$LASTYEAR".csv
    else
        echo "Previous year not available" >> $CRONLOG
    fi
else
    echo "No need to process any adjacent year" >> $CRONLOG
fi
#
# Now make the webpage
#
cd Webpage
cd src
python main.py  >> $CRONLOG #Run the main program
python sidebar.py  >> $CRONLOG #Get the sidebar

echo " " >> $CRONLOG
echo "ScraperUpdate.sh completed"  >> $CRONLOG
#