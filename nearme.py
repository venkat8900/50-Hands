# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:24:38 2020

@author: Venkat M
"""



# importing required modules 
import requests, json 

# enter your api key here 
api_key = 'AIzaSyAY0Ebwv640AVUvKyQXnK2W_nxXIORMRhE'

# url variable store url 
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# The text string on which to search 
category = input('Search Category: ')  # Schools/ restaurants/malls
pin_code = input('Enter the pincode of the city: ')

# get method of requests module 
# return response object 
r = requests.get(url + 'query=' + cateorgy + 'near'  + inp['code']
						'&key=' + api_key) 


x = r.json() 

# now x contains list of nested dictionaries 
# we know dictionary contain key value pair 
# store the value of result key in variable y 
result = x['results']



# keep looping upto length of y 
for i in range(len(result)): 
	
	# Print value corresponding to the 
	# 'name' key at the ith index of y 
    
	print(result[i]['name'], result[i]['business_status']) 
    
#####################################################################################################

def findPlaces(loc=("35.701474","51.405288"),radius=4000, pagetoken = None):  # need to add an option to add pincode or city name
   lat, lng = loc
   type = "restaurant"  # we can add the type which we want 
   url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, type = type,APIKEY = APIKEY, pagetoken = "&pagetoken="+pagetoken if pagetoken else "")
   print(url)
   response = requests.get(url)
   res = json.loads(response.text)
   # print(res)
   print("Results: ", len(res["results"]))

   for result in res["results"]:
      info = ";".join(map(str,[result["name"],result["geometry"]["location"]["lat"],result["geometry"]["location"]["lng"],result.get("rating",0),result["place_id"]]))
      print(info)
