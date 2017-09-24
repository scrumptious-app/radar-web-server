# -*- coding: utf-8 -*-
from src import app
from __future__ import print_function
import flask
from flask import Flask, render_template, request
import argparse
import json
import pprint
import requests
import sys
import urllib

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = "-y1QYEvrMVZRK2Mdwk6EQA"
CLIENT_SECRET = "ibYWJgzvOB6qLXfHKKVNNF7OuuepMdRhcAP3fQReaROUQEVekEEHvwUP66IqLSY2"

# Locu API 
LOCU_API_KEYS = ["dfde5a3db7684a9955eed4596c6007ef18ed6ef7", "ecc4cdde72c7e50c9f859a71d3408cfa2db8eb8f", "f165c0e560d0700288c2f70cf6b26e0c2de0348f", "09aa1c8487370126671d36ad8a27a69866c0cd73", "fcb35836fa320e8c7f7382a4a02a29146a100094", "bdeed6bf5eae32da59856986e058743fb11be970"]

# Facebook Graph API
FACEBOOK_APP_ID = "2000750090180739"
FACEBOOK_APP_SECRET = "10c470942e45a67e4c6e3f22057d3948"
FACEBOOK_TOKEN = "EAACEdEose0cBAI9uki1Ke0YsgJW4icDYGFRxuzxW1QbFqBfbEDx1kdrzH7XacIYbx0mHkdCNtKf9tH6NezzxREVEY54xjFlslZCrL0ZBRt8kvek9ZBZBE7CyWJUGYlO8KqClvAUgv0NZAHeiT3pDblywj0AZAsHFMg24cWlmp6R4ICkybpeVUBusAyvdrjsMoZD"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_TERM = 'mcdonalds'
DEFAULT_LOCATION = 'Detroit, MI'
DEFAULT_LATITUDE = 42.302851
DEFAULT_LONGITUDE = -83.705924
SEARCH_LIMIT = 3

MAIN_CATEGORIES = ["active", "arts", "auto", "beautysvc", "bicycles", "education", "eventservices", "financialservices", "food", "health", "homeservices", "hotelstravel", "localflavor", "localservices", "massmedia", "nightlife", "pets", "professional", "publicservicesgovt", "realestate", "religiousorgs", "restaurants", "shopping"]

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


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, latitude, longitude):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, latitude, longitude):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, latitude, longitude)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1},{2} found.'.format(term, latitude, longitude))
        return ""

    business_id = businesses[0]['id']

    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    response = get_business(bearer_token, business_id)

    # print(u'Result for business "{0}" found:'.format(business_id))
    # pprint(response, indent=2)

    return response

def searchManually(name, latitude, longitude):
    businessInfo = {}

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=name,
                        type=str, help='Search term (default: %(default)s)')
    # parser.add_argument('-l', '--location', dest='location',
    #                     default=DEFAULT_LOCATION, type=str,
    #                     help='Search location (default: %(default)s)')
    parser.add_argument('-lat', '--latitude', dest='latitude',
                        default=latitude, type=float,
                        help='Search latitude (default: %(default)f)')
    parser.add_argument('-long', '--longitude', dest='longitude',
                        default=longitude, type=float,
                        help='Search longitude (default: %(default)f)')

    input_values = parser.parse_args()

    try:
        response = query_api(input_values.term, input_values.latitude, input_values.longitude)
        if response == "":
            return json.dumps(businessInfo)
        # print(response['price'])
        # print({'price': response['price'].encode('ascii', 'ignore')})
        businessInfo['name'] = response['name'].encode('ascii', 'ignore')
        if 'price' in response:
            businessInfo['price'] = response['price'].encode('ascii', 'ignore')
        else:
            businessInfo['price'] = ""

        if 'rating' in response:
            businessInfo['rating'] = response['rating']
        else:
            businessInfo['rating'] = ""
        #print("response category alias: ", response['categories'][0]['alias'])
        #print(type(getCategory(response['categories'][0]['alias'])))
        if 'categories' in response:
            businessInfo['category'] = getCategory(response['categories'][0]['alias'])
        if 'image_url' in response:
            businessInfo['image'] = response['image_url']
        if 'distance' in response:
            businessInfo['distance'] = response['distance']
        businessInfo['id'] = response['id'].encode('ascii', 'ignore')

        print(businessInfo)
        # pprint(businessInfo)

    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

    return json.dumps(businessInfo)

def getCategory(alias):
    # print("alias: ", alias)

    if alias == "":
        return "none"

    with open("categories.json") as json_file:
        json_data = json.load(json_file)
        
        if alias in MAIN_CATEGORIES:
            # print("alias found")
            # print(type(str(alias)))
            return str(alias)
            #return "alias found"

        else:
            aliasIndex = 0
            first = 0
            last = len(json_data)-1
            found = False

            while json_data[first]['alias'] < json_data[last]['alias'] and not found:
                midpoint = (first+last)//2
                if json_data[midpoint]['alias'] == alias:
                    aliasIndex = midpoint
                    found = True
                else:
                    if json_data[midpoint]['alias'] > alias:
                        last = midpoint - 1
                    else:
                        first = midpoint + 1

            # print("get parent category")
            parent = json_data[aliasIndex]['parents'][0]
            
            return getCategory(parent)
            


