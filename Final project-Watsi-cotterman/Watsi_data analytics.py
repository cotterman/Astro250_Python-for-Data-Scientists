
###############################################################################
########## Data Analytics for Maximizing Donations to Watsi ###################
###############################################################################

#import urllib2
import os
import re

def get_spreadsheet_info():

    #use regular expression matching to find desired info
    date_pat = re.compile('\d+/\d+/\d+')
    profile_pat = re.compile('<a target="_blank" href="(https://watsi.org/profile/.*?-.*?)">\d+</a>')
    age_and_loc_pat = re.compile("<td class=\"s\d+\">(\d+)</td><td dir=\"ltr\" class=\"s\d+\">(.*?)<")
    costs_pat = re.compile('\$([0-9,]*\.\d{2})<')
    
    #folder in which data was downloaded
    subfolder = "/Watsi_data_downloaded/"
    ppath = os.getcwd()
    myfile = "watsi_spreadsheet.html" #downloaded on Dec 1, 2013
    file = os.path.join(ppath + subfolder + myfile)

    for line in open(file):
        # split the line into table rows
        data = re.split("</tr><tr.*?>", line)
        if len(data) == 1: continue
        for x in data: 
            # try to find a profile link, to verify that this is a row in the data table
            profile_links = re.findall(profile_pat, x)
            # if we can't find a profile link, skip this row
            if len(profile_links) == 0: 
                continue
            else:
                assert len(profile_links) == 1 
                profile_link = profile_links[0]
                
            dates = re.findall(date_pat, x)
            ages_and_locs = re.findall(age_and_loc_pat, x)
            all_costs = re.findall(costs_pat, x)
            print profile_link, dates, ages_and_locs, all_costs            

def main():

    #1) Get spreadsheet info from google doc
          #Age
          #Region (Latin America vs. Asia vs. Africa)
          #Cost of treatment
          #Date posted
          #Number of days posted
          #Donation rate (dollars per day)
    get_spreadsheet_info()

    #2) Download photo and text from google doc links 

    #3) Extract info from text (Friday - 
        #Gender (Friday)
        #Marital status (Friday)
        #Parenthood status (Friday)
        #cosmetic vs. physical disability vs. life-threatening (extra)
        #whether medical issue resulted from accident vs. biologically developed (extra)
        #Number of characters (Friday)
        #Mention of career ambitions (extra)

    #4) Extract photo attributes 
        #Size of face in frame (extra)
        #Outdoor/indoor (extra)
        #Smile/serious -- see http://dalelane.co.uk/blog/?p=2092 (Friday, by hand)
        #Focal point of eyes (extra)

    #5) Find correlates of donation rate 
        #Saturday -- get simple analysis done, plan more complex analysis
        #Sunday -- implement more complex analysis

    #6) Make graphs and figures -- Monday

main()


