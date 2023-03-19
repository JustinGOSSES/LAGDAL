from langchain.prompts import PromptTemplate

# promptKeywords = PromptTemplate(
#     input_variables=["READMEtext"],
#     template="Extract keywords from the text below and return them as a list formatted like ['keyword1','keyword2]. Do not include any \n\n or other text like 'Answer' before or after the list. {READMEtext}",
# )

promptStraightGeology = PromptTemplate(
    input_variables=["location"],
    template="What is the geology of {location}?"
)

# def CellPromptOnEachTextGetResult(texts,chain):
#     results = []
#     for text in texts:
#         keywords = chain.run(text["readme_text"])
#         fullname = text["reponame"]
#         print("keywords for fullname:",keywords)
#         results.append({fullname:keywords})
#     return results

# def kickOffGeologyForLocation(location,chain):
#     geology = chain.run(location)
#     print("geology for location:",geology)
#     return geology