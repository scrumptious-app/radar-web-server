###############
### Imports ###
###############
from __future__ import print_function
from flask import Flask, render_template, request
import json
import rauth
import time
import argparse
import pprint
import requests
import sys
import urllib
from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode

app = Flask(__name__)

##############################
### API Keys and Constants ###
##############################

# OAuth credentials
CLIENT_ID = "-y1QYEvrMVZRK2Mdwk6EQA"
CLIENT_SECRET = "ibYWJgzvOB6qLXfHKKVNNF7OuuepMdRhcAP3fQReaROUQEVekEEHvwUP66IqLSY2"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3

# Get Access Token
def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token

##############
### Routes ###
##############

# Search for a business given latitude, longitude, and name from photo
@app.route("/")
@app.route("/search" methods=['POST'])
def searchForBusiness():
	if request.method == 'POST':
		#this is pseudo code (generate search term based on visual data from camera?)
		searchTerm = request.form["term"]
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]

		params = {}
		params["term"] = searchTerm
		params["ll"] = "{},{}".format(str(latitude),str(longitude))
		params["radius_filter"] = "2000"
		params["limit"] = "10"

		session = rauth.OAuth1Session(
    	consumer_key = consumer_key
    	,consumer_secret = consumer_secret
    	,access_token = token
    	,access_token_secret = token_secret)

		request = session.get("http://api.yelp.com/v2/search",params=params)
		
		#Transforms the JSON API response into a Python dictionary
  		data = request.json()
  		session.close()

  		businessInfo = {}
  		businessInfo['price'] = data['price']
  		businessInfo['rating'] = data['rating']
  		businessInfo['category'] = data[0]['alias']
  		businessInfo['url'] = data['url']
  		return businessInfo
  	else:
  		return json.dumps({'error':'try again'})

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
