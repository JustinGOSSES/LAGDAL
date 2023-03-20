from langchain.prompts import PromptTemplate
import requests as requests
import json as json
import os

def getLocationDetailsFromPointCoordinates(latitude,longitude):
    key = os.environ.get('BING_MAPS_KEY')
    url="http://dev.virtualearth.net/REST/v1/Locations/" + str(latitude) + "," + str(longitude) +"?i&verboseplacenames=true&key=" + str(key)
    #print("url",url)
    #   http://dev.virtualearth.net/REST/v1/Locations/41.8781,-87.6298?i&verboseplacenames=true&key=ApoymyMCjjegZyBCvM9yhw_YFrSKaGbseri18vawWGEUFCSLMYBsh4itQ2KGnK6r
    r = requests.get(url, auth=('user', 'pass'))
    status = r.status_code
    if (status == 200):
        result = r.json()
        resultObj = result["resourceSets"][0]["resources"][0]
        # text = r.text
        # json_result = r.json()
        # data = json_result["success"]["data"]
        return resultObj
    if (status != 200):
        return "Error: " + str(status)

#city or neighborhood
def getAdminDistrctFromResultObject(resultObj):
    return resultObj["address"]["locality"]

## State
def getAdminDistrctFromResultObject(resultObj):
    #print("resultObj",resultObj)
    return resultObj["address"]["adminDistrict"]

## County    
def getCountryFromResultObject(resultObj):
    return resultObj["address"]["countryRegion"]

## full street address  
def getAddressFromResultObject(resultObj):
    return resultObj["address"]["formattedAddress"]


## given lat/long return state and country using bing maps API
def getStateAndCountyFromLatLong(latitude,longitude):
    resultObj = getLocationDetailsFromPointCoordinates(latitude,longitude)
    state = getAdminDistrctFromResultObject(resultObj)
    country = getCountryFromResultObject(resultObj)
    return {"state":state, "country":country}

def getAddressFromLatLong(latitude,longitude):
    resultObj = getLocationDetailsFromPointCoordinates(latitude,longitude)
    return getAddressFromResultObject(resultObj)

########## Semantic prompts

extractCityFromStreetAddress = PromptTemplate(
    input_variables=["address"],
    template="Given the following street address that could be in any country worldwide and comes from Bing Maps API, what is the likely city, town, or village {address} "
)


