# This program creates a sidebar for Councilmatis
# Create by Howard Matis for OpenOakland - October 23, 2018
#
# Takes data scraped from Oakland Legistar web page - https://oakland.legistar.com/Calendar.aspx
#

import csv
from datetime import datetime, timedelta
import calendar


def read_csv_file(datafile, elements):
    data = list(csv.reader(open(datafile), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
    numrows = len(data)
    present = datetime.now()
    today = present.strftime('%m/%d/%Y')

    for i in range(numrows):        # Find out which meetings have not occurred
        if i > 0:                   # Don't read headers
            if len(data[i][:]) >= 8:
                meeting_date = data[i][1]
                future_meeting = meeting_date >= today
                if not future_meeting:
                    break
                elements.append([])
                for j in range(0, 5):
                    elements[i-1].append(0)
                    elements[i-1][j] = data[i][j]


def write_day_header(f2, day1, day2):
    f2.write('<div class="calendar_plan">' + "\n")
    f2.write('<div class="cl_plan">' + "\n")
    f2.write('<div class="cl_title"> <font size="+1">' + day1 + '</font> </div>' + "\n")
    f2.write('<div class="cl_copy">' + day2 + '</div>' "\n")
    f2.write('</div>' + "\n")
    f2.write('</div>' + "\n")


def write_event_header(f2, time_event, link_calendar, name_committee, name_location):
    f2.write('<div class="event_item">' + "\n")
    f2.write('<div class="ei_Dot"></div>' + "\n")
    f2.write('<div class="ei_Title">' + time_event + "\n")
    f2.write('<a href="' + link_calendar + '">' + "\n")
    f2.write('<img border="0" alt="calendar link" src="../images/ical.gif" width="15" height="15"> </a></div>' + "\n")
    f2.write('<div class="ei_Copy"> <font size="+1">' + name_committee + '</font> <br/> ' + name_location + "\n")
    f2.write('</div>' + "\n")
    f2.write('</div>' + "\n")
    f2.write(' ' + "\n")


version = "2.0"
lookAhead = 14  # Number of the days to look ahead for meetings

print(" ")
print("Running Software Version ", version, " - sidebar.py ")
print(" ")

outfile = "../website/html/dynamic_calendar.html"
f1 = open(outfile, 'w+')

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year

# Check if close to a new year

if currentMonth == 12:     # See if need to look at next year's record
    if currentDay > 31 - lookAhead:
        years = [str(currentYear + 1), str(currentYear)]  # Allows reading later file first
    else:
        years = [str(currentYear)]
else:
    years = [str(currentYear)]


schedule = []
for year in years:
    scraper_file = "../website/scraped/year" + str(year) + ".csv"
    print(scraper_file)

    read_csv_file(scraper_file, schedule)


numrows = len(schedule)

today = datetime.now()
lastdate = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
today_day = str(today.month) + '/' + str(today.day) + '/' + str(today.year)
tomorrow_day = str(tomorrow.month) + '/' + str(tomorrow.day) + '/' + str(tomorrow.year)
for i in range(numrows-1, 0, -1):
    event_day = schedule[i][1]
    if lastdate != event_day:
        lastdate = event_day
        new_day = True
    else:
        new_day = False

    if new_day:
        day_datetime = datetime.strptime(event_day, '%m/%d/%Y')
        day_label = datetime.date(day_datetime).weekday()
        day_of_week = calendar.day_name[day_label]
        if event_day == today_day:
            day_of_week = "Today"
        elif event_day == tomorrow_day:
            day_of_week = "Tomorrow"

        print(event_day)
        print("New Day")
        write_day_header(f1,day_of_week, event_day)

    committee = schedule[i][0]
    if "City Council" in committee:
        committee = "City Council - (" + committee + ")"
    print("Meeting description")
    print(committee)  # Committee
    print(schedule[i][2])  # Calendar
    print(schedule[i][3])  # Time
    print(schedule[i][4])  # Room
    write_event_header(f1, schedule[i][3], schedule[i][2], committee, schedule[i][4])

f1.close()  # Close the file
print("End of sidebar.py")

quit()
