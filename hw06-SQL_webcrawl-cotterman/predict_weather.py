
##############################################################################
# Overview: Create a database to analyze historical weather data
#    and discovery the relationships between major cities.
# Author: Carolyn Cotterman
##############################################################################

import sqlite3 #I ended up not using this
import urllib2
import os
import pandas as pd
#import psycopg2 #sudo aptitude install pyscopg2

import numpy as np
from numpy import loadtxt, array

import scipy
from scipy.stats.stats import pearsonr

# pip install beautifulsoup4
#from bs4 import BeautifulSoup #I ended up not using this

##############################################################################


def get_airport_info(airport_info, test):
    """
    Store airport info as database table.
    """

    #ICAO_airports.csv (7 Mb) is a list of 43000+ airports with fields:                  
            #"id","ident","type","name","latitude_deg","longitude_deg",         
            #"elevation_ft","continent","iso_country","iso_region",
            #"municipality","scheduled_service","gps_code","iata_code",
            #"local_code","home_link","wikipedia_link","keywords"
    #read_csv won't get tripped up by extra #s and commas like loadtxt does
    airinfo_df = pd.read_csv(airport_info) 
    cursor = connection.cursor() #begin my transaction

    #not allowed to make a table that already exists.
    #so, drop the table if it exists already, otherwise do not throw error.
    sql_cmd = """
    DROP TABLE airinfo;
    """
    try: 
        cursor.execute(sql_cmd)
    except Exception, inst:
        print "Caught Exception: ", inst
        connection.rollback() 
    
    sql_cmd = """
    CREATE TABLE airinfo (
        latitude FLOAT, 
        longitude FLOAT, 
        elevation FLOAT, 
        iata_code TEXT);
    """
    cursor.execute(sql_cmd) #do sql_cmd in my current transaction

    for row in range(airinfo_df.shape[0]):
        latitude = float(airinfo_df['latitude_deg'][row])
        longitude = float(airinfo_df['longitude_deg'][row])
        elevation = float(airinfo_df['elevation_ft'][row])
        #continent = str(airinfo_df['continent'][row])
        iata_code = str(airinfo_df['iata_code'][row])
        #I don't want to throw out observations for which one value is missing, but I get error if I don't
        if (pd.notnull(latitude) and pd.notnull(longitude) and pd.notnull(elevation) 
            and pd.notnull(iata_code)):
            data = (latitude, longitude, elevation, iata_code)
            sql_cmd = ("INSERT INTO airinfo (latitude, longitude, elevation, iata_code) VALUES " + str(data))
            cursor.execute(sql_cmd)

    connection.commit() #commit my transaction (so its visible to others working on database, if applicable)
    #note: this might not succeed if someone commited btwn the time that I opened transaction and I committed
        #not an issue for SQLite since with SQLite, I am the only one working on database


    if test:
        sql_cmd = """SELECT iata_code, latitude, longitude, elevation FROM airinfo WHERE iata_code == 'LAX' """
        cursor.execute(sql_cmd)
        db_info = array(cursor.fetchall())
        print db_info


def get_top_airports(airport_list, test):
    """
    Store airport_list as a database table 
    """

    #airport_list is a csv that contain a list of the 50 most travelled airports in US
        #Fields: City,FAA,IATA,ICAO,Airport,Role,Enplanements
    topair_data = loadtxt(airport_list, skiprows=1, delimiter=",", dtype=str)
    cursor = connection.cursor()

    sql_cmd = """
    DROP TABLE topair;
    """
    try: cursor.execute(sql_cmd)
    except Exception: pass

    top_airports = [] #list to contain IATA codes of top 50 airports

    sql_cmd = """CREATE TABLE topair (city TEXT, IATA TEXT, airport_name TEXT)"""
    cursor.execute(sql_cmd)
    for airport in topair_data:
        top_airports.append(airport[2])
        airport_city = airport[0]
        airport_code = airport[2]
        airport_name = airport[4]
        data = (airport_city, airport_code, airport_name)
        sql_cmd = ("INSERT INTO topair (city, IATA, airport_name) VALUES " + str(data))
        cursor.execute(sql_cmd)

    connection.commit()

    if test:
        sql_cmd = """SELECT city, airport_name FROM topair WHERE IATA == 'LAX' """
        cursor.execute(sql_cmd)
        db_info = array(cursor.fetchall())
        print db_info

    return top_airports


def get_top_airport_info(test):
    """
    Join the airport_info table with the airport_list table
        Match using IATA code
    """

    cursor = connection.cursor()

    #view is a reference to the query that I run which is not stored on disk
    sql_cmd = """
        CREATE VIEW IF NOT EXISTS airports AS 
        SELECT topair.IATA, topair.city, topair.airport_name, 
               airinfo.latitude, airinfo.longitude, airinfo.elevation
        FROM topair 
        INNER JOIN airinfo ON topair.IATA = airinfo.iata_code 
    """
    cursor.execute(sql_cmd)

    if test:
        sql_cmd = """
            SELECT *
            FROM airports LIMIT 10;
        """
        cursor.execute(sql_cmd)
        print cursor.fetchall()

    connection.commit()


