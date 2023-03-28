from langchain.chains import LLMChain
from langchain.llms import OpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from util import append_experiment_results

from prompts import promptCombineAndRewordInStyle, promptIsThisAbout, promptGeologicalRegions, promptLocationWithinRegions

from prompts import promptDecideIfCountySmall

### functions functions
from native_skills.macrostrat.macrostrat import getPointLocationStratColumn, macrostratOnlyReturnFirstTwoLayers, macrostratOnlyReturnFirstLayer, ifNoSurfaceGeology
#### macrostrat prompts
from native_skills.macrostrat.macrostrat import macroStratColSummarizationTop, macroStratColSummarizationSecondMostLayer, macroStratColSummarization, macroStratColSummarizationWhenNoColumn

from native_skills.bing.geocoding import getStateAndCountyFromLatLong, getAddressFromLatLong

from native_skills.wikipedia.wikipedia import getWikipediaPageAndProcess, extractContentFromWikipediaPageContent


latitude = 40.7128
longitude = -74.006

places = [
    {
        "name": "New York City",
        "latitude": 40.7128,
        "longitude": -74.006
    },
    {
        "name": "Yukon, Alaska",
        "latitude": 64.881183,
        "longitude": -155.526101
    },
    {
        "name": "Oslo, Norway",
        "latitude": 59.9139,
        "longitude": 10.7522
    },
    {
        "name": "Stravenger, Norway",
        "latitude": 58.9700,
        "longitude": 5.7331
    },
    {
        "name": "Port Clinton, Ohio, USA",
        "latitude": 41.512,
        "longitude": -82.9377
    },
    {
        "name": "Houston, Texas, USA",
        "latitude": 29.7604,
        "longitude": -95.3698
    },
    {
        "name": "San Francisco, California, USA",
        "latitude": 37.7749,
        "longitude": -122.4194
    },
    {
        "name": "London, England, UK",
        "latitude": 51.5074,
        "longitude": 0.1278
    },
    {
        "name": "Paris, France",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    {
        "name": "Rome, Italy",
        "latitude": 41.9028,
        "longitude": 12.4964
    },
    {
        "name": "Taipei, Taiwan",
        "latitude": 25.0478,
        "longitude": 121.5318
    },
    {
        "name": "Banff, Alberta, Canada",
        "latitude": 51.1784,
        "longitude": -115.5708
    },
    {
        "name": "Bocas del Toro, Panama",
        "latitude": 9.3400,
        "longitude": -82.2500
    }
]



#### ADDRESS RELATED CODE
stateAndCountry = getStateAndCountyFromLatLong(latitude,longitude)
fullAddress = getAddressFromLatLong(latitude,longitude)
# #print("stateAndCountry ", stateAndCountry )

print(" The point location of: ",latitude, "latitude and ",longitude," longitude is located in ",fullAddress)


# llm = OpenAI(model_name="text-davinci-003",temperature=0.2)
llm = OpenAI(model_name="text-davinci-003",temperature=0.2, max_tokens=256)



#### GEOLOGY OF A POINT RELATED CODE

def macrostratGeologyForLocation(latitude, longitude):
    macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
    if macrostrat_column_json == "No stratigraphic column data available for this location.":
        #print("No stratigraphic column data available for this location of: ",latitude,longitude, " so we will try to get surface geology data.")
        macrostrat_map_json = ifNoSurfaceGeology(latitude,longitude)
        #print("macrostrat_map_json map geologic data is",macrostrat_map_json)
        #### Using prompt for map data when there is no stratigraphic column data
        chainMacroStratWhenNotColum = LLMChain(llm=llm, prompt=macroStratColSummarizationWhenNoColumn)
        response = chainMacroStratWhenNotColum.run(macrostrat_map_json)
        
    else:
        #print("Found a stratigraphic column data available for this location of. ",latitude,longitude)
        macrostrat_column_json = macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json)
        #### Using prompt for stratigraphic column data
        chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)
        response = chainMacroStrat.run(macrostrat_column_json)
        
    return response


geology_response = macrostratGeologyForLocation(latitude, longitude)

print("The predicted geology near the surface of that point location of is ",geology_response)

#### Initiate the chain to check it a subject is in text or not
checkIfTextAbout = LLMChain(llm=llm, prompt=promptIsThisAbout)


#### REGIONAL GEOLOGY RELATED CODE



chainWiki = LLMChain(llm=llm, prompt=extractContentFromWikipediaPageContent)

regional_geology_subarea = "regional geologic history"

