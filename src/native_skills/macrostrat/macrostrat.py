from langchain.prompts import PromptTemplate
# from langchain.utilities import RequestsWrapper
import requests as requests
import json as json


# requests = RequestsWrapper()
# print("test",requests.get("https://www.google.com"))

def getPointLocationStratColumn(latitude,longitude):
    #print("requets",requests)
    
    url="https://macrostrat.org/api/sections?lat=" + str(latitude) + "&lng=" + str(longitude) +"&response=long"
    r = requests.get(url, auth=('user', 'pass'))
    status = r.status_code
    text = r.text
    json_result = r.json()
    data = json_result["success"]["data"]
    return data

def macrostratOnlyReturnFirstLayer(macrostrat_column_json):
    top_layer_json = macrostrat_column_json[0]
    return json.dumps(top_layer_json)

def macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json):
    top_two_layers_json = macrostrat_column_json[0:2]
    return json.dumps(top_two_layers_json)

def jsonToText(macrostrat_column_json):
    return json.dumps(macrostrat_column_json)

# def convertStratColumnToText(stratColumn):
    
#     return text

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

macroStratColSummarization= PromptTemplate(
    input_variables=["macrostrat_column_json"],
    template="Given the following macrostrat stratigraphic column information in JSON format in which each stratigraphic layer is a different object in the json and t_age is youngest most age and b_age is oldest age for that unit and lith=lithology and env=depositional environment:  {macrostrat_column_json}  use that information to summarize the geology of the location in a 5-15 sentences of text. Be sure to describe each of the two layers separately."
)

