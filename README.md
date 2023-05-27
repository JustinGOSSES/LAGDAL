# LAGDAL
It's an acronym.

LLM Assisted Geology Descriptions of Arbitrary Locations = LAGDAL

This is currently an experiment on the weekends when I have a little time type of thing.

*Update: latest experiments with agent can be found here: https://justingosses.github.io/LAGDAL/experiments/ *

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

A draft blog post is at [On_LLMs_and_Robot_Roadside_Geologist.md](https://github.com/JustinGOSSES/LAGDAL/blob/main/On_LLMs_and_Robot_Roadside_Geologist.md)

## High-Level Summary of Skills
The following outline of potential semantic skills and deterministic functions are what is imagined might be necessary.

### Macrostrat
Data for a given lat/long and either at surface, 2nd layer down, or strat column going downwards.
- age
- lithologies
- depositional environment
- fossils (optional)

#### Macrostrat specific semantic functions
- convert from API's JSON data into words
    - summary of top two layers only
    - Might include some code that ignores any layers very young and very thin as likely dirt?ss

### Wikipedia 
- geology of ___ country
- geology of ____ state in USA, or state/provience in other country, or region of country

*Note: no longer using Wikipedia data in most recent scripts but functionality still in the code.

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

## Early Narrative Goals
_For a given latitude and longitude on land, generate a paragraph that roughly contains...._

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

## Required Tooling
All dependencies are in the requirements.txt file. 

The main top-level dependencies are:
- langchain
- open_ai
- requests
- wikipedia

### Needs API Keys
- [Bing Maps Geocoding API](https://learn.microsoft.com/en-us/bingmaps/rest-services/locations/)

#### OpenAI
- [OpenAI](https://platform.openai.com/docs/introduction) key as environmental variable

#### Bing Maps API 
- READ: https://www.microsoft.com/en-us/maps/create-a-bing-maps-key
- Set up bing maps key, which is free for certain number of geocoding calls

This is used to find city, county, state, country, etc. from lat/long and the inverse.

#### NOTE
In this repository, we've set there keys are environmental variables. How exactly you do that depends on Operating System and preference. 
Our environment dependencies is set by conda. 

_Reminder for Justin_......After adding an environmental variable to .bash_profile and running `source ~./bash_profile` it is important to active your conda environment again as it can be easy to forget.

## How to Install

- `git clone https://github.com/JustinGOSSES/LAGDAL.git`
- `cd LAGDAL`
- `pip install requirements.txt` or `conda create --name my_project_env && pip install -r requirements.txt`

## How to Run
- `cd src`
- `python main.py`

or 

- `cd src`
- `python agentA.py "Paris, France"`

The first approach uses a fixed chain of prompts & APIs. The second approach uses an agent that decides which "tools" to 
call where each "tool" is a prompt or a deterministic API call.

## Getting Started

This is a very hacky weekend project, so there's currently no docs or instructions. Think of it as a proof-of-concept. 

## Contributing

To-Do.... Currently, the organizational structure is so poor that it isn't really suited for collaboration with others yet.


## Experimental Results

#### See Experimental Results Over Time
For recent results over time, check out [https://justingosses.github.io/LAGDAL/experiments/](https://justingosses.github.io/LAGDAL/experiments/) to see experimental results in a webpage built from experiments JSONs. This link goes to a GitHub pages page, so it only covers what has been saved to an experiment JSON and pushed to the GitHub repository. 

#### To See Local Results
To see results from the last runs, check out the index.html file in experiments directory. 
You can stand this up by running `python -m http.server` in the top level folder and then navigating to 
[http://localhost:8000/experiments/](http://localhost:8000/experiments/)

#### Early Results Before Started to Keep Track in JSONs
To see early results before I started to keep track of them in JSONs, check out a markdown file where I copied some of them.

[/experiments/results_of_tests/early_results_before_exporting_to_JSONs.md](/experiments/results_of_tests/early_results_before_exporting_to_JSONs.md)

### Example of Improving Field Trip Stop Descriptions Over Time

#### First Attempts

`predicted geology description for top 2 layers at location of:  New York City, New York  is  

This location is composed of two stratigraphic layers. The first layer is composed of sand, with a siliciclastic sedimentary lithology and a shoreface marine depositional environment. It has a thickness of 10 meters and an age range of 0 to 0.0117 million years. The second layer is composed of gravel and sand, with a siliciclastic sedimentary lithology and a combination of estuary/bay, outwash plain, and lacustrine indet. depositional environments. It has a thickness of 15 meters and an age range of 0.4398 to 0.8678 million years. This layer also has an economic value as it is composed of sand and gravel, which can be used for construction materials.`

`
`predicted geology description for top 2 layers at location of:  Port Clinton, Ohio  is  

This location is composed of two stratigraphic layers. The upper layer is 0.0117 to 2.58 million years old and is composed of gravel, sand, and clay. The depositional environment is a combination of glacial and lacustrine. The lower layer is 358.9 to 398.6625 million years old and is composed of shale, sandstone, limestone, and dolomite. The depositional environment is mostly inferred marine, with a small portion of the layer being marine. Both layers are sedimentary in nature and provide a record of the geologic history of the area.
`

### Later Attempts

New York City, New York, USA:
`
RESPONSE: The uppermost surface geology at the local point location at center of New York City, New York, USA is the Manhattan Formation, undivided. It is composed of 79% pelitic schist, 84% gneiss, and 86% amphibolite. It is estimated to have been deposited between 538.8 and 458.4 million years ago, during the Early Cambrian and Middle Ordovician eras, respectively. The predicted depositional environment for this unit is eugeosynclinal rocks thrust upon Oma.,Now stepping back to talk about the regional geology around this area, the geologic story around New York City is quite complex and spans over millions of years. The youngest uppermost rocks in the area are from the Paleozoic Era, specifically the Ordovician Period, which lasted from 485.4 to 443.8 million years ago. During this time, the area was covered by a shallow sea, and sedimentary rocks such as sandstone, shale, and limestone were deposited. The next period, the Silurian, lasted from 443.8 to 419.2 million years ago, and saw the formation of more limestone and shale. The Devonian Period, from 419.2 to 358.9 million years ago, saw the formation of sandstone, shale, and conglomerate rocks. During the Carboniferous Period, from 358.9 to 298.9 million years ago, the area was covered by a swampy forest, which eventually became coal deposits. The Permian Period, from 298.9 to 252.2 million years ago, saw the formation of red sandstone and conglomerate rocks. 
 `

Port Clinton, Ohio, USA:
`
The uppermost surface geology at the local point location at center of Port Clinton, Ohio, USA is the Salina Group, which is composed of 8% dolostone, 31% shale, 36% anhydrite, and 37% gypsum. This unit is from the Silurian period, with an age range of 443.8 to 419.2 million years ago. The depositional environment of this unit is unknown. The second layer is composed of sedimentary rocks from the Paleozoic period, with an age range of 538.8 to 251.902 million years ago. This unit is composed of 100% sedimentary rocks and the depositional environment is unknown.,Now stepping back to talk about the regional geology around this area, the youngest rocks in this area are from the Silurian Period, which lasted from 443.8 to 419.2 million years ago. During this time, the area was covered by a shallow sea, and sedimentary rocks such as limestone, shale, and sandstone were deposited. These rocks are important for their fossil content, which includes brachiopods, trilobites, and crinoids. The Silurian rocks in this area are part of the Lockport Group, which is known for its distinctive fossil-rich layers. The Lockport Group is also important for its oil and gas reserves, which have been extracted from the rocks for many years. Overall, the geology of Port Clinton and the surrounding area is a fascinating record of ancient seas and the life that once inhabited them.
`








