from flask import Flask

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import pandas as pd
import os

# Remove generated files if exists
try:
    os.remove('Dataframe_result.csv')
    os.remove('askedFile.csv')
except OSError:
    pass

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

# Function to measure distance between a warehouse and headquarters
def distanceLocations(headquarter, warehouse):
    distance = geodesic(headquarter, warehouse).kilometers
    if distance < 20:
        clas = "1"
    elif distance < 100 and distance > 20:
        clas = "2"
    elif distance > 100:
        clas = "3"
    return clas

# Function to extract headquarters from the new dataframe "extractedDF"
def extractHeadquarters(addressWarehouse):
    # Load dependencies as dataframes
    dfLocations = pd.read_csv('locations.csv', sep=';')
    dfCountry = pd.read_json('country.json')
    dfCity = pd.read_json('city.json')

    # Replace City and Country codes based on city.json and country.json files
    dfLocations.insert(3, "city", "_" , True)
    dfLocations['city'] = dfLocations['city_id'].map(dfCity.set_index('id')['name'])
    dfLocations.insert(2, "country", "_" , True)
    dfLocations['country'] = dfLocations['country_id'].map(dfCountry.set_index('id')['name'])

    # Filter to extract only headquarters located in France
    IdFrance = dfCountry[(dfCountry['name'] == 'France')].values[0].tolist()[0]
    extractedDF = dfLocations[(dfLocations['is_headquarter'] == 1) & (dfLocations['country_id'] == IdFrance)]

    # Filter to remove NaN addresses
    extractedDF = extractedDF.dropna()
    extractedDF.to_csv('Dataframe_result.csv', index=False, header=True)

    # Extract longitude and latitude from addressWarehouse
    warehouseLatitude, warehouselongitude = longLatAddress(addressWarehouse)
    lonLatWarehouse = (warehouseLatitude, warehouselongitude)

    # Create empty list for appending headquarter classes
    classColumn = []
    
    # Iterate over extractedDF and assign class
    for i, row in extractedDF.iterrows():
        headquarterLatitude, headquarterlongitude = longLatAddress(extractedDF['address'][i] + " " + extractedDF['city'][i] + " " + extractedDF['country'][i])
        if headquarterLatitude is None and headquarterlongitude is None:
            classColumn.append("incorrectAddress")
        else:
            lonLatHeadquarter = (headquarterLatitude, headquarterlongitude)
            clas = distanceLocations(lonLatHeadquarter, lonLatWarehouse)
            classColumn.append(clas)

    return extractedDF, classColumn

@app.route('/')
def home():
    return '<h1>INVYO Test</h1>'

@app.route('/<addressWarehouse>')
def invyo(addressWarehouse):
    
    # Call function to extract headquarters, measure distance, and classify.
    extractedDF, classColumn = extractHeadquarters(addressWarehouse)

    extractedDF["Class"] = classColumn
    extractedDF.to_csv('askedFile.csv', index=False, header=True)
    
    return '<h1>INVYO Test - Done</h1>'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50001)