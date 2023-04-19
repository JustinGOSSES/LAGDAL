from langchain.prompts import PromptTemplate
# from langchain.utilities import RequestsWrapper
import requests as requests
import json as json


# requests = RequestsWrapper()
# print("test",requests.get("https://www.google.com"))

def getPointLocationStratColumn(latitude,longitude):    
    url="https://macrostrat.org/api/sections?lat=" + str(latitude) + "&lng=" + str(longitude) +"&response=long"
    r = requests.get(url, auth=('user', 'pass'))
    status = r.status_code
    text = r.text
    json_result = r.json()
    #print('json_result',json_result)
    try:
        if len(json_result["success"]["data"]) > 1:
            data = json_result["success"]["data"]
            return data[0:2]  #### changed this to only the top 2 here! not sure this is right long term
        else:
            return "No stratigraphic column data available for this location."
    except:
        return "No stratigraphic column data available for this location."
        
        

def ifNoSurfaceGeology(latitude,longitude):
    url="https://macrostrat.org/api/geologic_units/map/?lat=" + str(latitude) + "&lng=" + str(longitude) +"&response=long"
    r = requests.get(url, auth=('user', 'pass'))
    status = r.status_code
    text = r.text
    json_result = r.json()
    #print('ifNoSurfaceGeology - json_result =',json_result)
    try:
        if json_result["success"]["data"][0]['name']:
            data = json_result["success"]["data"]
            #print("geologic map data, not column data, for a point is: ",data)
            return data
    except:
        return "No surface map geologic data available for this location."
        

def macrostratOnlyReturnFirstLayer(macrostrat_column_json):
    top_layer_json = macrostrat_column_json[0]
    return json.dumps(top_layer_json)

def macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json):
    top_two_layers_json = macrostrat_column_json[0:2]
    return json.dumps(top_two_layers_json)

def jsonToText(macrostrat_column_json):
    return json.dumps(macrostrat_column_json)


########## Semantic prompts

macroStratColSummarizationTop = PromptTemplate(
    input_variables=["macrostrat_column_json"],
    template="Given the following macrostrat stratigraphic column information in JSON format:  {macrostrat_column_json}  Summarize the geology of the location in a paragraph of text with a focus on the top most stratigraphic unit closest to the surface."
)

macroStratColSummarizationSecondMostLayer = PromptTemplate(
    input_variables=["macrostrat_column_json"],
    template="""
      Given the following macrostrat stratigraphic column information in JSON format:  {macrostrat_column_json}  
      
      Ignore the top most layer if it has a thickness of 0 or age of less than 0.1 million years. 
      Then summarize the geology of the location in a two to ten sentence paragraph of text with a focus on the next most closest to the surface stratigraphic layer.
      """
)

macroStratColSummarizationWhenNoColumn= PromptTemplate(
    input_variables=["macrostrat_column_json"],
    template="""
    Given the following macrostrat stratigraphic column information in JSON format in which each stratigraphic layer is a different object in the json 
    
    And within that JSON the following keys have these meanings: 
    name = common language summary of this geologic unit's age and lithology
    lith = List of the lithologies or rock types found in this unit
    liths = percentage of the geologic unit that is lithology in the same order of the lith key. 
    t_int_age = youngest most age for that stratigraphic unit in terms of millions of years
    t_int_name = name of the geologic era that is the youngest age of the geologic unit.
    b_int_age = oldest age for that stratigraphic unit in terms of millions of years
    b_int_name = name of the geologic era that is the oldest age of the geologic unit.
    env = predicted depositional environment if the unit is sedimentary
    
    --input data start-- {macrostrat_column_json}  --input data end-- 
    
    Use that information to summarize in a 7-15 sentences of text the geology of the top 1-2 straigraphic layers at that location. Layers given in order of top most first.
    Be sure to:
     - Describe top and bottom ages of each geologic unit in terms of "millions of years".
     - Be sure to mention percentage of lithology and depositional enviornment as well as age.
    """
)


macroStratColSummarization= PromptTemplate(
    input_variables=["macrostrat_column_json"],
    template="""
    Given the following macrostrat stratigraphic column information in JSON format in which each stratigraphic layer is a different object in the json 
    
    And within that JSON the following keys have these meanings: 
    t_age = youngest most age for that stratigraphic unit in terms of millions of years
    b_age = oldest age for that stratigraphic unit in terms of millions of years
    lith = lithology
    env = predicted depositional environment
    pro = probability of each lithology or depositional environment in a given unit
    
    --input data start-- {macrostrat_column_json}  --input data end-- 
    
    Use that information to summarize in a 7-15 sentences of text the geology of the top two straigraphic layers at that location. 
    Be sure to:
     - Describe each of the two layers separately and include the words 'top two layers'. 
     - Describe top and bottom ages of each stratigraphic unit in terms of "millions of years".
     - Be sure to mention percentage of lithology and depositional enviornment as well as age.
    """
)

