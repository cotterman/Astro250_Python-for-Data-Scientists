
##############################################################################
# Overview: Create a database to analyze historical weather data
#    and discovery the relationships between major cities.
# Author: Carolyn Cotterman
##############################################################################

import sqlite3
import numpy
import pandas as pd
from numpy import loadtxt, array

##############################################################################


### 1) Create a table of the 50 most travelled airports in the US ### 
#include relevant info such as name, city, ICAO code, latitude, and longitude.

## Read in provided csv files into a database 

#top_airports.csv contains a list of the 50 most travelled airports in US
        #Fields: City,FAA,IATA,ICAO,Airport,Role,Enplanements
topair_data = loadtxt("hw_6_data/top_airports.csv", skiprows=1, delimiter=",", dtype=str)
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
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

#test
sql_cmd = """SELECT city, airport_name FROM topair WHERE IATA == 'LAX' """
cursor.execute(sql_cmd)
db_info = array(cursor.fetchall())
print db_info

#ICAO_airports.csv (7 Mb) is a list of 43000+ airports with fields:                  
        #"id","ident","type","name","latitude_deg","longitude_deg",         
        #"elevation_ft","continent","iso_country","iso_region",
        #"municipality","scheduled_service","gps_code","iata_code",
        #"local_code","home_link","wikipedia_link","keywords"

#pd.read_csv won't get tripped up by extra #s and commas like loadtxt does
airinfo_df = pd.read_csv('hw_6_data/ICAO_airports.csv') 
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
sql_cmd = """CREATE TABLE airinfo (id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT, longitude FLOAT, elevation FLOAT, iata_code TEXT)"""
cursor.execute(sql_cmd)

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
connection.commit()

#test
sql_cmd = """SELECT iata_code, latitude, longitude, elevation FROM airinfo WHERE iata_code == 'LAX' """
cursor.execute(sql_cmd)
db_info = array(cursor.fetchall())
print db_info

#join the tables together to create table
    #match using "iata_code" from ICAO_airports and "IATA" from top_airports
#join the tables together
connection = sqlite3.connect("weather.db")
cursor = connection.cursor()

#it's a waste of space to store all tables
#view is a reference to the query that I run which is not stored on disk
#disadvantage: it will re-run the query whenever it is referenced 
    #so could slow things down if the takes a long time to run
#note: if underlying data (e.g., topair) changes, then so will the view
#another alternative with PostgreSQL: materialized view
    #this will save the view on disk
    #different from creating table in that the materialized view
        #will be updated when underlying tables are updated
        
sql_cmd = """
    CREATE VIEW IF NOT EXISTS airports AS 
    SELECT topair.IATA, topair.city, topair.airport_name, 
           airinfo.latitude, airinfo.longitude, airinfo.elevation
    FROM topair 
    INNER JOIN airinfo ON topair.IATA = airinfo.iata_code 
"""
cursor.execute(sql_cmd)

#check
sql_cmd = """
    SELECT *
    FROM airports LIMIT 10;
"""
cursor.execute(sql_cmd)
print cursor.fetchall()

connection.commit()



### 2) Build another table that will hold historical weather info ###
    #include min/max temperature, humidity, precipitation, and cloud cover


### 3) Grab historical data from weather underground from 2008 until now ###
    #populate your tables accordingly


### 4) For each pair of cities/airports determine how the daily change of 
    #high temperature and cloud cover from one city predicts the daily change 
    #of the other city 1,3, & 7 days in advance ###


### 5) Plot the correlation strengths for the 10 top pairs ###
    #for all three dates, for both temperature and cloud cover 
    #as a function of distance. Also make a plot as a function of longitude difference. 
    #What trends do you see?
