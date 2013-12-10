
###############################################################################
########## Data Analytics for Maximizing Donations to Watsi ###################
###############################################################################

import os
import re
import numpy as np
import pandas as pd
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

###############################################################################

#folders within folder from which code is run
downloadfolder = "/Watsi_data_downloaded/"
processedfolder = "/Watsi_data_processed/"
resultsfolder = "/Summary_plots_and_tables/"
ppath = os.getcwd()

#file containing main data of interest
towrite = "Data_summary.csv" 
towrite_path = ppath + processedfolder + towrite

###############################################################################


def get_spreadsheet_info():
    """ I will extract basic info from the posted google doc.

    Info extracted includes:           
          #Age
          #Region (Latin America vs. Asia vs. Africa)
          #Cost of treatment
          #Date posted
          #Number of days posted
          #Donation rate (dollars per day)
    """

    #use regular expression matching to find desired info
    date_pat = re.compile('\d+/\d+/\d+')
    #profileID_pat = re.compile()
    profile_pat = re.compile('<a target="_blank" href="(https://watsi.org/profile/.*?-.*?)">\d+</a>')
    age_and_loc_pat = re.compile("<td class=\"s\d+\">(\d+)</td><td dir=\"ltr\" class=\"s\d+\">(.*?)<")
    costs_pat = re.compile('\$([0-9,]*\.\d{2})<')
    
    myfile = "watsi_spreadsheet_v2.html" #downloaded on Dec 9, 2013
    file = os.path.join(ppath + downloadfolder + myfile)

    #create dataframe in which to store spreadsheet info
    mydf = pd.DataFrame(index=range(10000), 
        columns=['profile_ID','profile_link', 'date_posted', 'date_funded', 'funding_time',
                'patient_age', 'country', 'treat_cost'])
    patient_num = 0
    for line in open(file):
        # split the line into table rows
        rows = re.split("</tr><tr.*?>", line)
        if len(rows) == 1: continue #this line does not contain patient info
        for row in rows: 

            # try to find a profile link, to verify that this is a row in the data table
            profile_links = re.findall(profile_pat, row)
            # if we can't find a profile link, skip this row
            if len(profile_links) == 0: 
                continue
            else:
                assert len(profile_links) == 1 
                profile_link = profile_links[0]

            #obtain profile ID
            soup = BeautifulSoup(row)
            a_tag = soup.findAll('a')
            assert len(a_tag)>1
            profile_ID = "{0:0>3}".format(a_tag[1].text)

            dates = re.findall(date_pat, row)
            # skip this row if profile has not yet been funded (funding date missing)
            if len(dates) < 2:
                continue
            #clear up what appears to be data entry mistake (2013 is not a leap year)
            if dates[0]=="2/29/2013":
                dates[0]="2/28/2013"
            if dates[1]=='8/1/20213':
                dates[1]='8/1/2013'
            #correct data typo (there are 2 profiles with ID 133 and none with ID 132)
            if profile_ID=="133" and dates[0]=="2/11/2013":
                profile_ID="132"
            date_posted = datetime.strptime(dates[0], '%m/%d/%Y')
            date_funded = datetime.strptime(dates[1], '%m/%d/%Y')
            #eliminate the profiles created in June of 2012 -- this was before watsi
                #appears to have had any traction (strange time for funding as a result)
            if date_posted < datetime(2012, 7, 1):
                continue
            funding_time = date_funded - date_posted

            ages_and_locs = re.findall(age_and_loc_pat, row)
            if len(ages_and_locs)<1:
                print "problem with ages_and_locs in profile " , profile_link , ages_and_locs
                continue
            if len(ages_and_locs[0])<1:
                print "problem with ages_and_locs in profile " , profile_link , ages_and_locs
                continue

            treat_cost_string = re.findall(costs_pat, row)[0]
            treat_cost = float(treat_cost_string.replace(",",""))
            if treat_cost>2900: #drop one extreme outlier that throws off results
                treat_cost=None

            #save data
            mydf.profile_ID[patient_num] = profile_ID
            mydf.profile_link[patient_num] = profile_link
            mydf.date_posted[patient_num] = date_posted
            mydf.date_funded[patient_num] = date_funded
            mydf.funding_time[patient_num] = funding_time
            mydf.patient_age[patient_num] = ages_and_locs[0][0]
            mydf.country[patient_num] = ages_and_locs[0][1]
            mydf.treat_cost[patient_num] = treat_cost
            patient_num+=1

    #get rid of empty rows
    mydf = mydf.drop(mydf.index[range(patient_num,mydf.shape[0])])

    print "\nWe have " , mydf.shape[0], " profiles in Watsi's main spreadsheet.\n"
    #print "\nSample from spreadsheet dataframe after first extraction:\n" , mydf.ix[:20] , "\n"     
    
    return mydf


