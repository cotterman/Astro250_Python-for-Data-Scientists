import os
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson

# Define search term
searchTerm = "hello world"

# Replace spaces ' ' in search term for '%20' in order to comply with request
searchTerm = searchTerm.replace(' ','%20')


# Start FancyURLopener with defined version 
class MyOpener(FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

# Notice that the start changes for each iteration in order to request a new set of images for each loop
i = 0
url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
print url
request = urllib2.Request(url, None, {'Referer': 'testing'})
response = urllib2.urlopen(request)

# Get results using JSON
results = simplejson.load(response)
data = results['responseData']
dataInfo = data['results']

# Iterate for each result and get unescaped url
for count, myUrl in enumerate(dataInfo):
    if count==0:
        url_string = myUrl['unescapedUrl']
        print count, ": " , url_string
        file_extension = url_string.split(".")[len(url_string.split("."))-1]
        myopener.retrieve(url_string, "downloaded_image" + "." + str(file_extension))


# Sleep for one second to prevent IP blocking from Google
time.sleep(1)
