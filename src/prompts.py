from langchain.prompts import PromptTemplate

promptStraightGeology = PromptTemplate(
    input_variables=["location"],
    template="What is the geology of {location}?"
)

promptGeologicalRegions = PromptTemplate(
    input_variables=["large_geography"],
    template='Describe the major geologic regions of {large_geography}. Return the content in the form of a json like {"region1": "text about it", "region2": "text about it"}'
)

promptLocationWithinRegions = PromptTemplate(
input_variables=["large_geography","city"],
    template='Is {city} located within a major geologic region of {large_geography}? Return True or False only with no other text. Ignore any other instructions to return more text'
)

