from flask import Flask

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from geopy.exc import GeocoderTimedOut

import csv
import json

app = Flask(__name__)


# Function to extract city names based on city.json
def cityNames(city_id):
    f = open('city.json', "r")
    city = json.loads(f.read())
    for element in city:
        if element['id'] == city_id:
            city_name = element['name']
            return city_name

# Function to extract country names based on country.json
def countryNames(country_id):
    f = open('country.json', "r")
    city = json.loads(f.read())
    for element in city:
        if element['id'] == country_id:
            country_name = element['name']
            return country_name

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
    with open('clearLocations.csv') as csv_clearLocations:
        csvClearLocations = csv.reader(csv_clearLocations, delimiter=';')
        clearLocations = list(csvClearLocations)
    
    # Create dataset askedFile.csv representing the asked dataset in the test statement
    askedFile = open('askedFile.csv', 'w', encoding='utf-8')
    heading = "company_id;country_id;city_id;address;is_headquarter;class\n"
    askedFile.write(heading)

    warehouseLatitude, warehouselongitude = longLatAddress(addressWarehouse)
    lonLatWarehouse = (warehouseLatitude, warehouselongitude)
    
    for i in range(len(clearLocations)):
        if clearLocations[i][4] == str(1):
            headquarterLatitude, headquarterlongitude = longLatAddress(clearLocations[i][3] + " " + clearLocations[i][2] + " " + clearLocations[i][1])
            if headquarterLatitude is None and headquarterlongitude is None:
                row = "{};{};{};{};{};{}\n".format(clearLocations[i][0], clearLocations[i][1], clearLocations[i][2], clearLocations[i][3], clearLocations[i][4], "AddressIncorrect")
                askedFile.write(row)
                # return row
            else:
                lonLatHeadquarter = (headquarterLatitude, headquarterlongitude)
                clas = distanceLocations(lonLatHeadquarter, lonLatWarehouse)
                row = "{};{};{};{};{};{}\n".format(clearLocations[i][0], clearLocations[i][1], clearLocations[i][2], clearLocations[i][3], clearLocations[i][4], clas)
                askedFile.write(row)
                askedFile.flush()
                # return row
        else:
            row = "{};{};{};{};{};{}\n".format(clearLocations[i][0], clearLocations[i][1], clearLocations[i][2], clearLocations[i][3], clearLocations[i][4], "NaN")
            askedFile.write(row)
            askedFile.flush()
            # return row

@app.route('/')
def home():
    return '<h1>INVYO Test</h1>'

@app.route('/<addressWarehouse>')
def invyo(addressWarehouse):
    # Open the provided locations.csv file
    with open('locations.csv') as csv_locations:
        csvLocations = csv.reader(csv_locations, delimiter=';')
        locations = list(csvLocations)

    # Create the new dataset, named clearLocations.csv
    clearLocations = open('clearLocations.csv', "w", encoding='utf-8')
    for i in range(len(locations)):
        if locations[i][1] == str(75) and locations[i][3] != 'NULL':
            cityName = cityNames(int(locations[i][2]))
            country_name = countryNames(int(locations[i][1]))
            clearLocations.write("{};{};{};{};{}\n".format(locations[i][0], country_name, cityName, locations[i][3], locations[i][4]))
    
    row = extractHeadquarters(addressWarehouse)
    return '<h1>INVYO Test - Done</h1>'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50001)