#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       LaTeX planner generator
#       planner.py
#
#       To be used with a full install of LaTeX. Guide for use at
#       http://bkanuka.com/2011/11/custom-planner/ ‎
#       
#       Copyright 2011 Bennett Kanuka <bkanuka@gmail.com>
#
#
#       This work is licensed under a Creative Commons 
#       Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#       
#       The full text of the lisence can be found at 
#       http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode
#
#
#



JALALI = False

if JALALI:
    import jdatetime as datetime
else:
    import datetime

WEEKSTOPRINT = 54

def monthCal(bdate):
    """Returns a single month calendar with current week highlighted.
    Calendars will include the last few days of the last month,
    and a few days of the next month, in gray, for easy reference"""
    currmonth=bdate.month
    curryear=bdate.year
    currday=bdate.day
    currdate=bdate
    #bdate will be the "working" date in this function, and currdate will be 
    #the original function input. currdate wont change in this function.
    
    #set bdate back to the first of the month
    bdate=datetime.date(curryear, currmonth, 1)

    #weektick will count the total number of weeks in this calendar.
    #We want all calendars to have 6 weeks so they are all the same size
    weektick=0
    
    #start a table with spaces separating elements
    calstring='\\begin{tabular}\n{@{}c@{ }c@{ }c@{ }c@{ }c@{ }c@{ }c@{}}\n'
    
    #print the month name across the top of the cal
    calstring+=('\\multicolumn{7}{c}{\\textbf{%s}}\\\\ \n' % bdate.strftime("%B"))
    
    #followed by the days of the week, and a line
    if JALALI:
        for day in bdate.j_weekday_short[::-1][:-1]:
            calstring += day
            calstring += r' & '
        calstring += bdate.j_weekday_short[::-1][-1]
        calstring += "\\\\ \n"
    else:
        calstring+='S & M & T & W & T & F & S\\\\ \n'
    
    calstring+='\\hline \n' 
    
    #move bdate to the last sunday
    while bdate.weekday() > 0:
        bdate = bdate - datetime.timedelta(days=1)
    
    bdate = bdate - datetime.timedelta(days=1)
    
    #if currdate is within the next 7 days of this bdate, this week needs to
    #be highlighted
    if currdate.toordinal()-bdate.toordinal() < 7:
        #the .8 here is the shade of gray - 1 being white. read CTAN page on rowcolor.
        #I also tell LaTeX to extend the gray box by 2pt around each number.
        #There can be issues like the gray covering an adjacent number
        calstring+='\\rowcolor[gray]{.8}[2pt][2pt]'
        
    weeklist = []
    #while we're still on last month, print in gray
    while bdate.month==advancemonth(datetime.date(curryear, currmonth, 1),-1).month:
        weeklist.append('\\textcolor{dark-gray}{%s}' % bdate.day)
        #if we get to the end of the week, skip a line and weektick
        if len(weeklist)==13:
            if JALALI:
                weeklist = weeklist[::-1]
            calstring+=' '.join(weeklist)
            calstring+='\\\\ \n'
            weektick+=1
            weeklist = []
        #else, just skip columns
        else:
            weeklist.append('&')
        #move to next day
        bdate = bdate + datetime.timedelta(days = 1)
    

    while bdate.month==currmonth:
        weeklist.append('%s' % bdate.day)
        if len(weeklist)==13:
            if JALALI:
                weeklist = weeklist[::-1]
            calstring+=' '.join(weeklist)
            calstring+='\\\\ \n'
            weektick+=1
            weeklist = []
            if currdate.toordinal() < bdate.toordinal()+8 and currdate.toordinal() > bdate.toordinal():
                calstring+='\\rowcolor[gray]{.8}[2pt][2pt]'
        else:
            weeklist.append('&')
        bdate = bdate + datetime.timedelta(days = 1)
    

    while weektick < 6:
        weeklist.append('\\textcolor{dark-gray}{%s}' % bdate.day)
        if len(weeklist)==13:
            if JALALI:
                weeklist = weeklist[::-1]
            calstring+=' '.join(weeklist)
            calstring+='\\\\ \n'
            weektick+=1
            weeklist = []
        else:
            weeklist.append('&')
        bdate = bdate + datetime.timedelta(days = 1)
        
    calstring+='\\end{tabular}'
    return calstring

def colorday(bdate, lastmonth, currmonth, nextmonth):
    if bdate.month == currmonth:
        return '\\textbf{%s}' % bdate.day
    elif bdate.month == lastmonth or bdate.month == nextmonth:
        return '\\textcolor{Gray}{%s}' % bdate.day
    else:
        return ' '

def colormonth(bdate, lastmonth, currmonth, nextmonth):
    if bdate.month == currmonth:
        return '\\multirow{5}{*}{\\begin{sideways}\\textbf{%s}\\end{sideways}}\\\\ \n' % bdate.strftime("%B")
    elif bdate.month == lastmonth:
        return '\\multirow{5}{*}{\\begin{sideways}\\textcolor{Gray}{~~~~%s}\\end{sideways}}\\\\ \n' % bdate.strftime("%B")
    elif bdate.month == nextmonth:
        return '\\multirow{5}{*}{\\begin{sideways}\\textcolor{Gray}{%s~~~~}\\end{sideways}}\\\\ \n' % bdate.strftime("%B")


