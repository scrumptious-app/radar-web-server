from src import app
from flask import render_template, request
import rauth
import time

################
### API Keys ###
################

#Obtain these from Yelp's manage access page
consumer_key = "YOUR_KEY"
consumer_secret = "YOUR_SECRET"
token = "YOUR_TOKEN"
token_secret = "YOUR_TOKEN_SECRET"

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

def main():
	# locations = [(39.98,-82.98),(42.24,-83.61),(41.33,-89.13)]
	# api_calls = []
	for latitude, longitude in locations:
    	params = searchBusinesses(lat,long)
    	api_calls.append(get_results(params))
    	#Be a good internet citizen and rate-limit yourself
    	time.sleep(1.0)
     
  ##Do other processing