# LAGDAL
It's an acronym..

LLM Assisted Geology Descriptions of Arbitrary Locations = LAGDAL

This is currently an experiment on the weekends when I have a little time type of thing.

### Purpose
The purpose of this project is to see to what degree a description of the local geology like what you might hear 
on a geology field trip stop could be programmatically generated. 

Given LLMs in 2023-03 tend to generate fake details about the local geology when you ask them to do this in a 
single prompt, this project will combine APIs with deterministic geologic information from large database, text 
content extracted from wikipedia and search results, and the abilities of LLM to extract content, summarize, determine if information of a specific type exists, etc. 

_The idea behind this attempt is to combine the strengths of LLM in text summarization, extraction, and writing with the strengths of geology data APIs like Marcostrat and the regional geologic descriptions that exist on Wikipedia and other places._

### How a future final product might be used
You might sit at a computer and what to get back pargaraph to page level summary descriptions of the geology 
of geographic places that range in scale from specific points to cities, states, countries, etc. You might query 
for this summmary or any changes in the summary at several points over some time. For example, you could 
intitially ask for a large summary, then ask for any differences 10 minutes later. This would be useful if you 
were on a road, train, or airplane trip. 

### Context & History & Difficulties


#### Strengths and weaknesses of Macrostrat API

#### Strengths and weaknesses of Wikipedia Geology of X

#### Strengths and weaknesses of Google or Bing Searches



## Brainstorming prompts and APIs to use...


## Skills
The following outline of potential semantic skills and deterministic functions are what is imagined might be necessary.


### Macrostrat
Data for a given lat/long and either at surface, 2nd layer down, or strat column going downwards.
- age
- lithologies
- depositional environment
- fossils (optional)

#### Macrostrat specific sementic functions
- convert from API data into words
    - summary of top layer
    - summary of 2nd layer
    - whether top layer is unlithified recent deposits to be ignored
    - summary of full stratigraphic column at that point location
- summary of multiple point locations and any of the previous points

### Wikipedia 
- geology of ___ country
- geology of ____ state in USA, or state/provience in other country, or region of country

#### wikipedia specific semantic functions
- extract from wikipedia geology page
    - extensional, contractual, or strike slip or combination structural regime
    - near or in ocean or mountains or coastal plain or craton
    - summary of tectonic setting
    - citations
        - within wikipedia article, return all citations
        - within wikipedia article, return citations having to do with ____ 

### Spatial
- Whether location is city, county, state/province, region, or country
- size of area in square kilometers or miles
- convert to square miles to kilometers and inverse
- Find lattitude and longitude of center point of given location
- Find X number of selected points within boundariees of location.

### General text summarization and extraction
- Given text X summarize down to ___ size.
- Given text X extract the part of the text that is about ____ if it exists.
- Given this JSON of strings and numbers and objectst that contain strings and numbers, reword it into a paragraph. Important context of the meaning of the keys is _____. 

### Google Search


### Bing Search Chat


## Narrative Goals

```
For geography of point, cities, counties, states, countries, etc. 

the size of the area is.... point, square area...

Tell...

Bedrock geology age, lithology, depositional environment...formations...

oldest rock unit exposed at the surface...

stratigraphic column going down..... (optional)

summarize regional structural geology of the area... 

mountains...plains.....lakes...oceans...coastal plans..craton....

type of tectonics....extensional, contraction, strike slip....

interesting fossils, gems, or minerals to find?
```



## How to Install


## How to Run


## Getting Started


## Contributing



#### NOTES on how to run...


## Early Results


#### Calling Macrostrat API and then using deterministic & LLM semantic functions to summarize the JSON data results into an easily readable format
`predicted geology description for top 2 layers at location of:  New York City, New York  is  

This location is composed of two stratigraphic layers. The first layer is composed of sand, with a siliciclastic sedimentary lithology and a shoreface marine depositional environment. It has a thickness of 10 meters and an age range of 0 to 0.0117 million years. The second layer is composed of gravel and sand, with a siliciclastic sedimentary lithology and a combination of estuary/bay, outwash plain, and lacustrine indet. depositional environments. It has a thickness of 15 meters and an age range of 0.4398 to 0.8678 million years. This layer also has an economic value as it is composed of sand and gravel, which can be used for construction materials.`

`
`predicted geology description for top 2 layers at location of:  Port Clinton, Ohio  is  

This location is composed of two stratigraphic layers. The upper layer is 0.0117 to 2.58 million years old and is composed of gravel, sand, and clay. The depositional environment is a combination of glacial and lacustrine. The lower layer is 358.9 to 398.6625 million years old and is composed of shale, sandstone, limestone, and dolomite. The depositional environment is mostly inferred marine, with a small portion of the layer being marine. Both layers are sedimentary in nature and provide a record of the geologic history of the area.
`

