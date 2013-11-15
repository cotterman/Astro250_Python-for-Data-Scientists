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
import os
import pybtex
from werkzeug import secure_filename
from pybtex.database.input import bibtex

#uploaded files will be saved to this folder
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) # leads to path of script
ALLOWED_EXTENSIONS = set(['txt', 'bib'])

#__name__ refers to the name of the script that I am running
app = Flask(__name__) #this initializes an instance of the Flask object
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
    
    sql_cmd = """
    CREATE TABLE biblio (
        citation_tag TEXT,
        author_list TEXT, 
        journal TEXT,
        volume TEXT, 
        pages TEXT, 
        year INT, 
        title TEXT, 
        collection TEXT);
    """
    cursor.execute(sql_cmd) #do sql_cmd in my current transaction
    print "biblio table has been created"

@app.route('/view_collections', methods=['GET', ])
def view_collections():
    connection = sqlite3.connect("bibliography.db")
    cursor = connection.cursor() #begin my transaction 

    sql_cmd = """
    SELECT collection FROM biblio
    """
    cursor.execute(sql_cmd)
    db_info = cursor.fetchall()
    if db_info==[]:
        return """I pity you fool for having no collections.  Add one
    	          <a href='%s'>here</a>""" % url_for("upload_file")
    else:
        return "Your collections: %s" % db_info
        

#the browser makes either a post or a get request
    #simply going to the webpage initiates a GET request
@app.route('/welcomeyo', methods=['GET', ])
def welcomehi():
    return '''
        <h1>What would you like to do?</h1>
        You may <a href='%s'>View collections</a> -- or -- 
        <a href='%s'>Add a collection</a>
        ''' % (url_for("view_collections"), url_for("upload_file"))

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET',])
def upload_file():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload BibTeX file to add to bibliography database</h1>
    <form action="namecollection" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/namecollection', methods=['POST',])
def namecollection():
    """ Saves uploaded file and asks for collection name """
    # saves the file
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    assert request.method == 'POST'
    file = request.files['file']
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print "name of file that was uploaded: " , filename
    return '''
        <form action="addcollection" method="POST">
        Thank you for uploading your file.  To which collection does it belong?
        <input type="text" name="cname" />
        <input type="hidden" name="filename" value="{}" />
        <input type="submit" />
        </form>'''.format(filename)

@app.route('/addcollection', methods=['POST',])
def addcollection():
    """ Upload bibTeX file """
    
    assert request.method == 'POST'
    filename = request.form['filename']
    cname = request.form['cname']
   
    parser = bibtex.Parser()
    bib_data = parser.parse_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #print "Print bib_data.entries.keys(): " , bib_data.entries.keys()
    for key in bib_data.entries.keys():
        print "key: " , key
        print "title: " , bib_data.entries[key].fields['title']
        #return str(bib_data.entries[key].persons['author'])
    print "read in all keys, no prob"

    connection = sqlite3.connect("bibliography.db")
    cursor = connection.cursor() #begin my transaction
    for key in bib_data.entries.keys():
        #create columns for citation tag, author list, journal, volume, pages, year, title, and collection
        citation_tag = key
        title = bib_data.entries[key].fields['title']
        collection = cname
        print "progress"
        #data = (citation_tag, author_list, journal, volume, pages, year, title, collection)
        #sql_cmd = ("INSERT INTO biblio (citation_tag, author_list, journal, volume, pages, year, title, collection) VALUES " + str(data))
        data = (citation_tag, title, collection)
        print "data: " , data
        sql_cmd = ("INSERT INTO biblio (citation_tag, title, collection) VALUES " + str(data))
        cursor.execute(sql_cmd)
        print "success"
    connection.commit()


    return '''
    <h1>Nice!  You just added the contents of {} to the {} collection. </h1>
    Click <a href={}>here</a> to continue
    '''.format(filename, cname, url_for("welcomehi"))

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