def get_airports(airport_info, airport_list):
    """
    Create database that contains a view of 50 top airports with corresponding info
    """

    ## Read in provided csv files into database
    get_airport_info(airport_info, test=False) 
    top_airports = get_top_airports(airport_list, test=False)

    #join the tables together to create table view of intersection
    get_top_airport_info(test=False)

    return top_airports


def build_weather_table(test):
    """
    Build another table that will hold historical weather
    information, such as min/max temperature, humidity,
    precipitation, and cloud cover
    """

    cursor = connection.cursor()

    sql_cmd = """
    DROP TABLE weatherD;
    """
    try: cursor.execute(sql_cmd)
    except Exception: pass

    sql_cmd = """
    CREATE TABLE weatherD (
        iata_code TEXT,
        day_num INT,
        date TEXT,
        tempF_max FLOAT,
        tempF_mean FLOAT,
        tempF_min FLOAT,
        humidity_mean FLOAT,
        wind_mean FLOAT,
        wind_direction FLOAT,
        precipitation FLOAT,
        cloud_cover INT);
    """
    cursor.execute(sql_cmd)

    if test:
        #to find out what a database contains:
        sql_cmd = """SELECT name FROM sqlite_master
            WHERE type='table' OR type='view'
            ORDER BY name;"""
        cursor = connection.cursor()
        cursor.execute(sql_cmd)
        db_info = cursor.fetchall()
        print "Tables in weather.db: " , db_info
    
    cursor.close() #this seems to not have a purpose
    connection.commit()

    
def download_weather(airport, start_yr, end_yr):
    """
    Access a months worth of tabular weather data in csv format from Weather
        Underground using the ICAO airport code. For instance, 
        to get the weather for San Francisco airport (ICAO code KSFO) 
        in the month of September 2013, go to:
        http://www.wunderground.com/history/airport/KSFO/2013/9/1/MonthlyHistory.html?format=1
        Write data into csv files.
    """

    subfolder = "/hw_6_data/MyDownloadedData/" # location of file to be written
    #ppath , file = os.path.split(os.path.realpath(__file__))
    ppath = os.getcwd()

    #create subfolder for airport if subfolder does not already exist
    if os.path.exists(ppath+subfolder+airport) == False:
        os.mkdir(ppath+subfolder+airport)

    years = range(start_yr, end_yr+1)
    for year in years:
        
        if year<2013: months = 12
        else: months = 9 #only go thru sept of 2013 since data does not exist for all of October yet
        for month in range(1, months+1):
        
            myfile = str(year) + "_" + str(month) + ".csv" # file to be written
            file = ppath + subfolder + airport + "/" + myfile
             
            url_beg = "http://www.wunderground.com/history/airport/"
            url_mid = airport + "/" + str(year) + "/" + str(month)
            url_end = "/1/MonthlyHistory.html?format=1"
            response = urllib2.urlopen(url_beg + url_mid + url_end)
            
            with open(file, 'w') as f: f.write(response.read()) #write to file
            #the line above is mostly equivalent (but supeior) to running the following 3:    
                #fh = open(file, "w") #open the file for writing
                #fh.write(response.read()) # read from request while writing to file
                #fh.close()


def insert_line(line, myday, airport, year):

    dlist = line.split(",")
    #skip blank first line and line with var names
    if dlist[0][:4] != str(year):
        return
        
    iata_code = airport
    day_num = myday
    
    try:
        date = dlist[0]
        tempF_max = float(dlist[1])
        tempF_mean = float(dlist[2])
        tempF_min = float(dlist[3])
        humidity_mean = float(dlist[8])
        wind_mean = float(dlist[17])
        wind_direction = float(dlist[22].split("<")[0]) #don't want the XML tag <br />\\n
        precipitation = 0 if dlist[19] == 'T' else float(dlist[19])
        cloud_cover = int(dlist[20])
    except Exception, inst:
        print "Could not convert dlist"
        print inst
        return
    
    data = (iata_code, day_num, date, tempF_min, tempF_max, tempF_mean, 
            humidity_mean, wind_mean, wind_direction, precipitation, cloud_cover)
    #print data #data types look as desired

    cursor = connection.cursor()
    sql_cmd = """
        INSERT INTO weatherD (
            iata_code, day_num, date, 
            tempF_min, tempF_max, tempF_mean,
            humidity_mean, wind_mean, wind_direction,
            precipitation, cloud_cover
        ) VALUES ('%s', %i, '%s', %e, %e, %e,
            %e, %e, %e, %e, %i
        )""" % data
    cursor.execute(sql_cmd)
    connection.commit()