def gender_pronouns(mytext, profile_ID):

    male_words = ['he','his','him','man','boy']
    female_words = ['she','her','woman','girl']
    male_count = 0.
    female_count = 0.    
    
    for word in mytext.split(" "):
        for male_word in male_words:
            if word.lower() == male_word:
                male_count +=1
                continue
        for female_word in female_words:
            if word.lower() == female_word:
                female_count +=1
                continue

    if male_count+female_count > 0:
        proportion_male = male_count/ (male_count+female_count)
    else:
        print "Warning:  no gender-specific words for profile " , profile_ID
        proportion_male =  None

    #replace ambiguous gender with hand look-up
        #(for proportion_male between .3 and .7)
    if profile_ID==11:
        proportion_male = 1
    elif profile_ID==89:
        proportion_male = 1
    elif profile_ID==125:
        proportion_male = 0
    elif profile_ID==160:
        proportion_male = 1
    elif profile_ID==225:
        proportion_male = 0
    elif profile_ID==229:
        proportion_male = 1
    elif profile_ID==263:
        proportion_male = 0
    elif profile_ID==313:
        proportion_male = 1
    elif profile_ID==324:
        proportion_male = 1 #adorable!!
    elif profile_ID==482:
        proportion_male = 1 #adorable!!
    elif profile_ID==509:
        proportion_male = 1 #adorable!!
    elif profile_ID==738:
        proportion_male = 1 
    elif profile_ID==459:
        proportion_male = 0 
    elif profile_ID==887:
        proportion_male = 1
    elif profile_ID==889:
        proportion_male = 1
    elif profile_ID==920:
        proportion_male = 1
    elif profile_ID==940:
        proportion_male = 1
    
    #for now, assign gender based on majority of gender-specific pronouns
    #todo: there were a total of 99 profiles with both gender pronouns
        #might want to examine more cases (or make rules involving babies, etc.)
    if proportion_male>=.5:
        male = 1
    elif proportion_male<.5:
        male = 0
    else:
        male = None

    return male


def get_facial_expression(profile_count):

    myfile = "smiles.csv" #classifications done by human inspection
    file = os.path.join(ppath + downloadfolder + myfile)

    #create dataframe in which to store spreadsheet info
    df_smile = pd.DataFrame(index=range(profile_count+200), 
        columns=['profile_ID','smile_scale'])
    
    for line_num, line in enumerate(open(file)):
        df_smile.profile_ID[line_num] = "{0:0>3}".format(line_num+1) #gen profileID
        df_smile.smile_scale[line_num] = float(line.split(",")[0]) #smile score 0 - 1
        if df_smile.smile_scale[line_num]==99:
            df_smile.smile_scale[line_num]=None
    print "\nWe have imported smile info for " , line_num, " profiles. (includes missings.)"

    return df_smile


