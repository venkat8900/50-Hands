import requests, json 
from flask import Flask,jsonify,request
import geopy
import csv
import os

app = Flask(__name__)

def getLocationCoordinates(locationName):
  locator = geopy.geocoders.Nominatim(user_agent='lat and lng finder')
  location = locator.geocode(locationName,timeout=180)

  return (location.latitude,location.longitude)

def getPinCode(loc):
	locator = geopy.geocoders.Nominatim(user_agent='pincode finder')
	location = locator.reverse(loc,timeout=180)
	return str(location.raw['address']['postcode'])

@app.route('/nearMeAPI', methods = ['GET', 'POST'])
def getLocationStatus():
    APIKEY = 'AIzaSyAY0Ebwv640AVUvKyQXnK2W_nxXIORMRhE'
    
    content = request.json
    types = content['category']
    city_name = content['city_name']
    pagetoken = None
    
    if "radius" in content.keys():
        radius = content['radius']
    else:
        radius = 4000
    
    lat,lng = getLocationCoordinates(city_name)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={types}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, types = types,APIKEY = APIKEY, pagetoken = "&pagetoken="+pagetoken if pagetoken else ""
    
    PATH = './data.csv'                                                                                                                                             
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print('file exists')
    else: 
        with open('data.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter = ',')
            data_head = [['name', 'pincode', 'status', 'category']]
            a.writerows(data_head)
    
    db = pd.read_csv('data.csv')
    exist_in_db = db[(db['name'] == city_name) & (db['category'] == types)]
    
    if len(exist_in_db) == 0:
        print('pincode not found in the database')
        response = requests.get(url)
        res = json.loads(response.text)
        out = []
        
        for i in range(len(res['results'])):
            if 'opening_hours' in res['results'][i].keys():
                result['business_status'] = res['results'][i]['business_status']
                result['is_open'] = res['results'][i]['opening_hours']['open_now']
                result['location_name'] = res['results'][i]['name']
                query = str(res['results'][i]['geometry']['location']['lat']) + "," + str(res['results'][0]['geometry']['location']['lng'])
                pincode = getPinCode(query)
                print(pincode)
                
                out.append(result)
        
        response = { 'name': result['location_name'], 'pincode': pincode, 'category': types, 'status': result['is_open']}
        db_data = { 'name': result['location_name'], 'pincode': pincode, 'category': types, 'status': result['is_open']}
        df = pd.DataFrame.from_dict(db_data)
        df.to_csv("data.csv", index = False, mode = 'a', header = False)
    else:
        print("data present in database")
        response = { 'name': db[db['name'] == cityname].values.tolist(), 'category': db[db['category'] == types].values.tolist()}
    
    return jsonify(out)

if __name__ == '__main__':
    locator = geopy.geocoders.Nominatim(user_agent = 'demo')
    app.run()
    
            