@app.route("/search", methods=['GET'])
def searchMain():
    businessInfo = {}
    # print(dir(flask.request))
    if flask.request.method == "GET":
        # data = flask.request.data
        # print(data)

        #if all(x in request.args for x in ['name', 'latitude', 'longitude']):
        if 'name' and 'latitude' and 'longitude' in flask.request.args:
            # name = request.args.get('name')
            # latitude = request.args.get('latitude')
            # longitude = request.args.get('longitude')
            name = flask.request.args['name']
            latitude = flask.request.args['latitude']
            longitude = flask.request.args['longitude']

            parser = argparse.ArgumentParser()

            parser.add_argument('-q', '--term', dest='term', default=name,
                                type=str, help='Search term (default: %(default)s)')
            # parser.add_argument('-l', '--location', dest='location',
            #                     default=DEFAULT_LOCATION, type=str,
            #                     help='Search location (default: %(default)s)')
            parser.add_argument('-lat', '--latitude', dest='latitude',
                                default=latitude, type=float,
                                help='Search latitude (default: %(default)f)')
            parser.add_argument('-long', '--longitude', dest='longitude',
                                default=longitude, type=float,
                                help='Search longitude (default: %(default)f)')

            input_values = parser.parse_args()

            try:
                response = query_api(input_values.term, input_values.latitude, input_values.longitude)
                if response == "":
                    return json.dumps(businessInfo)
                # print(response['price'])
                # print({'price': response['price'].encode('ascii', 'ignore')})
                businessInfo['name'] = response['name'].encode('ascii', 'ignore')
                if 'price' in response:
                    businessInfo['price'] = response['price'].encode('ascii', 'ignore')
                else:
                    businessInfo['price'] = ""

                if 'rating' in response:
                    businessInfo['rating'] = response['rating']
                else:
                    businessInfo['rating'] = ""
                #print("response category alias: ", response['categories'][0]['alias'])
                #print(type(getCategory(response['categories'][0]['alias'])))
                if 'categories' in response:
                    businessInfo['category'] = getCategory(response['categories'][0]['alias'])
                if 'image_url' in response:
                    businessInfo['image'] = response['image_url']
                if 'distance' in response:
                    businessInfo['distance'] = response['distance']
                businessInfo['id'] = response['id'].encode('ascii', 'ignore')

                print(businessInfo)
                # pprint(businessInfo)

            except HTTPError as error:
                sys.exit(
                    'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                        error.code,
                        error.url,
                        error.read(),
                    )
                )
    return json.dumps(businessInfo)

@app.route("/nearby", methods=['GET'])
def getNearby():
    nearbyPlaces = {}
    goodPlacesList = {}
    if flask.request.method == "GET":
        if 'name' and 'latitude' and 'longitude' in flask.request.args:
            latitude = str(flask.request.args['latitude'])
            longitude = str(flask.request.args['longitude'])
            latLong = '%s,%s' % (latitude, longitude)
            print(latLong)
            url = "https://graph.facebook.com/search"
            payload = {'type': 'place', 'center': latLong, 'limit':100, 'fields':'name,location,id', 'access_token': FACEBOOK_TOKEN}
            nearbyPlaces = requests.get(url, params=payload).json()['data']

            index = 0
            goodPlacesCount = 0
            while goodPlacesCount < 15:
                searchResults = searchManually(nearbyPlaces[index]['name'], latitude, longitude)
                if len(searchResults) > 0:
                    goodPlacesList[goodPlacesCount] = searchResults
                    goodPlacesCount += 1
                index += 1
            # for place in places:
            #     nearbyPlaces[index] = {"name": }
    return json.dumps(goodPlacesList)

@app.route("/menu", methods=['GET'])
def getMenuItems():
    menuItems = {}
    num_elements = 0
    if flask.request.method == "GET":
        if 'business' in flask.request.args:
            business = str(flask.request.args['business'])

            data = '{"api_key" : "dfde5a3db7684a9955eed4596c6007ef18ed6ef7","fields" : [ "name", "location", "menus"],"venue_queries" : [{"name" : "' + business +'","menus" : { "$present" : true }}]}'

            subsections = requests.post('https://api.locu.com/v2/venue/search', data=data).json()['venues'][0]['menus'][0]['sections'][0]['subsections']
 
            menuItemIndex = 0
            #while menuItemIndex < 10:
            for x in subsections[0]['contents']:
                if 'name' and 'price' in x:
                    menuItems[x['name']] = x['price']
                    menuItemIndex += 1
                elif 'name' in x and 'price' not in x:
                    menuItems[x['name']] = ""
                    menuItemIndex += 1

            """Should return a dictionary that has foods as keys and prices as values"""            
            return json.dumps(menuItems)

    return json.dumps(menuItems)

