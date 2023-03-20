from langchain.prompts import PromptTemplate

promptStraightGeology = PromptTemplate(
    input_variables=["location"],
    template="What is the geology of {location}?"
)
