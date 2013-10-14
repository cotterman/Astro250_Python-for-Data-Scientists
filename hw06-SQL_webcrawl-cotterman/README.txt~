##############################################################################
################## Notes on running code #####################################
##############################################################################



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
#A database is like a structure or a folder and comes with an associated DBMS 
    #another person can't use postgresql while I use mysql on the same DB
    #SQL code (mostly) will transfer, but if you change your mind in terms
        of whether you want to use PostgreSQL, MySQL, or SQLite then you will 
        need to import data info into a new database with you desired DBMS  


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
        #there are many alternatives (e.g., pg8000)
        

## From within the database itself:
    #psql
        #allows interaction with a PostgreSQL database
        #like a light wrapper for the PostgreSQL API
    

