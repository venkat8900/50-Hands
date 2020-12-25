

import requests, json 
from flask import Flask,jsonify,request
import geopy
import pandas as pd
import csv
import os

app = Flask(__name__)




def getLocationCoordinates(locationName):
    locator = geopy.geocoders.Nominatim(user_agent='demo')
    location = locator.geocode(locationName)
    return (location.latitude,location.longitude)

@app.route('/nearMe',methods=['GET','POST'])
def getLocationStatus():
    APIKEY = 'AIzaSyAY0Ebwv640AVUvKyQXnK2W_nxXIORMRhE'

	content = request.json
	types = content['category']
	pincode = content['pincode']
	pagetoken = None
	if "radius" in content.keys():
		radius = content['radius']
	else:
		radius = 4000
    lat,lng = getLocationCoordinates(pincode)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={types}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, types = types,APIKEY = APIKEY, pagetoken = "&pagetoken="+pagetoken if pagetoken else "")
    PATH = './data.csv'
    
   
    
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print('file exists')

    else:
        with open('data.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data_head = [['name', 'pincode', 'status', 'category']]
            a.writerows(data_head)
    
    db = pd.read_csv('data.csv')
    exist_in_db = db[(db['pincode'] == content['pincode']  & (db['category'] == content['category'])]
    
    if len(exist_in_db) == 0:
        print('pincode and catergory not found in db')
        response = requests.get(url)	
	    res = json.loads(response.text)
	    out =[]

    	for i in range(len(res['results'])):
            result={}
            if 'opening_hours' in res['results'][i].keys():
                result['business_status']=res['results'][i]['business_status']
                result['is_open']=res['results'][i]['opening_hours']['open_now']
                result['location_name']=res['results'][i]['name']
                out.append(result)
        
        response = { 'name':result['Location_name'], 'pincode': content['pincode'], 'status': result[is_open] }
        db_data = { 'pincode' : [content['pincode']]*length, 'category': [str(content['category'])]*length, 'status': result['is_open'], 'name': result['location_name']}
        df = pd.DataFrame.from_dict(db_data)
        df.to_csv("data.csv", index = False, mode='a', header=False)
        
    else: 
        print("Data present in database")
        response = {  'name': exist_in_db['name'].values.tolist(), 'pincode': exist_in_db['pincode'].values.tolist() ,'status' : exist_in_db['status'].values.tolist() } 
	
    return jsonify(out)

if __name__ == '__main__':
	locator = geopy.geocoders.Nominatim(user_agent='demo')
	app.run()