def get_text_and_photo_data(mydf_main, download):

    #create dataframe in which to store additional info
    mydf_addon = pd.DataFrame(index=range(mydf_main.shape[0]), 
        columns=['maleness', 'text_length'])

    print "Extract profile text and photo info for " , mydf_main.shape[0], " profiles."
    for row_num in xrange(mydf_main.shape[0]):
    #for row_num in range(3): #use for testing
        if row_num!=781 and row_num!=836 and row_num!=968: #profiles cannot be downloaded for some reason

            myfile = "profile_" + str(row_num) + ".html" # file with downloaded page
            file = ppath + downloadfolder + myfile

            #download page info for each profile
            if download==1:
                url_profile = mydf_main.profile_link[row_num]
                response = urllib2.urlopen(url_profile)
                with open(file, 'w') as f: f.write(response.read()) #write to file

            get_text = 0
            mytext = ""
            for line_num, line in enumerate(open(file)):

                begin_pat = re.compile('</a></div></div><div class="row description"><div class="span2">Description:</div><div')
                begin_text = re.findall(begin_pat, line)
                if len(begin_text)>0:
                    get_text=1

                if get_text==1:
                    mytext = mytext + line

                end_pat = re.compile('</div></div><div class="row transparency"><div class="span2">Transparency:</div><div')
                end_text = re.findall(end_pat, line)
                if len(end_text)>0:
                    get_text=0

            #clean up text a bit
            start_find = '>Description:</div><div class="span8"><p>'
            start_char = mytext.find(start_find)
            end_char = mytext.find('</div></div><div class="row transparency">')
            if  start_char==-1 or end_char==-1:
                print "\nWarning: could not find text descriptors for row " , row_num , "\n"
                #print mytext
                continue
            mytext = mytext[start_char+len(start_find):end_char]
            mytext_clean = mytext.replace("<p>"," ")
            mytext_clean = mytext_clean.replace("</p>"," ")
            #print "\n mytext:" , mytext_clean

            #number of characters in text description
            text_length = len(mytext_clean)

            #obtain proportion of gender-specific words that are male 
            proportion_male = gender_pronouns(mytext_clean, mydf_main.profile_ID[row_num])
            #print "\n proportion_male: " , proportion_male
        
            #place summary of text in dataframe
            mydf_addon.text_length[row_num] = text_length
            mydf_addon.maleness[row_num] = proportion_male

    #obtain facial expression info
    mydf_photo = get_facial_expression(mydf_main.shape[0])
    #print "\nSample from photo info dataframe:\n" , mydf_photo.ix[:20]

    mydf_expand1 = pd.merge(mydf_main, mydf_addon, left_index=True, right_index=True, how='left')
    mydf_expand2 = pd.merge(mydf_expand1, mydf_photo, on='profile_ID', how='left')  

    #print "\nSample from expanded spreadsheet dataframe:\n" , mydf_expand2.ix[:20] , "\n"
    return mydf_expand2

def write_data_csv(mydf):
    
    dollars_per_day_list = []
    days_diff_list = []
    region_list = []
    for row_num in xrange(mydf.shape[0]):

        #indicate geographic region (for 18 countries)
        if mydf.country[row_num]=="Kenya" or mydf.country[row_num]=="Tanzania" or \
            mydf.country[row_num]=="Uganda" or mydf.country[row_num]=="Nigeria" or \
            mydf.country[row_num]=="Ghana" or mydf.country[row_num]=="Somaliland" or \
            mydf.country[row_num]=="Mali" or mydf.country[row_num]=="Malawi" or \
            mydf.country[row_num]=="Zambia" or mydf.country[row_num]=="Ethiopia":
            region = "Africa"
        elif mydf.country[row_num]=="Cambodia" or mydf.country[row_num]=="Burma" or \
            mydf.country[row_num]=="Thailand" or mydf.country[row_num]=="Philippines" or \
            mydf.country[row_num]=="Nepal":
            region = "Asia"
        elif mydf.country[row_num]=="Guatemala" or mydf.country[row_num]=="Panama" or \
            mydf.country[row_num]=="Haiti":
            region = "Central America/ Caribbean"
        else:
            region = None

        #convert each datetime.timedelta to number of days
        if pd.notnull(mydf.funding_time[row_num]):
            days_diff = 1. + (mydf.funding_time[row_num].total_seconds() / (60.*60*24))
        else:
            days_diff = None
        if days_diff<1 or days_diff>30:
            #print "warning: invalid funding time for row " , row_num
            days_diff = None

        #dollars per day donated
        if pd.notnull(mydf.treat_cost[row_num]) and pd.notnull(days_diff):
            dollars_per_day = mydf.treat_cost[row_num] / days_diff
        else:
            #print "\nWarning: cannot calculate dollars_per_day for row " , row_num
            dollars_per_day = None

        region_list.append(region)
        dollars_per_day_list.append(dollars_per_day)
        days_diff_list.append(days_diff)

    mydf['region'] = region_list 
    mydf['dollars_per_day'] = dollars_per_day_list 
    mydf['funding_days'] = days_diff_list   

    mydf.to_csv(towrite_path)


