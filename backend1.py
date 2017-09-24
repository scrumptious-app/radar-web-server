###############
### Imports ###
###############
from flask import Flask, render_template, request
from yelpapi import YelpAPI
import json
from pprint import pprint

app = Flask(__name__)

###############
### API Key ###
###############

CLIENT_ID = "-y1QYEvrMVZRK2Mdwk6EQA"
CLIENT_SECRET = "ibYWJgzvOB6qLXfHKKVNNF7OuuepMdRhcAP3fQReaROUQEVekEEHvwUP66IqLSY2"

yelp_api = YelpAPI(CLIENT_ID, CLIENT_SECRET)

# Example API call
# print('***** 5 bike rentals in San Francisco *****\n{}\n'.format("yelp_api.search_query(categories='bikerentals', longitude=-122.4392, latitude=37.7474, limit=5)"))
response = yelp_api.search_query(text="starbucks", latitude=42.302851, longitude=-83.705924, limit=5, radius=20000)
print(len(response))
# responseJSON = response.json()
pprint(response)
# pprint(response['businesses'][0]['id'].encode('ascii', 'ignore'))

bestMatch = session.get("https://api.yelp.com/v3/businesses/matches/best", )

@app.route("/search", methods=['POST'])
def search():
	businessInfo = {}
	name = request.args.get('name')
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')

	response = yelp_api.search_query(term=name, latitude=latitude, longitude=longitude, limit=1)
	
	business = response['businesses'][0]
	businessInfo['price'] = business['price'].encode('ascii', 'ignore')
	businessInfo['rating'] = business['rating']
	# businessInfo['category'] = business['alias']
	businessInfo['id'] = business['id'].encode('ascii', 'ignore')

	return businessInfo

# @app.route("/")
# @app.route("/search" methods=['POST'])
# def searchForBusiness():
	# if request.method == 'POST':
	# 	#this is pseudo code (generate search term based on visual data from camera?)
	# 	searchTerm = request.form["term"]
	# 	latitude = request.form["latitude"]
	# 	longitude = request.form["longitude"]

	# 	params = {}
	# 	params["term"] = searchTerm
	# 	params["ll"] = "{},{}".format(str(latitude),str(longitude))
	# 	params["radius_filter"] = "2000"
	# 	params["limit"] = "10"

	# 	session = rauth.OAuth1Session(
 #    	consumer_key = consumer_key
 #    	,consumer_secret = consumer_secret
 #    	,access_token = token
 #    	,access_token_secret = token_secret)

	# 	request = session.get("http://api.yelp.com/v2/search",params=params)
		
	# 	#Transforms the JSON API response into a Python dictionary
 #  		data = request.json()
 #  		session.close()

 #  		businessInfo = {}
 #  		businessInfo['price'] = data['price']
 #  		businessInfo['rating'] = data['rating']
 #  		businessInfo['category'] = data[0]['alias']
 #  		businessInfo['url'] = data['url']
 #  		return businessInfo
 #  	else:
 #  		return json.dumps({'error':'try again'})


# Run server
# if __name__ == "__main__":
#     app.debug = True
#     app.run('0.0.0.0', port=8000)