# LAGDAL
It's an acronym.

LLM Assisted Geology Descriptions of Arbitrary Locations = LAGDAL

This is currently an experiment on the weekends when I have a little time type of thing.

*Update: latest experimental results with agent can be found here: https://justingosses.github.io/LAGDAL/experiments/ *

#### Try it live: https://app-lagdal.azurewebsites.net/ 

#### Try website with only front-end: https://justingosses.github.io/LAGDAL/frontend/

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

## Should I trust this?

No. 

All models are wrong. Geologic maps and large language models (LLM) are different types of models. They are both going to have inaccuracies. Additionally, the information you want to be told may not be what they have to provide. This is a global geologic map, so there is A LOT of lumping things together. Significant real variation in geology will not be shown on it. As an example, my masters work was on volcanic and sedimentary deposits in a 27 kilometer-wide Eocene-age caldera in south western Argentina. The entirity of that huge geologic feature is not shown on the geologic map being used and does not get described in most versions of the generative field trip stop description. Large language models by themselves are not thinking, doing logic, or referring back to a database of facts. They are really good at predicting the next sequence of words like how certain humans would write them. This is an amazingly useful skill that a large number of capabilities can be built upon. However, it also leads to certain types of flaws that are not always easy to detect. It is important to always keep this in mind when interpreting results or writing code that calls large language models. By grounding large language models in real data, we can limit some of their flaws. Informed skepticism of the result is very useful.

I think this might be a useful starting point for quick insights into surface bedrock geology, that should then be followed up with more research when accuracy is even a little important. As someone who no longer does geology as their job, I can see myself using it on vacations when I'm curious about that rock outcrop we passed on the train. If you would like to read more writing about what might be possible and goals of the project, check out this blog post.

If you see something that the field trip stop description gets wrong, please report it via the "Fact Wrong" issue template. It is helpful to collect examples of where errors occur. There is no implied promise to improve any specific failing, however, as this is just a weekend side project to learn and see what is possible. 

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
- wikipedia (not being used in later attempts)

### Needs API Keys
- [Bing Maps Geocoding API](https://learn.microsoft.com/en-us/bingmaps/rest-services/locations/)

#### OpenAI
- [OpenAI](https://platform.openai.com/docs/introduction) key as environmental variable

#### Bing Maps API 
- READ: https://www.microsoft.com/en-us/maps/create-a-bing-maps-key
- Set up bing maps key, which is free for certain number of geocoding calls

This is used to find city, county, state, country, etc. from lat/long and the inverse.

#### NOTE
In this repository, we've set the keys as environmental variables. How exactly you do that depends on Operating System and preference. 
Our environment dependencies is set by conda. 

_Reminder for Justin_......After adding an environmental variable to .bash_profile and running `source ~./bash_profile` it is important to active your conda environment again as it can be easy to forget.

## How to Install 

- `git clone https://github.com/JustinGOSSES/LAGDAL.git`
- `cd LAGDAL`
- `pip install requirements.txt` or `conda create --name my_project_env && pip install -r requirements.txt`

## How to Python Scripts Run locally
- `cd src`
- `python main.py`

or 

- `cd src`
- `python agentE.py "Paris, France"`

## How to Run Flask App that stands up full front-end & back-end application
- from top directory, run in terminal `flask run` or if you need more debugging information `Python app.py`. 
- Go to the the address shown in the terminal in a browser, usually: `http://127.0.0.1:5000`.

#### Try it live: https://app-lagdal.azurewebsites.net/ 


The first approach uses a fixed chain of prompts & APIs. The second approach uses an agent that decides which "tools" to 
call where each "tool" is a prompt or a deterministic API call.

## Getting Started

This is a very hacky weekend project, so there's currently not much in the way of docs or instructions. Think of it as a proof-of-concept. 

### Folder Structure
- Experiments: prediction outputs from local text prediction experiments
- frontend: place for front-end code experimentation and prototypes. Development has moved to `templates` and `static` for the flask app.
- images: folder for images used in markdown files
- notebooks: quick experimentation has taken place in notebooks. There are no reusable notebook templates.
- src: most of the python code that calls the various APIs is in this folder
  - The various top-level files are what is meant to be called. `main.py` is the eariest version, then `agentA.py` through E.
  - The file `agent_website_explore.py` is what is called by the Flask app that is live at: https://app-lagdal.azurewebsites.net/
  - The native_skills folder holds various scripts that calls APIs like macrostrat and bing.
- static: holds the front-end CSS and JavaScript code used in the Flask app. 
- templates: Holds the HTML files used in the flask app. 
- app.py: Runs the flask app deployed to Azure Web Applications.

## Contributing

Open to contributions from others, but have not had any yet. 
As a prototype playground, the organizational structure and code quality is very poor right now.
 Please file issues and pull-requests. See the issues for ideas of how this prototype can be built upon by others either here or in your projects.

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








