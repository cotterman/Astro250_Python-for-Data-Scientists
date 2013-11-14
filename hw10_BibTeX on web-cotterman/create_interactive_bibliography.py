###############################################################################

# Create a flask-based website that provides a query interface to
# BibTeX bibliographic data. The website must allow a user to upload
# a BibTeX file, store the contents of the file in a database, and provide
# a query interface to the database.

# Author: Carolyn Cotterman

###############################################################################

from flask import Flask, redirect, request, url_for

app = Flask(__name__)
app.debug = True

## we can tell our view functions what HTTP methods it
## is allowed to respond to
@app.route('/welcomeyo', methods=['GET', 'POST'])
def welcomehi():

    if request.method == 'POST':
	    collectionname = request.form['cname']
	    if collectionname not in (""," ",None):
	    	return "Your collections: %s" % collectionname
	    else:
	    	return """Please add a collection name and upload corresponding BibTeX file
	    	          <a href='%s'>here</a>""" % url_for("welcomehi")
    else:
    	## this is a normal GET request
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