def check_weatherD():
    """
    Print some info on what the weatherD table contains.
    """

    cursor = connection.cursor()

    sql_cmd = """
        SELECT COUNT(*) FROM weatherD;
        """
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    print "Number of records in weatherD: " , db_info

    sql_cmd = """
        SELECT DISTINCT iata_code FROM weatherD;
        """
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    print "Airports included in weatherD: " , db_info

    sql_cmd = """
        SELECT * FROM weatherD WHERE day_num<4;
        """
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    print "First 3 records for each airport in weatherD: " , db_info




def put_weather_in_table(airport, start_yr, end_yr):
    """
    Put weather info from CSV files into table in database
    """

    subfolder = "/hw_6_data/MyDownloadedData/" # location of file to be written
    ppath = os.getcwd()
   
    myday = 0
    years = range(2012, 2014)
    for year in years:
        if year < 2013: months = 12
        else: months = 9 #only go thru sept of 2013 since data does not exist for all of October yet
        
        for month in range(1, months+1):
            myfile = str(year) + "_" + str(month) + ".csv" # file to be written
            file = ppath + subfolder + airport + "/" + myfile
            monthD = open(file, "r") #monthD is a pointer to the file
            
            for line in monthD:
                insert_line(line, myday, airport, year)
                myday +=1


def grab_weather_data(top_airports, download, start_yr, end_yr, run_checks):
    """
    Obtain daily weather info for top 50 airports by looking up 
        ICAO codes on www.wunderground.com
    """
    #pull weather data and save in CSV files on PC.  Do for each airport.
    if download:
        for ICAO_code in top_airports:
            download_weather(ICAO_code, start_yr, end_yr)

    #populate datatable with weather info
    for ICAO_code in top_airports:
        put_weather_in_table(ICAO_code, start_yr, end_yr)

    if run_checks:
        check_weatherD() #check what weatherD table contains        


def corr_changes(top_airports, gaps, variable):
    """For each pair of cities/airports determine how the daily change of 
        #high temperature and cloud cover from one city predicts the daily change 
        #of the other city 1,3, & 7 days in advance ###
    """
    #Note: Cloud cover from the Weather Underground tables ranges from 
        #0 (clear) to 8 (completely cloudy)
    
    cursor = connection.cursor()

    #for airport_pair in top_airports:
    airport1 = "ATL"
    airport2 = "ORD"

    #get required data from tables
    sql_cmd = "SELECT " + variable + " FROM weatherD WHERE iata_code='" + airport1 + "'"
    print sql_cmd
    cursor.execute(sql_cmd)
    #materialize list before converting to array since arrays reallocate memory 
        #everytime an element is added -- costly to add elements
    data1 = np.array([ x[0] for x in cursor.fetchall() ]) 
    print airport1, " has ", data1.shape[0], " non-missing " , variable , " values."

    sql_cmd = "SELECT " + variable + " FROM weatherD WHERE iata_code='" + airport2 + "'"
    print sql_cmd
    cursor.execute(sql_cmd)
    data2 = np.array([ x[0] for x in cursor.fetchall() ]) 
    print airport2, " has ", data2.shape[0], " non-missing " , variable , " values."

    #put daily changes in table
    changesDF = pd.DataFrame(index=range(data1.shape[0]-1), columns=[airport1, airport2])
    changesDF[airport1] = data1[1:] - data1[:-1]
    changesDF[airport2] = data2[1:] - data2[:-1]
    print "Data: " , data1[:10]
    print "Changes: " , changesDF[airport1][:10]

    #find pearson's correlation coefficient
    #for gap in gaps:
    corr = pearsonr(changesDF[airport1], changesDF[airport2])[0]


##############################################################################

#this will open up a SQLite database.  
    #Just do this once  -- re-opening is costly and pointless
connection = sqlite3.connect("weather.db")
#this will open up the postgreSQL database
    #note: anyone can connect to this database if they provide the 
        #dbname, user, password, and host
#connection = psycopg2.connect('dbname=carolyn user=carolyn password=cotterman host=wotan.lbl.gov')


def main():

    ### 1) Create a table of the 50 most travelled airports in the US ### 
        #also, return list of 50 most travelled airports
    top_airports = get_airports("hw_6_data/ICAO_airports.csv", "hw_6_data/top_airports.csv")
    print "List of top 50 airports: " , top_airports

    ### 2) Build another table that will hold historical weather info ###
        #include min/max temperature, humidity, precipitation, and cloud cover
    #build_weather_table(test=True)

    ### 3) Grab historical data from weather underground from 2008 until now ###
        #populate table accordingly
    #grab_weather_data(top_airports[:2], False, 2012, 2013, True)

    ### 4) For each pair of cities/airports determine how the daily changes in
        #one city predicts the daily change of the other city ###
    corr_changes(top_airports[:2], gaps=[(1,3,7)], variable='tempF_max')
    #corr_changes(top_airports[:2], gaps=[(1,3,7)], variable='cloud_cover')

    ### 5) Plot the correlation strengths for the 10 top pairs ###
        #for all three dates, for both temperature and cloud cover 
        #as a function of distance. Also make a plot as a function of longitude difference. 
        #What trends do you see?

main()

