from langchain.chains import LLMChain
from langchain.llms import OpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from prompts import promptStraightGeology

### functions functions
from native_skills.macrostrat.macrostrat import getPointLocationStratColumn, macrostratOnlyReturnFirstTwoLayers, macrostratOnlyReturnFirstLayer, ifNoSurfaceGeology
#### macrostrat prompts
from native_skills.macrostrat.macrostrat import macroStratColSummarizationTop, macroStratColSummarizationSecondMostLayer, macroStratColSummarization, macroStratColSummarizationWhenNoColumn

from native_skills.bing.geocoding import getStateAndCountyFromLatLong, getAddressFromLatLong

from native_skills.wikipedia.wikipedia import getWikipediaPageAndProcess, extractContentFromWikipediaPageContent

#location =  41.5120, -82.9377 (Port Clinton, Ohio, USA)

# ## Stravenger Norway
# latitude = 58.9700
# longitude = 5.7331 

latitude = 59.9139
longitude = 10.7522

#### ADDRESS RELATED CODE
stateAndCountry = getStateAndCountyFromLatLong(latitude,longitude)
fullAddress = getAddressFromLatLong(latitude,longitude)
# #print("stateAndCountry ", stateAndCountry )

print(" The point location of: ",latitude, "latitude and ",longitude," longitude is located in ",fullAddress)


llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

#### GEOLOGY OF A POINT RELATED CODE
#chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)

def macrostratGeologyForLocation(latitude, longitude):
    macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
    if macrostrat_column_json == "No stratigraphic column data available for this location.":
        print("No stratigraphic column data available for this location of: ",latitude,longitude, " so we will try to get surface geology data.")
        macrostrat_map_json = ifNoSurfaceGeology(latitude,longitude)
        print("macrostrat_map_json map geologic data is",macrostrat_map_json)
        #### Using prompt for map data when there is no stratigraphic column data
        chainMacroStratWhenNotColum = LLMChain(llm=llm, prompt=macroStratColSummarizationWhenNoColumn)
        response = chainMacroStratWhenNotColum.run(macrostrat_map_json)
        
    else:
        print("Found a stratigraphic column data available for this location of. ",latitude,longitude)
        macrostrat_column_json = macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json)
        #### Using prompt for stratigraphic column data
        chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)
        response = chainMacroStrat.run(macrostrat_column_json)
        
    return response


# def macrostratGeologyForLocation(latitude, longitude):
#     macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
#     if macrostrat_column_json == "No stratigraphic column data available for this location.":
#         print("No stratigraphic column data available for this location of: ",latitude,longitude)
#         macrostrat_column_json = ifNoSurfaceGeology(latitude,longitude)
#         chainMacroStratWhenNotColum = LLMChain(llm=llm, prompt=macroStratColSummarizationWhenNoColumn)
#         response = chainMacroStratWhenNotColum.run(macrostrat_column_json)
        
#     else:
#         print("Found a stratigraphic column data available for this location of. ",latitude,longitude)
#         macrostrat_column_json2 = macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json)
#         if macrostrat_column_json2 == "No stratigraphic column data available for this location.":
#             print("No stratigraphic column data available for this location of: ",latitude,longitude)
#             return macrostrat_column_json2
#         else:
#             chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)
#             response = chainMacroStrat.run(macrostrat_column_json2)
        
#     return response

geology_response = macrostratGeologyForLocation(latitude, longitude)

print("The predicted geology near the surface of that point location of is ",geology_response)


#### REGIONAL GEOLOGY RELATED CODE


chainWiki = LLMChain(llm=llm, prompt=extractContentFromWikipediaPageContent)

regional_geology_subarea = "structural ors tectonic geology"

def regionalGeologyOfStateFromWikipedia(stateAndCountry, chainWiki,regional_geology_subarea):
    #search_term = "Geology of "+stateAndCountry["state"]+" state, "+stateAndCountry["country"]
    search_term = "Geology of "+stateAndCountry["state"]
    wikipedia_page_object = getWikipediaPageAndProcess(search_term)
    page_content = wikipedia_page_object["content"]
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(page_content)
    docs = [Document(page_content=t) for t in texts[:3]]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summarized_wikipedia = chain.run(docs)

    response = chainWiki.run({"subject_to_extract":regional_geology_subarea,"wikipedia_page_content":summarized_wikipedia})
    return response

regional_tectonic_geology_response = regionalGeologyOfStateFromWikipedia(stateAndCountry, chainWiki,regional_geology_subarea)

print("If we step out to a regional scale and specifically talking about the regional ", regional_geology_subarea, " of ",stateAndCountry["state"]," : ",regional_tectonic_geology_response)