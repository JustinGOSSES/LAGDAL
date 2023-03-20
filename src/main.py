from langchain.chains import LLMChain
from langchain.llms import OpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from prompts import promptStraightGeology

from native_skills.macrostrat.macrostrat import getPointLocationStratColumn, macrostratOnlyReturnFirstTwoLayers, macrostratOnlyReturnFirstLayer
from native_skills.macrostrat.macrostrat import macroStratColSummarizationTop, macroStratColSummarizationSecondMostLayer, macroStratColSummarization

from native_skills.bing.geocoding import getStateAndCountyFromLatLong, getAddressFromLatLong

from native_skills.wikipedia.wikipedia import getWikipediaPageAndProcess, extractContentFromWikipediaPageContent

#location =  41.5120, -82.9377 (Port Clinton, Ohio, USA)
latitude = 58.9700
longitude = 5.7331

stateAndCountry = getStateAndCountyFromLatLong(latitude,longitude)
fullAddress = getAddressFromLatLong(latitude,longitude)

print(" The point location of: ",latitude, "latitude and ",longitude," longitude is located in ",fullAddress)


llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)

def macrostratGeologyForLocation(latitude, longitude, chainMacroStrat):
    macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
    macrostrat_column_json2 = macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json)
    response = chainMacroStrat.run(macrostrat_column_json2)
    return response

geology_response = macrostratGeologyForLocation(latitude, longitude, chainMacroStrat)

print("The predicted geology near the surface of that point location of is ",geology_response)

#print("chainMacroStrat prompt",chainMacroStrat.prompt)


stateAndCountry = getStateAndCountyFromLatLong(latitude,longitude)
#print("stateAndCountry ", stateAndCountry )


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