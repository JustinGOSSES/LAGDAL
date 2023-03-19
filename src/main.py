from langchain.chains import LLMChain
from langchain.llms import OpenAI

from prompts import promptStraightGeology
from native_skills.macrostrat.macrostrat import getPointLocationStratColumn, macrostratOnlyReturnFirstTwoLayers, macrostratOnlyReturnFirstLayer
from native_skills.macrostrat.macrostrat import macroStratColSummarizationTop, macroStratColSummarizationSecondMostLayer, macroStratColSummarization


# llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

# chain = LLMChain(llm=llm, prompt=promptStraightGeology)

# location = "Port Clinton, Ohio"
# latitude = 41.5120
# longitude = -82.9377


# def geologyForLocation(location,chain):
#     response = chain.run(location)
#     return response

# geology_response = geologyForLocation(location,chain)

# print("predicted geology description for location of: ",location," is ",geology_response)


####-----
# location = "Port Clinton, Ohio"
# latitude = 41.5120
# longitude = -82.9377

# llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

# chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)

# def macrostratGeologyForLocation(latitude, longitude, chainMacroStrat):
#     macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
#     print("macrostrat_column_json",macrostrat_column_json)
#     response = chainMacroStrat.run(macrostrat_column_json)
#     return response

# geology_response = macrostratGeologyForLocation(latitude, longitude, chainMacroStrat)

# print("predicted geology description for location of: ",location," is ",geology_response)

########

# location = "Port Clinton, Ohio"
# latitude = 41.5120
# longitude = -82.9377

# llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

# chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarizationSecondMostLayer)

# def macrostratGeologyForLocation(latitude, longitude, chainMacroStrat):
#     macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
#     print("macrostrat_column_json",macrostrat_column_json)
#     response = chainMacroStrat.run(macrostrat_column_json)
#     return response

# geology_response = macrostratGeologyForLocation(latitude, longitude, chainMacroStrat)

# print("predicted geology description for location of: ",location," is ",geology_response)

# print("chainMacroStrat prompt",chainMacroStrat.prompt)

#######

location = "New York City, New York"
latitude = 40.7128
longitude = -74.0060

llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)

def macrostratGeologyForLocation(latitude, longitude, chainMacroStrat):
    macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
    macrostrat_column_json2 = macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json)
    print("macrostrat_column_json",macrostrat_column_json2)
    response = chainMacroStrat.run(macrostrat_column_json2)
    return response

geology_response = macrostratGeologyForLocation(latitude, longitude, chainMacroStrat)

print("predicted geology description for location of: ",location," is ",geology_response)

print("chainMacroStrat prompt",chainMacroStrat.prompt)