def monthlyPage(bdate):
    """Prints a page in between months"""
    currmonth=bdate.month
    curryear=bdate.year
    currday=bdate.day
    currdate=bdate
    
    lastmonth=advancemonth(datetime.date(curryear, currmonth, 1),-1).month
    nextmonth=advancemonth(datetime.date(curryear, currmonth, 1),1).month
    
    #bdate will be the "working" date in this function, and currdate will be 
    #the original function input. currdate wont change in this function.
    
    #set bdate to the first of last month
    bdate=advancemonth(datetime.date(curryear, currmonth, 1),-1)
    
    calstring='\n'
    calstring+='\\LARGE{}\n\n'
    
    calstring+='\\vspace*{\\fill}\n\n'
    
    #start a table with spaces separating elements

    #this is a special table that is textwidth. the 215pt starts the table far to the right.
    #the 38pt is the separation between sunday's date and the month name (written sideways)
    calstring+='\\begin{tabular*}{\\textwidth}[p]{@{\hspace{215pt}}c@{ }c@{ }c@{ }c@{ }c@{ }c@{ }c@{\\extracolsep{38pt}}l}\n'
    
    #followed by the days of the week
    calstring+='S & M & T & W & T & F & S &\\\\ \n'
    
    #this is a fancy line
    calstring+='\\cline{1-7}\n'  
    

    weeklist = []
        
    print bdate
    for ii in range(bdate.weekday()+1):
        weeklist.append('~')
        weeklist.append('&')

    while len(weeklist) < 13:
        weeklist.append(colorday(bdate, lastmonth, currmonth, nextmonth))
        weeklist.append('&')
        bdate = bdate + datetime.timedelta(days = 1)

    weeklist.append(colormonth(bdate, lastmonth, currmonth, nextmonth))
    print weeklist
    calstring+=' '.join(weeklist)
    weeklist = []

    while bdate.month == lastmonth:
        while len(weeklist) < 13:
            weeklist.append(colorday(bdate, lastmonth, currmonth, nextmonth))
            weeklist.append('&')
            bdate = bdate + datetime.timedelta(days = 1)

        if bdate.month == lastmonth:
            weeklist.append('\\\\ \n')
        else:
            weeklist.append(colormonth(bdate, lastmonth, currmonth, nextmonth))
        calstring+=' '.join(weeklist)
        print weeklist
        weeklist = []

    while bdate.month == currmonth:
        while len(weeklist) < 13:
            weeklist.append(colorday(bdate, lastmonth, currmonth, nextmonth))
            weeklist.append('&')
            bdate = bdate + datetime.timedelta(days = 1)

        if bdate.month == currmonth:
            weeklist.append('\\\\ \n')
        else:
            weeklist.append(colormonth(bdate, lastmonth, currmonth, nextmonth))
        calstring+=' '.join(weeklist)
        print weeklist
        weeklist = []
    
    while bdate.month == nextmonth:
        while len(weeklist) < 13:
            weeklist.append(colorday(bdate, lastmonth, currmonth, nextmonth))
            weeklist.append('&')
            bdate = bdate + datetime.timedelta(days = 1)

        weeklist.append('\\\\ \n')
        calstring+=' '.join(weeklist)
        print weeklist
        weeklist = []
        
    calstring+='\n\\end{tabular*}\n\n'
    
    calstring+='\\vspace*{\\fill}\n\n\\normalsize{}\n\n\\newpage\n\n'
    
    return calstring

def advancemonth(bdate, nmonths):
    """Advance date by nmonths. Takes a date object and an integer.
    The math here is a little nasty if you dont know mod, and
    probably equally nasty if you DO know mod. But it works."""
    
    if nmonths == 0:
        return bdate

    month = bdate.month - 1 + nmonths
    if nmonths < 0:
        year = bdate.year + (nmonths / 12) + 1
    else:
        year = bdate.year + nmonths / 12
    month = month % 12 + 1
    if JALALI:
        day = min(bdate.day, datetime.j_days_in_month[month -1])
    else:
        import calendar
        day = min(bdate.day, calendar.monthrange(year, month)[1])

    return datetime.date(year, month, day)



