from langchain.prompts import PromptTemplate

promptStraightGeology = PromptTemplate(
    input_variables=["location"],
    template="What is the geology of {location}?"
)

promptGeologicalRegions = PromptTemplate(
    input_variables=["largeGeography"],
    template='Describe the major geologic regions of {largeGeography}. Return the content in the form of a json Object with the following two keys: "regionName", "regionDescription" for each region in a list.'
)

promptLocationWithinRegions = PromptTemplate(
input_variables=["city", "largeGeography"],
    template='Is {city} located within a major geologic region of {largeGeography}? Return True or False only with no other text. Ignore any other instructions to return more text'
)

