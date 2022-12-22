from flask import Flask

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from geopy.exc import GeocoderTimedOut

import csv
import json

app = Flask(__name__)

# Function to extract longitude and latitude from an address
def longLatAddress(address):
    geolocator = Nominatim(user_agent="https://adresse.data.gouv.fr/api-doc/adresse")
    companyLocation = geolocator.geocode(address)

    if companyLocation is not None:
        companyLocationAddress = companyLocation.address
        companyLocationLatitude = companyLocation.latitude
        companyLocationlongitude = companyLocation.longitude
        # return(companyLocationLatitude, companyLocationlongitude)
    else:
        companyLocationLatitude = None
        companyLocationlongitude = None
    return(companyLocationLatitude, companyLocationlongitude)

# Function to measure distance between a headquarter and its warehouses
def distanceLocations(headquarter, warehouse):
    distance = geodesic(headquarter, warehouse).kilometers
    if distance < 20:
        clas = "1"
    elif distance < 100 and distance > 20:
        clas = "2"
    elif distance > 100:
        clas = "3"
    return clas

# Function to measure distance between a headquarter and its warehouses
def distanceLocations(headquarter, warehouse):
    distance = geodesic(headquarter, warehouse).kilometers
    if distance < 20:
        clas = "1"
    elif distance < 100 and distance > 20:
        clas = "2"
    elif distance > 100:
        clas = "3"
    return clas

# Function to extract headquarters from the new dataset clearLocations.csv
def extractHeadquarters(addressWarehouse):
    # Open the created dataset clearLocations.csv
    with open('Dataframe_result.csv') as csv_clearLocations:
        csvClearLocations = csv.reader(csv_clearLocations, delimiter=',')
        clearLocations = list(csvClearLocations)

    askedFile = open('askedFile.csv', 'w', encoding='utf-8')
    heading = "company_id,country_id,country,city_id,city,address,is_headquarter,class\n"
    askedFile.write(heading)
    warehouseLatitude, warehouselongitude = longLatAddress(addressWarehouse)
    lonLatWarehouse = (warehouseLatitude, warehouselongitude)
    for i in range(1, len(clearLocations)):
        headquarterLatitude, headquarterlongitude = longLatAddress(clearLocations[i][5] + " " + clearLocations[i][4] + " " + clearLocations[i][2])
        if headquarterLatitude is None and headquarterlongitude is None:
            row = "{},{},{},{},{},{},{},{}\n".format(clearLocations[i][0], clearLocations[i][1], clearLocations[i][2], clearLocations[i][3], clearLocations[i][4], clearLocations[i][5], clearLocations[i][6], "AddressIncorrect")
            askedFile.write(row)
        else:
            lonLatHeadquarter = (headquarterLatitude, headquarterlongitude)
            clas = distanceLocations(lonLatHeadquarter, lonLatWarehouse)
            row = "{},{},{},{},{},{},{},{}\n".format(clearLocations[i][0], clearLocations[i][1], clearLocations[i][2], clearLocations[i][3], clearLocations[i][4], clearLocations[i][5], clearLocations[i][6], clas)
            askedFile.write(row)
            askedFile.flush()

@app.route('/')
def home():
    return '<h1>INVYO Test</h1>'

@app.route('/<addressWarehouse>')
def invyo(addressWarehouse):
    
    extractHeadquarters(addressWarehouse)
    
    return '<h1>INVYO Test - Done</h1>'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50001)