def newcal(year, month, day):
    """Action. takes a year month and day and starts printing a planner. Prints
    the planner for WEEKSTOPRINT number of weeks"""
    
    #LaTeX preamble. Notice use of double slash - this is used to print a single
    # slash in Python. Also comments will switch to using % as per LaTeX
    top_mat="""\\documentclass[12pt]{article}

%the following lines change font
%\\usepackage[T1]{fontenc}
%\\usepackage[scaled]{helvet}
%\\renewcommand*\\familydefault{\\sfdefault}

%%Paletino
\\usepackage[T1]{fontenc}
\\usepackage[sc]{mathpazo}
\\linespread{1.05}

%%Biolinium
%\\usepackage[T1]{fontenc}
%\\usepackage{libertine}
%\\renewcommand*\\familydefault{\\sfdefault}  %% Only if the base font of the document is to be sans serif


%This is where page size is changed. currently set at half-legal
\\usepackage[margin=0in, paperwidth=7in, paperheight=8.5in]{geometry}
%Take away all margins
\\geometry{top=0cm,bottom=0cm,left=0cm,right=0cm,nohead,nofoot}
%Color is available if wanted
\\usepackage[usenames, dvipsnames]{color}

%Don't know what all this does, but I'd keep it.
\\usepackage{graphicx}
\\usepackage{multicol}
\\usepackage{multirow}

%This next package is cool (and self explanitory)
\\usepackage{colortbl}

%Allow rotating text
\\usepackage{rotating}

%Remove page numbers
\\pagestyle{empty}

%Define a gray that shows up on the printer
\\definecolor{dark-gray}{gray}{0.4}

% Finally!
\\begin{document}

%This is a dirty hack. Later we will need to redefine (renewcommand) \Sun etc
% so they will need to be defined once first otherwise renewcommand complains
\\newcommand{\\Sun}{NULL}
\\newcommand{\\Mon}{NULL}
\\newcommand{\\Tue}{NULL}
\\newcommand{\\Wed}{NULL}
\\newcommand{\\Thr}{NULL}
\\newcommand{\\Fri}{NULL}
\\newcommand{\\Sat}{NULL}
\\newcommand{\\Cal}{NULL}
\\newcommand{\\PageCal}{NULL}

%okay, we want the svgs from inkscape to fill the whole page
\\def\\svgwidth{\\paperwidth}

%This crap is just to create a blank page (the cover), because we want the first
%page of the planner to start on page 2 so that the next days of the week are
%adjacent when the planner is opened.



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%Begining of generated content%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
"""
#End of preamble

    #Take in start date
    currdate=datetime.date(year, month, day)
    
    #Open file "planner.tex" for writing
    ncal=file("planner.tex", 'w')
    #write LaTeX preamble to file
    ncal.write(top_mat)
    
    currdate=currdate.fromordinal((currdate.toordinal()-7))
    
    #Start printing the calendar starting previous Sunday
    while (currdate.weekday()+1)%7!=0:
        currdate=currdate.fromordinal((currdate.toordinal()-1))
        
    ncal.write(monthlyPage(currdate))    
    
    
    #This for loop does the actual page creation    
    for ii in range(WEEKSTOPRINT):
    
    
    
    
    
    
        #this nasty notation is the only way i know how to progress days
        sundate=currdate.fromordinal((currdate.toordinal()+0))
        mondate=currdate.fromordinal((currdate.toordinal()+1))
        tuedate=currdate.fromordinal((currdate.toordinal()+2))
        weddate=currdate.fromordinal((currdate.toordinal()+3))
        thrdate=currdate.fromordinal((currdate.toordinal()+4))
        fridate=currdate.fromordinal((currdate.toordinal()+5))
        satdate=currdate.fromordinal((currdate.toordinal()+6))
        
        
        if weddate.month != currdate.fromordinal((currdate.toordinal()-4)).month:
            ncal.write('~\\newpage')
            ncal.write(monthlyPage(weddate))    
                    
        
        ncal.write("""%%%%%NEW WEEK%%%%\n\n""")
        #replaces any instance of \Sun from Inkscape with the day number
        ncal.write("""\\renewcommand{\\Sun}{%s}\n""" % sundate.day)
        ncal.write("""\\renewcommand{\\Mon}{%s}\n""" % mondate.day)
        ncal.write("""\\renewcommand{\\Tue}{%s}\n""" % tuedate.day)
        ncal.write("""\\renewcommand{\\Wed}{%s}\n""" % weddate.day)
        ncal.write("""\\renewcommand{\\Thr}{%s}\n""" % thrdate.day)
        ncal.write("""\\renewcommand{\\Fri}{%s}\n""" % fridate.day)
        ncal.write("""\\renewcommand{\\Sat}{%s}\n\n""" % satdate.day)
        
        #this next command replaces an instance of \Cal with a full-month cal.
        #we want to print the same month as the next Wednesday because that 
        #will mark the predominent month of that week
        ncal.write("""\\renewcommand{\\Cal}{\n%s}\n\n""" % monthCal(weddate))
        
        #now write the pages created in latex
        ncal.write("""\\centerline{\\input{page1.pdf_tex}}\n""")
        ncal.write("""\\centerline{\\input{page2.pdf_tex}}\n\n\n\n""")
        
        
        #and progress by one week and repeat this for loop
        currdate=currdate.fromordinal((currdate.toordinal()+7))

    ncal.write("""\\end{document}""")
    ncal.close()



if __name__ == "__main__":
    import os
    #we start on this day,month,year but you can choose anything here
    #newcal(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
    newcal(2014, 1, 1)
    #os.system('pdflatex planner.tex')
