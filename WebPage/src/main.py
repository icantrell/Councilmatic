# This program creates a web page
# Create by Howard Matis for OpenOakland - October 19, 2018
#
# Takes data scraped from Oakland Legistar web page - https://oakland.legistar.com/Calendar.aspx
#

import csv
from datetime import datetime, timedelta


def dateLessThanEqual(date1, date2):  # Compare whether deadline has passed
    datetime1 = datetime.strptime(date1, '%m/%d/%Y')
    datetime2 = datetime.strptime(date2, '%m/%d/%Y')
    return datetime1 <= datetime2


def create_html(url_open, fx):  # Read a template file and then write it main file
    in_file = open(url_open, 'r')
    page = in_file.read()
    fx.write(page)
    in_file.close()
    return


def read_csvfile(datafile, search_string, f2):
    data = list(csv.reader(open(datafile), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
    numrows = len(data)
    # numcolumns = len(data[0])
    citycouncil = search_string
    https = "https://"
    for i in range(numrows):

        if len(data[i][:]) >= 9:
            meeting = data[i][0]
            meeting = meeting.replace(" and ", " & ")  # must do this because non-standardization of Oakland
            if citycouncil in meeting:
                meeting_video = data[i][8]
                meeting_date = data[i][1]
                meeting_time = data[i][3]
                meeting_room = data[i][4]
                meeting_agenda = data[i][6]
                meeting_minutes = data[i][7]
                ecomment = data[i][9]

                if https in meeting_video:
                    link = meeting_video
                    link_text = "Click for Video Minutes and Agenda"
                elif https in meeting_minutes:
                    link = meeting_minutes
                    link_text = "Click for Minutes"
                elif https in meeting_agenda:
                    link = meeting_agenda
                    link_text = "Click for Agenda"
                else:
                    link = 'none'
                    link_text = 'none'

                present = datetime.now().strftime('%m/%d/%Y')
                agenda_deadline = datetime.strptime(meeting_date, '%m/%d/%Y') + timedelta(days=10)
                agenda_deadline = agenda_deadline.strftime('%m/%d/%Y')

                if dateLessThanEqual(present, meeting_date):
                    link_text = "Meeting at " + meeting_time + " in the " + meeting_room
                    write_http_row(f2, meeting_date, link, link_text, ecomment)
                elif dateLessThanEqual(agenda_deadline, present):
                    # 10 days have passed since meeting.  Only keep if have video minutes
                    if link_text == "Click for Video Minutes and Agenda":
                        # Need video minutes for this length of time
                        write_http_row(f2, meeting_date, link, link_text, "video")
                else:
                    # print out meeting details in preliminary time
                    write_http_row(f2, meeting_date, link, link_text, "video")


def write_http_row(f2, date, link, message, emessage):
    https = "https://"
    f2.write("\n")

    lineout = "<tr>"
    f2.write(lineout + "\n")

    lineout = "<td><span class=\nstyle1\n>" + date + "</span></td>"
    f2.write(lineout + "\n")

    if link == "none":
        lineout = '<td>' + message  # if no link omit it
    elif emessage == "video":
        lineout = '<td> <a href="' + link + '" target=\n_top">' + message
    else:
        lineout = '<td>' + message + " | "'<a href="' + link + '" target=\n_top">' + "Click for agenda"

    if https in emessage:       # to add e-comment
        lineout = lineout + " | " '<a href="' + emessage + '" target=\n_top">' + "Click to comment electronically"

    f2.write(lineout + "\n")

    lineout = '</a></td>'
    f2.write(lineout + "\n")

    lineout = "</tr>"
    f2.write(lineout + "\n")


#
# Write out a navigation bar
#
def make_navbar(type, list, year_list, committee_list, loop_type, loop_index, f2):
    #   write the top of navbar
    if type ==1:
        url = "template_navbar_top.txt"
    else:
        url = "template_navbar_top2.txt"
    create_html(url, f2)  # Create  template for HTML page
    #
    for index, item in enumerate(list):
        linenav = '<li class="nav-item">'
        f2.write(linenav + "\n")

        if loop_type:
           year_bar = str(year_list[loop_index])      # Looping over the committees so fixed year
           committee_bar = str(index)
        else:
            year_bar = str(year_list[index])           # Looping over the years so fixed committee
            committee_bar = str(loop_index)

        urlnavbar = '../' + year_bar + '/committee' + committee_bar + ".html" #looping over years
        linenav = '<a class="nav-link" href="' + urlnavbar + ' "href=#">' + item + '</a>'   #Problem may be here
        f2.write(linenav + "\n")

        f2.write("    </li>" + "\n")

    url = "template_navbar_bottom.txt"
    create_html(url, f2)  # Create  template for HTML page
    f2.write(" ")

#
# Main program
#


version = "3.1"
print(" ")
print("<------------------Running main.py – Version", version, "------------------>")
committees = ["City Council", "Rules & Legislation", "Public Works", "Life Enrichment", "Public Safety",
              "Oakland Redevelopment", "Community & Economic Development" , "Finance & Management"]
years = ["2018", "2017", "2016", "2015", "2014"]

for index_year, year in enumerate(years):
    for index, committee in enumerate(committees):
        print(year, committee)
        outfile = "../website/" + year + "/committee" + str(index) + ".html"
        f1 = open(outfile, 'w+')
        #
        #   write the top of the web page
        url = "template_top.txt"
        create_html(url, f1)  # Create  template for HTML page
        f1.write(" ")

        loop_committee = True # Loop over committees
        loop_index = index_year  # Fix the year
        make_navbar(1, committees, years, committees, loop_committee, loop_index, f1)

        #  write the top of the web page
        url = "template_above_table.txt"
        create_html(url, f1)  # Create  template for HTML page
        f1.write(" ")

        line = '<div align="center"><p><h3>' + committee + " - " + year + '</h3></p></div>'
        f1.write(line)

        url = "template_table_top.txt"
        create_html(url, f1)  # Write bottom of header file
        f1.write(" ")

        scraper_file = "../website/scraped/year" + str(year) + ".csv"
        read_csvfile(scraper_file, committees[index], f1)

        # write the bottom of the table
        url = "template_table_bottom.txt"
        create_html(url, f1)  # Create  template for HTML page
        f1.write(" ")

        # create the lower navigation bar
        loop_committee = False  # Loop over years
        loop_index = index  # Fix the year
        make_navbar(2, years, years, committees, loop_committee, loop_index, f1)

        # write the bottom of the web page
        url = "template_bottom.txt"
        create_html(url, f1)  # Create  template for HTML page
        f1.write(" ")

        f1.close()  # Close the file

print("<-----------------End of main.py--------------------–––––––––––>")

quit()