def regionalGeologyOfStateFromWikipedia(stateAndCountry, chainWiki,regional_geology_subarea):
    #search_term = "Geology of "+stateAndCountry["state"]+" state, "+stateAndCountry["country"]
    search_term = "Geology of "+stateAndCountry["state"]+ stateAndCountry["country"]
    wikipedia_page_object = getWikipediaPageAndProcess(search_term,stateAndCountry)
    page_content = wikipedia_page_object["content"]
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(page_content)
    docs = [Document(page_content=t) for t in texts[:3]]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summarized_wikipedia = chain.run(docs)
    wikipedia_page_title = wikipedia_page_object["title"]
    response = chainWiki.run({"subject_to_extract":regional_geology_subarea,"wikipedia_page_content":summarized_wikipedia})
    if "No" in checkIfTextAbout.run({"subject":"geology","text":response}) or "No" in checkIfTextAbout.run({"subject":stateAndCountry["country"],"text":response}):
        ### deferring to direct prompt
        ### decide if we want to use the prompt for the state or the country
        sizeOfCountryInKilometers_chain = LLMChain(llm=llm, prompt=promptDecideIfCountySmall)
        sizeOfCountryInKilometers = sizeOfCountryInKilometers_chain.run(stateAndCountry["country"])
        if int(sizeOfCountryInKilometers) > 500000:
            geology_regions_chain = LLMChain(llm=llm, prompt=promptGeologicalRegions)
            response = geology_regions_chain.run(stateAndCountry["state"])
        else:
            response = geology_regions_chain.run(stateAndCountry["country"])
        return {"summary":response,"wikipedia_page_title":"regional geology areas prompt"}
        
    else: 
        return {"summary":response,"wikipedia_page_title":wikipedia_page_title}

regional_repsonse = regionalGeologyOfStateFromWikipedia(stateAndCountry, chainWiki,regional_geology_subarea)
regional_tectonic_geology_response = regional_repsonse["summary"] 
wikipedia_page_title = regional_repsonse["wikipedia_page_title"] 


print("If we step back and talk about the ", regional_geology_subarea, " of ",stateAndCountry["state"],", ",stateAndCountry["country"]," based on the wikpedia page", wikipedia_page_title ,": ",regional_repsonse["summary"] )


def makeObjectForExperimentResults(latitude,longitude,fullAddress,geology_response,regional_geology_subarea,regional_tectonic_geology_response):
    experiment_results = {
        "latitude":latitude,
        "longitude":longitude,
        "fullAddress":fullAddress,
        "geology_response":geology_response,
        "regional_geology_subarea":regional_geology_subarea,
        "regional_tectonic_geology_response":regional_tectonic_geology_response
    }
    return experiment_results


### Style to reword results into
writerOrWrittingStyle = "Ernest Hemmingway"

styleForRewording = writerOrWrittingStyle + " is a professor teaching a geology 101 field trip and this was his first statement to the class about the geology of this area"


def reWordResponseInStyleLLM(writingStyle,responseObject):
    oneString = ""
    for string in responseObject:
        if type(responseObject[string]) == str:
            oneString = oneString + responseObject[string] + "                    "
    print("oneString is ",oneString)
    print("writingStyle is ",writingStyle)
    ##promptCombineAndRewordInStyleFormatted = promptCombineAndRewordInStyle.format(style=writingStyle, contentJSONIntoString=oneString)
    ##print("promptCombineAndRewordInStyleFormatted is ",promptCombineAndRewordInStyleFormatted)
    chainReword = LLMChain(llm=llm, prompt=promptCombineAndRewordInStyle)
    response = chainReword.run({"style":writingStyle, "contentJSONIntoString":oneString})
    # print("One string is ",oneString)
    # rewordChain = LLMChain(llm=llm, prompt=promptCombineAndRewordInStyle)
    # response = rewordChain.run(oneString)
    return response

responseObjectWithoutText = makeObjectForExperimentResults(latitude,longitude,fullAddress,geology_response,regional_geology_subarea,regional_tectonic_geology_response)

def rewordExperimentResults(style, responseObjectWithoutText):
    rewordedResponse = reWordResponseInStyleLLM(style,responseObjectWithoutText)
    return rewordedResponse

rewordedResponse = rewordExperimentResults(styleForRewording, responseObjectWithoutText)
    
### Save results to file    
    
filepath = "../experiments/results_of_tests/experiment_results.json"

append_experiment_results(filepath, latitude,longitude,fullAddress,geology_response,regional_geology_subarea,regional_tectonic_geology_response,rewordedResponse)