def summarize_data(towrite_path):

    mydf = pd.read_csv(towrite_path)
    #want to make sure dates come in as dates
    mydf['date_posted'] = pd.to_datetime(mydf['date_posted'])
    mydf['date_funded'] = pd.to_datetime(mydf['date_funded'])
    
    #histograms (countries, gender, treatment costs, funding days, donation rate, smiles, etc.)
    


###############################################################################

def main():

    ## Get spreadsheet info from google doc 
    spreadsheet_df = get_spreadsheet_info()

    ## Get data from photo and text 
        #if desired html files are already downloaded, 
         #set download to 0 to prevent re-downloading these files
    expanded_df = get_text_and_photo_data(mydf_main=spreadsheet_df, download=0)

    ## Create additional variables and write data to file
    write_data_csv(expanded_df)

    ## Obtain basic summary stats (can start running from here if csv is already created)
    summarize_data(towrite_path)
     

    #3) Extract info from text (Saturday)
        #Gender
        #Marital status 
        #Parenthood status 
        #cosmetic vs. physical disability vs. life-threatening (extra)
            #"prenatal care" "maternal care"
            #"accident", "burn", "accidently" "fracture" "broken"
            #"congenital ", "hereditary", "birth defect" "tumor" "club feet" "walk again"
            #eye sight, cancer, cancerous, "restore mobility" "walk normally" "cataract" "squamous cell carcinoma"
        #whether medical issue resulted from accident vs. biologically developed (extra)
        #Number of characters
        #Mention of career ambitions (extra)
            #mention of school, teacher
        #correlation with DALYs?  (use age and disability info)

        #do people want to give to sad faces, while being more likely to revisit site if confronted with happy faces?
            #(literature on this?)
        #why are patient IDs sometimes out of order?  (Is this b/c you try to acheive a mix of patient types on site at given point in time?)
            #what determines who is featured on front page (i.e., 3 featured profiles)?
            #were there any changes I should be aware of in terms of profile presentations online?

    #4) Extract photo attributes 
        #Size of face in frame (extra)
        #Outdoor/indoor (extra)
        #Smile/serious -- see http://dalelane.co.uk/blog/?p=2092 (Saturday, by hand)
            #forced smile?
        #Focal point of eyes (extra)
        #camara angle (looking down at child?)
        #tucked chin (e.g., children looking shy)

    #5) Find correlates of donation rate 
        #Sunday -- get simple analysis done, plan more complex analysis
        #Monday -- implement more complex analysis

        #run a "popular" words for different countries (maternal care in Africa, eye stuff in burma, 
                # meningoencephalocele in Cambodia etc.)
            #same thing but for high/low funding rate
            #same thing but for treatment cost 

    #6) Make graphs and figures -- Tuesday

    #7) Make poster -- Wednesday

main()


