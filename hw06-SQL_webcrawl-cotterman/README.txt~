##############################################################################
################## Notes on running code #####################################
##############################################################################

#The program of interest is "predict_weather.py"

#You must have installed sqlite3 and matplotlib to run this code.
#You must also have a subfolder in your pwd called "hw_6_data"
    #this folder should contain ICAO_airports.csv and top_airports.csv
#Code will create subfolder within the "hw_6_data" subfolder 
    called "MyDownloadedData" if it doesn't already exist
    #Code place the downloaded csv files in here
#I was able to execute all components of this problem for 
    the first 10 airports listed in the "top 50" file.
    #Unfortunately, when I moved to running for all top 50, I got errors.
    #Errors are probably due to some idiosyncracies of certain downloaded 
        data files and I unfortunately ran out of time to trouble-shoot.
    #Therefore, my results might look a bit funny.
#If you wish to run my code for testing purposes, I would recommend
    keeping the function build_weather_table and grab_weather_data commented out
    since it will take a while to redownload the data
    and you can just use what's already in "MyDownloadedData" folder

RESULTS:
    #please find the requested graphs, produced by "predict_weather.py":
        #tempF_max_Distances.pdf
        #tempF_max_longitude_diffs.pdf 
        #cloud_cover_Distances.pdf
        #cloud_cover_longitude_diffs.pdf       
    #As expected, the correlations are strongest for smaller lags (i.e., 1 day)
    #I also expected correlations to be strongest for airports closest together
        #But due to limited data, this trend is not obvious.



###############################################################################
######### Notes on the things I learned from this week's module ###############
###############################################################################

#### BACKGROUND BASICS ####

#In python, you are typically pretty specific with how to run a join or a sort
    or a search, etc., and you might be doing things very inefficiently
#SQL is a language used to access databases
    #advantages:
        #Can access items much more quickly 
        (you basically say what you want, and then a database managment system (DBMS)
        decides how best to retreive the result)
        #Allows multiple users simultaneous access 
        (don't need to make copies of the data for individuals to access)
#Popular database management systems (which all interpret the SQL language):
    #PostgreSQL (open-source)   
        #better in every way than MySQL
    #MySQL
        #should not use (only inferior to PostgreSQL)
    #SQLite
        #good for small data (see below)
    #Note: while SQL is the underlying language for the above DBMSs, 
        the functions available while working with any of them do differ.
        Ex:  I couldn't figure out how to do basic stuff like correlations
            or even square roots with sqlite (??)  PostgreSQL, in contrast,
            has a module which allows access to virually all of R's library
            of functions.
#A database is like a structure or a folder and comes with an associated DBMS 
    #another person can't use postgresql while I use mysql on the same DB
    #SQL code (mostly) will transfer, but if you change your mind in terms
        of whether you want to use PostgreSQL, MySQL, or SQLite then you will 
        need to import data info into a new database with you desired DBMS 

#### SQL DETAILS ####

#Table VIEW (versus CREATE):
    #it's a waste of space to store all tables
    #view is a reference to the query that I run which is not stored on disk
    #disadvantage: it will re-run the query whenever it is referenced 
        #so could slow things down if the takes a long time to run
    #note: if underlying data (e.g., topair) changes, then so will the view
    #another alternative with PostgreSQL: materialized view
        #this will save the view on disk
        #different from creating table in that the materialized view
            #will be updated when underlying tables are updated 


#### WAYS TO USE/ACCESS A DATABASE ####

## From Python:
    #sqlite3 (see ipython lecture notebook).  
        #does not use postgreql or mysql....it has its own embedded DBMS
        #good for small data -- don't need to worry about setting up postgresql server
            #connects to the data on disk
    #ipython-sql (see ipython lecture notebook) 
        #probably uses sqlite as the DBMS
    #MySQLdb
        #allows for interaction with a MySQL database
    #PyGreSQL
        #allows for interaction with PostgreSQL database
        #there are many alternative packages (e.g., pg8000, pyscopg2)
        #note: it is cumbersome to setup a PostgreSQL database, which is necessary
            for using PyGreSQL.  But, if you know someone amazing who will
            set one up for you, then using it with PyGreSQL is just like using sqlite
            (but with access to more built-in libraries/ functions)        

## From within the database itself:
    #psql
        #allows interaction with a PostgreSQL database
        #like a light wrapper for the PostgreSQL API
    

