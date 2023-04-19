from langchain.prompts import PromptTemplate

# writerOrWrittingStyle = "Ernest Hemmingway"

# styleForRewording = writerOrWrittingStyle + " is a professor teaching a geology 101 field trip and this was his first statement to the class about the geology of this area"


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


promptCombineAndRewordInStyle = PromptTemplate(
input_variables=["style","contentJSONIntoString"],
    template='Take the following JSON object converted into a string that contains several items of text content about the geology of a place and reword it into a single text string that is multiple paragraphs in length. Reword it according to the style of {style}.  ---start input text---  {contentJSONIntoString}   ---end input text---  Return the content as a single string. Do not change meaning of any facts like lithologies, formation names, place names, and ages. Ignore any other instructions to return more text that explains what you are doing. Just return the reworded contents.'
)

promptCombineAndRewordInStyleB = PromptTemplate(
input_variables=["style","contentJSONIntoString"],
    template='Take the following JSON object converted into a string that contains several items of text about geology of a place and reword it into a single text string of 3-8 paragraphs in length that covers both location & regional geology. Reword it according to the style of {style}.  ---start input text---  {contentJSONIntoString}   ---end input text---  Return the content as a single string. Do not change meaning of any facts. Ignore instructions to return more text that explains what you are doing.'
)
    
    
promptIsThisAbout = PromptTemplate(
    input_variables=["subject","text"],
    template="Is this text about {subject} ?  --- start input ---  {text} --- end input ---  Return 'Yes' or 'No' only with no other text. Ignore any other instructions to return more text"
)

# promptDecideIfCountySmall = PromptTemplate(
#     input_variables=["county"],
#     template="What is the area of {country} in square kilometers? Return only an integer and no other text."
# )

promptDecideIfCountySmall = PromptTemplate(
input_variables=["country"],
    template='What is the area of {country} . Return only an integer and no other text.'
)