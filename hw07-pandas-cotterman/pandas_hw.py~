
##############################################################################
# Overview: Use pandas to explore downloaded json file.
# Author: Carolyn Cotterman
##############################################################################


import numpy as np
import pandas as pd
import pprint
import json
from datetime import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import izip


def create_df(FileName):
    """
    Create data from from downloaded json file.
    """
    #Download a dump of data about closed GitHub issues for the pandas project here:
        #https://www.dropbox.com/s/pe6dqooznrfynii/closed.json
    #Use the built-in json library to read this file into memory. Each element in
    #the list contains information about a GitHub issue and all developer comments
    #that were made on it in the 'comments' field.

    myfile = json.load(open(FileName, "r"))
    #check out the first 5 items
    #pprint.pprint(myfile[:5])
 
    #1) Make a DataFrame with one row per issue with the following columns extracted
        #from the issue data: ntitle, created_at, labels, closed_at, user, id
    mydf = pd.DataFrame(index=range(len(myfile)), 
        columns=['title', 'created_at', 'labels', 'closed_at', 'user', 'id'])
    for counter, element in enumerate(myfile):
        mydf.title[counter] = myfile[counter]['title'] 
        mydf.created_at[counter] = myfile[counter]['created_at'] 
        mydf.labels[counter] = myfile[counter]['labels'] 
        mydf.closed_at[counter] = myfile[counter]['closed_at'] 
        #Transform the user values to be simply the 'login' string, so that the user
        #column contains only string usernames.
        mydf.user[counter] = myfile[counter]['user']['login']
        mydf.id[counter] = myfile[counter]['id'] 
    print "\nSample from dataframe produced for item 1:\n" , mydf.ix[:5] , "\n"

    #2) Remove duplicate rows by id from the DataFrame you just created using the id
        #column's duplicated method.
    print "Number of rows before dropping duplicates: " , mydf.shape[0], "\n"
    dedup = mydf.drop_duplicates(['id'])
    print "Number of rows after dropping duplicates (item 2): " , dedup.shape[0], "\n"
    #keep in mind that indices of dedup are not sequential from 0 to dedup.shape[0]


    #3,4) Convert the created_at and closed_at columns from string to datetime type.
        #current fomat looks like this: 2010-09-29T00:45:31Z
    for counter in list(dedup.index):
        dedup.ix[counter]['created_at'] = datetime.strptime(dedup.ix[counter]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        dedup.ix[counter]['closed_at'] = datetime.strptime(dedup.ix[counter]['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
        #these methods also work
            #dedup.ix[counter]['created_at'] = parse(dedup.ix[counter]['created_at'])
            #dedup.ix[counter]['created_at'] = pd.to_datetime(dedup.ix[counter]['created_at'])
    print "Sample from dataframe produced for item 4:\n" , dedup.ix[:5] , "\n"

    return dedup


def plot_issues_per_month(tsdata):
    issues_per_month = tsdata.resample('M', how='count') #number of observations (i.e., issues) per month
    issues_per_month.plot(title="Number of issues created per month")
    plt.savefig('Issues_per_month.pdf')


def plot_users_per_month(tsdata):
    dedup2 = tsdata.drop_duplicates(['user','created_at'])
    #print dedup2[:10]
    users_per_month = dedup2.resample('M', how='count')
    #print users_per_month
    users_per_month.plot(title="Number of distinct users creating issues each month")
    plt.savefig('Users_per_month.pdf') #why do I also see issues_per_month?


def plot_days_elapsed(ts):
    """
    Create a plot and table containing the mean number of days it took for issues 
    to be closed by the month they were opened. 
    In other words, for closed issues created in August 2012, how
     # long were they open on average? (hint: use the total_seconds function on the
     # timedelta objects computed when subtracting datetime objects). Also show the
     # number of issues in each month in the table.
    """

    time_open = np.array(ts["closed_at"])-np.array(ts["created_at"])
    #print type(time_open[5])
    days_open = []
    for i in range(len(time_open)):
        #convert each datetime.timedelta to number of days
        days_diff = time_open[i].total_seconds() / (60.*60*24)
        days_open.append(days_diff)
    #print days_open[:5]
    days_open_ts = pd.Series(days_open, index=ts["created_at"]) 
    #print days_open_ts[:20]

    #get average number of days open per month
    myts3 = days_open_ts.to_period(freq='M') #convert
    mean_days_per_month = myts3.resample('M', how=['mean','count'])
    mean_days_per_month.index.name = "Month"
    print "\nTable for item 6: mean days from creation to closure \n" , mean_days_per_month
    mean_days_per_month.plot(title="Mean number of days it took for issues to be closed")
    plt.savefig('Mean_days_per_month.pdf')


def create_label_df(FileName="closed.json"):
    """
    Create dataframe containing pairs of issue ids and corresponding label(s)
    """
    myfile = json.load(open(FileName, "r"))

    mytups = []
    for counter, element in enumerate(myfile):
        if len(myfile[counter]['labels'])==0:
            mytups.append((myfile[counter]['id'],"None"))
        else:
            nlab = 0
            for label in myfile[counter]['labels']:
                mytups.append(( myfile[counter]['id'], myfile[counter]['labels'][nlab]['name'] ))
                nlab += 1

    #build data frame expanded so each comment gets a row
    mydf = pd.DataFrame(index=range(len(mytups)), columns=['id','label'])     
    for row, tup in enumerate(mytups):
        mydf.ix[row]['id'] = tup[0]
        mydf.ix[row]['label'] = tup[1]

    #get rid of duplicated rows 
        #I assume we should though assignment does not specify here
    mydf2 = mydf.drop_duplicates(['id','label'])
    print "\nSample from dataframe containing labels-id mapping (item 9): \n" , mydf2[:30]

    return mydf2

def create_comment_df(FileName):
    myfile = json.load(open(FileName, "r"))
    #print "Number of rows in original df: " , len(myfile), "\n"

    #size of expanded dataframe
    newsize = 0
    for counter, element in enumerate(myfile):
        for comment in myfile[counter]['comments']:
            newsize +=1
    #print "Number of rows in expanded dataframe:" ,  newsize , "\n"

    #build data frame expanded so each comment gets a row
    mydf = pd.DataFrame(index=range(newsize), 
        columns=['title', 'created_at', 'labels', 'closed_at', 'user', 'id', 'comment_count', 
                 'comment_author','comment_created','comment_text','comment_updated'])
    newrow = 0
    for counter, element in enumerate(myfile):
        for comment in myfile[counter]['comments']:
            mydf.title[newrow] = myfile[counter]['title'] 
            mydf.created_at[newrow] = myfile[counter]['created_at'] 
            mydf.labels[newrow] = myfile[counter]['labels'] 
            mydf.closed_at[newrow] = myfile[counter]['closed_at'] 
            mydf.user[newrow] = myfile[counter]['user']['login']
            mydf.id[newrow] = myfile[counter]['id'] 
            mydf.comment_count[newrow] = len(myfile[counter]['comments'])
            mydf.comment_author[newrow] = comment['author']
            mydf.comment_created[newrow] = comment['created']
            mydf.comment_text[newrow] = comment['text']
            mydf.comment_updated[newrow] = comment['updated']
            newrow += 1
    #print mydf.ix[mydf.comment_count>1][:10]

    #get rid of duplicated rows 
        #I assume we should though assignment does not specify here
    mydf2 = mydf.drop_duplicates(['id','comment_count','comment_author','comment_created','comment_text'])
    #print "Number of rows after dropping duplicates: " , mydf2.shape[0], "\n"

    #Convert the 'created' column to datetime format; note you will need to multiply
    #the values (appropriately converted to integers) by 1000000 to get them in
    #nanoseconds and pass to to_datetime.
    mydf2.index = range(mydf2.shape[0])
    for row in range(mydf2.shape[0]):
        mydf2.comment_created[row] = pd.to_datetime(int(mydf2.comment_created[row])*1000000)

    #change index to comment_created (date) so we can group on this index later
    mydf2 = mydf2.set_index(mydf2.comment_created)
    mydf2 = mydf2.sort_index()
    print "\nSample of dataframe in response to item 7: \n"
    print mydf2[mydf2.comment_count>1][:10][['id','comment_author','comment_created','comment_text']]

    return mydf2

def calc_comments_per_month_REJECT(comment_df):
    """
    Calculate the total number of issue comments
        #I get different answer than I do using the defaultdict approach (why??)
    """
    mydf3 = comment_df.drop(['title', 'created_at', 'labels', 'closed_at', 'user'], axis=1)
    mydf4 = mydf3.to_period(freq='M')
    #print "After sorting and dropping various columns: \n" , mydf3[:5] , "\n"

    mydf5 = mydf4.drop(['comment_count','comment_author','id','comment_updated','comment_text'], axis=1)
    #mydf5 = mydf3.drop_duplicates(['comment_created'])
    #print mydf5[:5]
    comments_per_month = mydf5.resample('M', how='count') #wacky result if I don't first drop most columns (why??)
    #print type(comments_per_month)
    print "\n Item 8a) Number of comments per month: \n \n" , comments_per_month

def calcs_for_item8(comment_df):
    """
    Produce summary table of monthly comments.
    """

    #create a defaultdict of defaultdicts of ints (i.e., the inner defaultdict will map keys to ints)   
    #lambda is a keyword to indicate that we are creating a "unnamed" function
        #ex:  (lambda x,y: 7+x+y)(1,2)
    mydict = defaultdict(lambda: defaultdict(int))
    for date, user in izip(comment_df['comment_created'], comment_df['comment_author']):
        mydict[(date.year, date.month)][user] += 1

    df8 = pd.DataFrame(index=range(len(mydict.keys())), 
        columns=['year-month', 'chattiest_name', 'chattiest_percent', 'author_count','comment_count'])

    #note: the default iterator only iterates over keys, but we want the keys and their associated value(s)
        #.iteritems will return the keys and their associated values
    for counter, ((year, month), data) in enumerate(mydict.iteritems()):
        #print (year, month), max( (v,k) for (k,v) in data.iteritems()) ,\
         #   len(data), sum(data.values())
        df8.ix[counter]['year-month'] = (year, month)
        df8.ix[counter]['chattiest_name'] = max( (v,k) for (k,v) in data.iteritems())[1]
        df8.ix[counter]['chattiest_percent'] = 100*float(max( (v,k) for (k,v) in data.iteritems())[0])/sum(data.values())
        df8.ix[counter]['author_count'] = len(data)
        df8.ix[counter]['comment_count'] = sum(data.values())

    print "\nInfo on comments per month (item 8): \n \n" , df8


def join_issues_and_labels(ts, label_df):
    """
    Join the issues data with the labels helper table (pandas.merge). 
    """

    #join the issues data with the labels helper table (pandas.merge). 
    df10 = pd.merge(ts, label_df, on='id', how='outer')

    #Add a column to this table containing the number of days (as a floating point
    #number) it took to close each issue.
    time_open = np.array(df10["closed_at"])-np.array(df10["created_at"])
    #print type(time_open[5])
    days_open = []
    for i in range(len(time_open)):
        #convert each datetime.timedelta to number of days
        days_diff = time_open[i].total_seconds() / (60.*60*24)
        days_open.append(days_diff)
    df10['days_open'] = days_open

    print "\nSample of dataframe produced for item 10:\n"
    print df10[:30][['id','created_at','closed_at','days_open','label']]
    
    return df10

def calc_time_per_label_month(joined_df):
    """
    Calculate and plot mean time till closure by label, by month
    """

    print "\nSample of dataframe produced for item 11:\n"


###############################################################################


def main():

    #0 - 4) Create data from from supplied json file
        #this data is "deduped" by issue ID number
    ts = create_df(FileName="closed.json")
    #print "Time series (from items 0 - 4)\n" ,  ts.ix[:5]

    #5) Now construct appropriate time series and pandas functions to make the
        #following plots:

    #create time series with index indicating monthly period
    myts = pd.Series(np.array(ts["user"]), index=ts["created_at"])  
    #print "time series: \n", myts[:5] 
    myts2 = myts.to_period(freq='M') #convert to data with a monthly "period" index 
    #print myts2.ix[:5] #now index dates display month and not day (better for graph)

    #graph number of issues per month
    plot_issues_per_month(myts2)    

    #Graph number of distinct users creating issues each month 
    plot_users_per_month(myts2)
    
    #6) Make a table and an accompanying plot illustrating 
        #days elapsed between creation and closure
    plot_days_elapsed(ts)


    #7) Make a DataFrame containing all the comments for all of the issues. 
    #Add an 'id' attribute to each comment while doing so so that each row
    #contains a single comment and has the id of the issue it belongs to.
    comment_df = create_comment_df(FileName="closed.json")

    #8) Compute a table summarizing the following for each month:
        #- Total number of issue comments
        #- The "chattiest" user (most number of comments)
        #- The percentage of total comments made by the chattiest users
        #- The number of distinct participants in the issue comments
    calcs_for_item8(comment_df)


    #9) Create a helper 'labels' table from the issues data with two columns: id and
    #label. If an issue has 3 elements in its 'labels' value, add 3 rows to the
    #table. If an issue does not have any labels, place a single row with None as
    #the label (hint: construct a list of tuples, then make the DataFrame).
    label_df = create_label_df(FileName="closed.json")

    #10) Now, join the issues data with the labels helper table (pandas.merge). Add
    #a column to this table containing the number of days (as a floating point
    #number) it took to close each issue.
    joined_df = join_issues_and_labels(ts, label_df)

    #11) Compute a table containing the average time to close for each label
    #type. Now make a plot comparing mean time to close by month for Enhancement
    #versus Bug issue types.
    calc_time_per_label_month(joined_df)

main()


