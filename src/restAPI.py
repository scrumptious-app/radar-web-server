from src import app
from flask import render_template, request
import rauth
import time

@app.route("/")
@app.route("/search" methods=['POST'])
def searchBusinesses():
	if request.method == 'POST':
		#this is pseudo code (generate search term based on visual data from camera?)
		searchTerm = request.form["term"]
		params = {}
		params["term"] = searchTerm
		params["ll"] = "{},{}".format(str(lat),str(long))
		params["radius_filter"] = "2000"
		params["limit"] = "10"
 		return params

def get_results(params):
  	#Obtain these from Yelp's manage access page
  	consumer_key = "YOUR_KEY"
  	consumer_secret = "YOUR_SECRET"
  	token = "YOUR_TOKEN"
  	token_secret = "YOUR_TOKEN_SECRET"
   
  	session = rauth.OAuth1Session(
    	consumer_key = consumer_key
    	,consumer_secret = consumer_secret
    	,access_token = token
    	,access_token_secret = token_secret)
     
  	request = session.get("http://api.yelp.com/v2/search",params=params)
   
  	#Transforms the JSON API response into a Python dictionary
  	data = request.json()
  	session.close()
  	return data

def get_price(data):
	return data["price"]

def get_rating(data):
	return data["rating"]

def get_category(data):
	for x in data["categories"]:
		return x["alias"]

def get_url(data):
	return data["url"]


def main():
	locations = [(39.98,-82.98),(42.24,-83.61),(41.33,-89.13)]
	api_calls = []
	for lat,long in locations:
    	params = searchBusinesses(lat,long)
    	api_calls.append(get_results(params))
    	#Be a good internet citizen and rate-limit yourself
    	time.sleep(1.0)
     
  ##Do other processing