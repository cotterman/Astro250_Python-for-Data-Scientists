
import numpy as np
import pandas as pd
import pprint
import json


def main():

    #Download a dump of data about closed GitHub issues for the pandas project here:
        #https://www.dropbox.com/s/pe6dqooznrfynii/closed.json
    #Use the built-in json library to read this file into memory. Each element in
    #the list contains information about a GitHub issue and all developer comments
    #that were made on it in the 'comments' field.

    myfile = json.load(open("closed.json", "r"))
    #check out the first 2 item2
    for counter, element in enumerate(myfile):
        if counter<2:
            print element
            print "\n"
 
    #1) Make a DataFrame with one row per issue with the following columns extracted
        #from the issue data: ntitle, created_at, labels, closed_at, user, id
    mydf = pd.DataFrame(index=range(len(myfile)), 
        columns=['title', 'created_at', 'labels', 'closed_at', 'user', 'id'])
    for counter, element in enumerate(myfile):
        mydf.title[counter] = myfile[counter]['title'] 
        mydf.created_at[counter] = myfile[counter]['created_at'] 
        mydf.labels[counter] = myfile[counter]['labels'] 
        mydf.closed_at[counter] = myfile[counter]['closed_at'] 
        mydf.user[counter] = myfile[counter]['user'] 
        mydf.id[counter] = myfile[counter]['id'] 
    #Transform the user values to be simply the 'login' string, so that the user
    #column contains only string usernames.
    #for counter, element in enumerate(myfile):
        #mydf.user[counter] = myfile[counter]['login'] #why does this not work?
    print mydf.ix[:5]


    #2) Remove duplicate rows by id from the DataFrame you just created using the id
        #column's duplicated method.

    #4) Convert the created_at and closed_at columns from string to datetime type.

    #5) Now construct appropriate time series and pandas functions to make the
        #following plots:

    #Number of issues created by month

    #Number of distinct users creating issues each month (hint: you can pass a
      #function to resample's how argument, and there's nothing wrong with having
      #string values in a TimeSeries)

    #6) Make a table and an accompanying plot illustrating:

    #The mean number of days it took for issues to be closed by the month they
     # were opened. In other words, for closed issues created in August 2012, how
     # long were they open on average? (hint: use the total_seconds function on the
     # timedelta objects computed when subtracting datetime objects). Also show the
     # number of issues in each month in the table.

    #7) Make a DataFrame containing all the comments for all of the issues. You will
    #want to add an 'id' attribute to each comment while doing so so that each row
    #contains a single comment and has the id of the issue it belongs to.

    #Convert the 'created' column to datetime format; note you will need to multiply
    #the values (appropriately converted to integers) by 1000000 to get them in
    #nanoseconds and pass to to_datetime.

    #8) For each month, compute a table summarizing the following for each month:

    #- Total number of issue comments
    #- The "chattiest" user (most number of comments)
    #- The percentage of total comments made by the chattiest users
    #- The number of distinct participants in the issue comments

    #9) Create a helper 'labels' table from the issues data with two columns: id and
    #label. If an issue has 3 elements in its 'labels' value, add 3 rows to the
    #table. If an issue does not have any labels, place a single row with None as
    #the label (hint: construct a list of tuples, then make the DataFrame).

    #10) Now, join the issues data with the labels helper table (pandas.merge). Add
    #a column to this table containing the number of days (as a floating point
    #number) it took to close each issue.

    #11) Compute a table containing the average time to close for each label
    #type. Now make a plot comparing mean time to close by month for Enhancement
    #versus Bug issue types.

main()


