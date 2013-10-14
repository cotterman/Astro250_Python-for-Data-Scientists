
##############################################################################
# Overview: Create a database to analyze historical weather data
#    and discovery the relationships between major cities.
# Author: Carolyn Cotterman
##############################################################################

import sqlite3
import urllib2
import pandas as pd

import numpy
from numpy import loadtxt, array

# pip install beautifulsoup4
from bs4 import BeautifulSoup

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
    connection = sqlite3.connect("weather.db") #in SQLite, this opens up the database
    cursor = connection.cursor() #begin my transaction

    #not allowed to make a table that already exists.
    #so, drop the table if it exists already, otherwise do not throw error.
    sql_cmd = """
    DROP TABLE airinfo;
    """
    try: cursor.execute(sql_cmd)
    except Exception: pass

    sql_cmd = """
    CREATE TABLE airinfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    sql_cmd = """
    DROP TABLE topair;
    """
    try: cursor.execute(sql_cmd)
    except Exception: pass

    sql_cmd = """CREATE TABLE topair (id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT, IATA TEXT, airport_name TEXT)"""
    cursor.execute(sql_cmd)
    for airport in topair_data:
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


def get_top_airport_info(test):
    """
    Join the airport_info table with the airport_list table
        Match using IATA code
    """

    connection = sqlite3.connect("weather.db")
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
    get_airport_info(airport_info, test=True) 
    get_top_airports(airport_list, test=True)

    #join the tables together to create table view of intersection
    get_top_airport_info(test=True)


def build_weather_table(test):
    """
    Build another table that will hold historical weather
    information, such as min/max temperature, humidity,
    precipitation, and cloud cover
    """

    connection = sqlite3.connect("weather.db")
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
        celcius_min FLOAT, 
        celcius_max FLOAT, 
        humidity FLOAT, 
        precipitation FLOAT,
        cloud_cover INT);
    """
    cursor.execute(sql_cmd)

    if test:
        #to find out what a database contains:
        sql_cmd = """SELECT name FROM sqlite_master
            WHERE type='table' OR type='view'
            ORDER BY name;"""

        #note: the with syntax is good practice, as it will close the connection
            #regardless of whether the code ends prematurely with an error
        with sqlite3.connect("weather.db") as connection:
            cursor = connection.cursor()
            cursor.execute(sql_cmd)
            db_info = array(cursor.fetchall())
            print db_info
    
    cursor.close() #this seems to not have a purpose (??)
    connection.commit()
    

def grab_weather_data():
    """
    Obtain daily weather info for top 50 airports by looking up 
        ICAO codes on www.wunderground.com
    """

    #Access a months worth of tabular weather data in csv format from Weather
        #Underground using the ICAO airport code. For instance, 
        #to get the weather for San Francisco airport (ICAO code KSFO) 
        #in the month of September 2013, go to:
        #http://www.wunderground.com/history/airport/KSFO/2013/9/1/MonthlyHistory.html?format=1
    pass


##############################################################################


def main():

    ### 1) Create a table of the 50 most travelled airports in the US ### 
    get_airports("hw_6_data/ICAO_airports.csv", "hw_6_data/top_airports.csv")

    ### 2) Build another table that will hold historical weather info ###
        #include min/max temperature, humidity, precipitation, and cloud cover
    build_weather_table(test=True)

    ### 3) Grab historical data from weather underground from 2008 until now ###
        #populate your tables accordingly
    grab_weather_data()

    ### 4) For each pair of cities/airports determine how the daily change of 
        #high temperature and cloud cover from one city predicts the daily change 
        #of the other city 1,3, & 7 days in advance ###


    ### 5) Plot the correlation strengths for the 10 top pairs ###
        #for all three dates, for both temperature and cloud cover 
        #as a function of distance. Also make a plot as a function of longitude difference. 
        #What trends do you see?

main()

