

import wikipedia
from langchain.prompts import PromptTemplate
import requests as requests
import json as json
import os

def getWikipediaPageForX(subject):
    #### NEED TO IMRPOVE THIS AS FIRST RESULT WILL NOT ALWAYS WORK!!!
    results_of_search = wikipedia.search(subject)
    #print("results_of_search = ",results_of_search)
    #print(" type of results_of_search[0]", type(results_of_search[0]))
    wikipedia_page = wikipedia.page(results_of_search[0])
    #print("wikipedia_page =  ",wikipedia_page)
    #print("type of wikipedia_page", type(wikipedia_page))
    return wikipedia_page

def processWikipediaPage(wikipedia_page):
    # print("wikipedia_page = ",wikipedia_page)
    # wikipedia_page = wikipedia_page[0]
    
    title = wikipedia_page.title
    url = wikipedia_page.url
    content = wikipedia_page.content
    links = wikipedia_page.links
    #print("content = ",content)
    wikipage_object = {
        "title":title,
        "url":url,
        "content":content,
        "links":links
    }
    #print("wikipage_object == ",wikipage_object)
    print("wikipage_object == ",type(wikipage_object.content))
    print("wikipage_object == ",len(wikipage_object.content))
    return wikipage_object
    
def getWikipediaPageAndProcess(subject):
    wikipedia_page = getWikipediaPageForX(subject)    
    wikipedia_page_object = processWikipediaPage(wikipedia_page) 
    return wikipedia_page_object
    
########## Semantic prompts

extractContentFromWikipediaPageContent = PromptTemplate(
    input_variables=["subject_to_extract","wikipedia_page_content"],
    template="""
    Given the following wikipedia article
    --- start wikipedia article ---
    {wikipedia_page_content}
    --- end wikipedia article ---
    extract the content that has to do with: {subject_to_extract} and summarize it into 8-15 sentences.
    """
)
