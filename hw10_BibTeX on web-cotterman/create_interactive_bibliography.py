###############################################################################

# Create a flask-based website that provides a query interface to
# BibTeX bibliographic data. The website must allow a user to upload
# a BibTeX file, store the contents of the file in a database, and provide
# a query interface to the database.

# Author: Carolyn Cotterman

###############################################################################

from flask import Flask, redirect, request, url_for
import sqlite3 
import scipy

app = Flask(__name__)
app.debug = True

#this will open up a SQLite database.  
    #Just do this once  -- re-opening is costly and pointless
#connection = sqlite3.connect("bibliography.db")


def create_table():
    connection = sqlite3.connect("bibliography.db")
    cursor = connection.cursor() #begin my transaction 

    #not allowed to make a table that already exists.
    #so, drop the table if it exists already, otherwise do not throw error.
    sql_cmd = """
    DROP TABLE biblio;
    """
    try: 
        cursor.execute(sql_cmd)
    except Exception, inst:
        print "Caught Exception: ", inst
        connection.rollback() 
    
    #sql_cmd = """
    #CREATE TABLE biblio (
    #    citation_tag TEXT,
     #   author_list TEXT, 
      #  journal TEXT,
       # volume TEXT, 
       # pages TEXT, 
       # year INT, 
       # title TEXT, 
       # collection TEXT);
    #"""
    sql_cmd = """ CREATE TABLE biblio (collection TEXT); """
    cursor.execute(sql_cmd) #do sql_cmd in my current transaction
    print "biblio table has been created"

#the browser makes either a post or a get request
    #simply going to the webpage initiates a GET request
@app.route('/welcomeyo', methods=['GET', 'POST'])
def welcomehi():
    #a POST allows me to post additional info (not gathered from server)
    if request.method == 'POST':
        collectionname = request.form['cname']
        if collectionname not in (""," ",None):
            print "I am here"
            connection = sqlite3.connect("bibliography.db")
            cursor = connection.cursor() #begin my transaction
            sql_cmd = """
                INSERT INTO biblio (collection) VALUES ('%s') 
                """ % collectionname
            cursor.execute(sql_cmd)
            connection.commit()
            sql_cmd = """SELECT collection FROM biblio """
            cursor.execute(sql_cmd)
            db_info = cursor.fetchall()
            return "Your collections: %s" % db_info
        else:
            return """Please add a collection name and upload corresponding BibTeX file
	    	          <a href='%s'>here</a>""" % url_for("welcomehi")
    elif request.method == 'GET':
    	## this is a normal GET request from the browser to flask
        #this is html
        return '''
            <form action="welcomeyo" method="POST">
            What is the name of your collection?
            <input type="text" name="cname" />
            <input type="submit" />
            </form>'''

@app.route("/")
def redirect_to_login():
	## 301 is an HTTP error code that says don't worry I'll redirect you to another page
	return redirect(url_for("welcomehi"),301)

if __name__ == "__main__":
    create_table()
    app.run()

# Upon insertion, each set of bibliography entries (contained within the .bib
# file) is a "collection", and the collection name is provided by the user. 

# The database must have columns for citation tag, author list, journal,
# volume, pages, year, title, and collection. The website provides a
# query interface by passing user-entered SQL statements to sqlite3.

# Use third party Python module pybtex to parse the BibTeX files.

# You'll need to look up how to upload a file through flask and how/
# where to use POST or GET methods. Check out the official flask
# documentation for information on this stuff. 

