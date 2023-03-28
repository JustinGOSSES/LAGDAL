# LAGDAL
It's an acronym.

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

A draft blog post is at `On_LLMs_and_Robot_Roadside_Geologist.md`

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
Our environment dependencies is set by conda. After adding an environmental variable to .bash_profile and running `source ~./bash_profile` it is important to active your conda environment again as it can be easy to forget.

## How to Install

- `git clone https://github.com/JustinGOSSES/LAGDAL.git`
- `cd LAGDAL`
- `pip install requirements.txt` or `conda create --name my_project_env && pip install -r requirements.txt`

## How to Run
- `cd src`
- `python main.py`

## Getting Started

To-Do....

## Contributing

To-Do....


## Early Results

Some examples of predictions for lat/longs are below in order they were created.

There are more `experiments/results_of_tests/experiment_results.json`.

#### Calling Macrostrat API and then using deterministic & LLM semantic functions to summarize the JSON data results into an easily readable format

A few slight variations as trying slightly different prompts. 

`predicted geology description for top 2 layers at location of:  New York City, New York  is  

This location is composed of two stratigraphic layers. The first layer is composed of sand, with a siliciclastic sedimentary lithology and a shoreface marine depositional environment. It has a thickness of 10 meters and an age range of 0 to 0.0117 million years. The second layer is composed of gravel and sand, with a siliciclastic sedimentary lithology and a combination of estuary/bay, outwash plain, and lacustrine indet. depositional environments. It has a thickness of 15 meters and an age range of 0.4398 to 0.8678 million years. This layer also has an economic value as it is composed of sand and gravel, which can be used for construction materials.`

`
`predicted geology description for top 2 layers at location of:  Port Clinton, Ohio  is  

This location is composed of two stratigraphic layers. The upper layer is 0.0117 to 2.58 million years old and is composed of gravel, sand, and clay. The depositional environment is a combination of glacial and lacustrine. The lower layer is 358.9 to 398.6625 million years old and is composed of shale, sandstone, limestone, and dolomite. The depositional environment is mostly inferred marine, with a small portion of the layer being marine. Both layers are sedimentary in nature and provide a record of the geologic history of the area.
`

`
predicted geology description for location of:  New York City, New York  is  

    The top two layers at this location have an age range of 0 to 0.0117 million years and 0.4398 to 0.8678 million years respectively. The top layer is composed of 100% sand and has a depositional environment of 50% shoreface and 50% fluvial indeterminate. The second layer is composed of 14.29% gravel and 85.72% sand and has a depositional environment of 33.33% estuary/bay, 33.33% outwash plain, and 33.33% lacustrine indeterminate. There is a gap of 0.4281 million years between the top two layers.
`

Code for the last result ran from what was in main.py at the time:
```
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
```

----------- More Results ---------------

##### Local point surface geology and regional tectonic story results.

Start with a lat/long location as the input. Gets data from the macrostrat and wikipedia APIs. Uses davinci-003 text models to extract 
from JSON and text, summarize, and combine content so it answers specific questions. 

##### New York, New York, USA
results = []
```
The the point location of:  40.7128 latitude and  -74.006  longitude is located in  39 Park Row, New York, New York 10007, United States

The predicted geology near the surface of that point location of is  
    The top two layers at this location are separated by a gap of 0.3761 million years. The top layer is 0.0117 million years old and is composed of 100% sand with a predicted depositional environment of 50% shoreface and 50% fluvial indet. The second layer is 0.4398 million years old and is composed of 14.29% gravel and 85.72% sand with a predicted depositional environment of 33.33% estuary/bay, 33.33% outwash plain, and 33.33% lacustrine indet. This layer also has an economic value of sand and gravel for construction material.

If we step out to a regional scale and specifically talking about the regional  structural ors tectonic geology  of  New York  :  
The igneous and metamorphic crystalline basement rock of New York formed in the Precambrian and are coterminous with the Canadian Shield. The Adirondack Mountains, Thousand Islands, Hudson Highlands, and Fordham gneiss are part of the Grenville Province. The Avalonian mountain building event 575 million years ago in the Neoproterozoic deformed and metamorphosed the Hudson Highlands and Manhattan Prong. The Taconic orogeny 445 million years ago closed the Iapetus Ocean and caused intense folding, fracturing, thrust faults and large landslides. The Acadian orogeny formed a massive range and rapidly eroded and shed sediments, even as uplift continued. The Peekskill granite intruded between 335 and 320 million years ago. The Alleghanian orogeny around 250 million years ago formed gentle east–west folds in the Alleghany Plateau. The Newark Basin formed beginning 220 million years ago during the late Triassic as Pangea rifted apart. The Fall Zone Peneplain began to be covered by the current sediments of the Atlantic coastal plain beginning in the Jurassic. The Baltimore Canyon Trough is a long basin south of Long Island filled with up to 12 kilometers
```

##### Paris, France 
results = [seems there is missing or different results in API results so LLM results get funky]
```
 The point location of:  48.8566 latitude and  2.3522  longitude is located in  20 Place de l'Hôtel de Ville-Esplanade de la Libération, 75004 Paris, France

The predicted geology near the surface of that point location of is  
    The top two layers at this location are the youngest and oldest layers, with the top layer having a t_age of 0.5 million years and a b_age of 0.3 million years, and the second layer having a t_age of 0.7 million years and a b_age of 0.5 million years. The top layer is composed of 70% lithology and 30% depositional environment, while the second layer is composed of 50% lithology and 50% depositional environment. This indicates a gap of 0.2 million years between the top two layers.

If we step out to a regional scale and specifically talking about the regional  structural ors tectonic geology  of  Île-de-France  :  
France is a country in Western Europe with several overseas regions and territories. It is bordered by Belgium, Luxembourg, Germany, Switzerland, Italy, Monaco, Andorra, and Spain. It is also linked to the United Kingdom by the Channel Tunnel. The extreme points of France are Dunkirk at the North Sea, Perpignan at the Spanish border, Haguenau at the German border, and Brest south of Land's End (England). The highest point of Western Europe is Mont Blanc at 4,810 m (15,781 ft) and the lowest point is Les Moëres at −2.5 m (−8 ft).

France has a variety of geographic features, including glaciers, islands, lakes, mountains, and rivers. The French Alps are a mountain range in the country and the most famous volcano in France is the Puy de Dôme. The major rivers in France are the Loire, the Seine, the Rhône, and the Garonne.

France has a variety of geological features, including sedimentary rocks, metamorphic rocks, and igneous rocks. The sedimentary rocks are mainly limestone, sandstone, and shale. The metamorphic rocks are mainly schist, gne
```

##### Port CLinton, Ohio 
results = [for some reason if you include the country in the wikipedia prompt it gives you a non-geology page ]
```
The point location of:  41.512 latitude and  -82.9377  longitude is located in  230 E 2nd St, Port Clinton, Ohio 43452, United States

The predicted geology near the surface of that point location of is  
    The top two layers at this location are separated by a gap of millions of years. The top layer is 0.0117 million years old and is composed of gravel, sand, and clay in proportions of 48.81%, 44.05%, and 7.14%, respectively. The depositional environment is predicted to be glacial and lacustrine in proportions of 66.67% and 33.33%, respectively. The second layer is 358.9 million years old and is composed of shale, sandstone, limestone, and dolomite in proportions of 37.5%, 12.5%, 31.25%, and 18.75%, respectively. The depositional environment is predicted to be marine and inferred marine in proportions of 6.25% and 93.75%, respectively.

If we step out to a regional scale and specifically talking about the regional  structural ors tectonic geology  of  Ohio  :  
Ohio's geology dates back to the Precambrian eon, with the Grenville Province and Superior Province forming the crystalline basement rock. These two provinces were formed by tectonic events, such as the Taconic orogeny and Acadian orogeny, which occurred during the Paleozoic era. These events caused the formation of sedimentary rocks, which were later uplifted and weathered during the Mesozoic and Cenozoic eras. This process erased most evidence of these periods, but some fossils and plant remains have been found in sediments formed since the Pleistocene. Quarries and road cuts provide the best fossil exposures, allowing geologists to study the structural geology of the region. The Grenville Province and Superior Province are the oldest rocks in Ohio, and were formed by the Taconic orogeny and Acadian orogeny, respectively. These two tectonic events occurred during the Paleozoic era, and caused the formation of sedimentary rocks. During the Mesozoic and Cenozoic eras, the region experienced long-running uplift and weathering, erasing most evidence of these periods. However, some fossils and plant remains have been found in recent sediments formed since the Ple
```

##### San Francisco 
Results = [I ask it to tell how long an unconformity exists between the top and second top most layer, it fails at the math sometimes, so need to use the calculation skill. Also, the doc summarization used to shortern wikipedia page prevents errors but needs to be more sophisticated]
```
The point location of:  37.7749 latitude and  -122.4194  longitude is located in  123 Market St, San Francisco, California 94103, United States

The predicted geology near the surface of that point location of is  
    The top two layers at this location are separated by a gap of 8.7825 million years. The top layer is 0 to 2.58 million years old and is composed of 14.29% gravel, 71.43% sand, and 14.29% clay. This layer is predicted to have been deposited in a fluvial environment. The second layer is 3.345 to 12.1775 million years old and is composed of 2.38% gravel, 2.38% sand, 12.78% siltstone, 12.78% sandstone, 8% conglomerate, 2.67% limestone, 9.38% volcanic, 13.36% andesite, 13.36% basalt, 8.33% ash, and 1.39% tuff. This layer is predicted to have been deposited in a fluvial, estuary/bay, lacustrine, and non-marine environment.

If we step out to a regional scale and specifically talking about the regional  structural ors tectonic geology  of  California  :  
California's geology is complex and dates back 1.8 billion years. It is composed of numerous mountain ranges, faulting and tectonic activity, and rich natural resources. The California Coast Ranges extend from Oregon to Santa Ynez River and are composed of Franciscan subduction complex, shale, limestone, and radiolarian chert. The Klamath Mountains are made up of four terranes, with preserved oceanic crust and a range of rocks from the Cretaceous to modern times. The Modoc Plateau is a large region of lava flows and volcanic rocks.

Tectonic activity in California is evident in the numerous mountain ranges, such as the California Coast Ranges and the Klamath Mountains. The California Coast Ranges are composed of Franciscan subduction complex, shale, limestone, and radiolarian chert, while the Klamath Mountains are made up of four terranes with preserved oceanic crust and a range of rocks from the Cretaceous to modern times. The Modoc Plateau is a large region of lava flows and volcanic rocks.

Faulting is also a major part of California's tectonic geology. Coronado Island in San Diego County was formed
```

##### Banff, Alberta, Canada
results = []
```
The point location of:  51.1784 latitude and  -115.5708  longitude is located in  299 Banff Ave, Banff, Alberta T1L 1E5, Canada

The predicted geology near the surface of that point location of is  
    The top two layers at this location are separated by a gap of millions of years. The top layer is 0-2.58 million years old and is composed of 16.66% gravel, 66.66% sand, and 16.66% silt. This layer was likely deposited in a fluvial or glacial environment. The second layer is 229.5-251.8265 million years old and is composed of 29.17% shale, 45.83% siltstone, 17.86% sandstone, 3.57% limestone, and 3.57% dolomite. This layer was likely deposited in a marine environment.

If we step out to a regional scale and specifically talking about the regional  structural ors tectonic geology  of  Alberta  :  
    Alberta's geology is composed of ancient Precambrian basement rock, overlain by sedimentary rocks containing coal, oil, and natural gas. During the Mesozoic and Cenozoic eras, the North American continent moved westward, leading to the formation of the Guichon Batholith and the Morrison Formation in South Dakota. This tectonic movement caused rivers to shift northward towards the Arctic Ocean, forming the Cretaceous Bullhead and Minnes groups. The Rocky Mountains also caused erosion in Alberta, resulting in the formation of the Blairmore and Manville groups along the edge of the ocean. In the Cenozoic era, sedimentation continued in the Western Canada Sedimentary Basin, with the Paskapoo and Ravenscrag Formations depositing near the Rockies and the Cypress Hills Formation. This tectonic activity has shaped the geology of Alberta, creating a variety of sedimentary rocks and formations that contain valuable resources such as coal, oil, and natural gas.
```

##### Stravger 
results = [Looks like we have at least two problems for Norway, one is that macrostrat has no data, so the LLM makes up stuff. Secondly, wikipedia does not have a geology page for the administrative boundary like in US or Canada.]
```
The point location of:  58.97 latitude and  5.7331  longitude is located in  Domkirkeplassen 1, 4005 Stavanger/Sandnes, Norway

The predicted geology near the surface of that point location of is  
    The top two layers at this location are from the last 2 million years. The top layer is 0.5 million years old and is composed of sandstone with a probability of 70% and siltstone with a probability of 30%. It was deposited in a fluvial environment. The second layer is 1.5 million years old and is composed of shale with a probability of 70% and siltstone with a probability of 30%. It was deposited in a lacustrine environment. There is a gap of 1 million years between the top two layers.

If we step out to a regional scale and specifically talking about the regional  structural ors tectonic geology  of  Rogaland  :  
Preikestolen, or Pulpit Rock, is a 604 metre high cliff located in Rogaland county, Norway. It is composed of a steep cliff face of the Precambrian-age rock of the Folgefonna peninsula. The cliff is a result of tectonic forces that have shaped the landscape over millions of years, and is an example of the folding of the Earth's crust. The cliff is composed of a thick layer of sandstone, which is part of the Devonian-age sandstone formation of the Rogaland Group. The cliff is also an example of the erosion of the Earth's surface, with the cliff face being exposed to the elements over time. The cliff is also an example of the uplift of the Earth's crust, with the cliff face being pushed up by the tectonic forces that have shaped the landscape. The Norwegian authorities have not installed safety devices, as fatalities are rare, and the hike to the top takes around 3-4 hours. The Norwegian authorities have started projects to improve the paths and signs, making it a popular tourist attraction, with around 200,000 visitors a year, and a popular spot for BASE jumpers.
```

-------- results 2023-03-24 --------------

##### Oslo Norway

```
 The point location of:  59.9139 latitude and  10.7522  longitude is located in  Storgata 28, 0184 Oslo, Norway
The predicted geology near the surface of that point location of is  
    The top stratigraphic layer at this location is composed of 18% carbonate and is from the Silurian period, 419.2 million years ago. This layer is part of the Precambrian-Phanerozoic sedimentary rocks. The second layer is composed of 7% phyllite, 14% mudstone, and 83% conglomerate and is from the Cambrian period, 538.8 million years ago. This layer is part of the Cambrian phyllite and is an undifferentiated metamorphic rock.
If we step back and talk about the  regional geologic history  of  Oslo ,  Norway  based on the wikpedia page Geology of Norway :  
Norway's geologic history dates back to the Precambrian era, when the Iapetus Ocean widened and the Varanger ice age began. During the Devonian, Carboniferous, Permian, Triassic, Jurassic, and Cretaceous periods, continental sediments were exposed in various areas of Norway and on Svalbard. The Late Jurassic period was the main rifting phase in the Central Graben, Viking Graben, More Basin, Vøring Basin, and Barents shelf, which caused the land to split apart. Rifting restarted in the late Cretaceous period and continued through to the early Palaeocene period. This rifting created the fjords and valleys that are characteristic of Norway's landscape today. The Caledonian orogeny, which occurred during the Devonian period, also had a significant impact on Norway's geology. This orogeny caused the formation of mountains and hills, and the folding of the Earth's crust. These geological events have shaped Norway's landscape and geology over millions of years.
```

##### Port Clinton, Ohio

```
 The point location of:  41.512 latitude and  -82.9377  longitude is located in  230 E 2nd St, Port Clinton, Ohio 43452, United States
The predicted geology near the surface of that point location of is  
    The top two layers at this location are separated by a gap of millions of years. The top layer is 0.0117 million years old and consists of gravel, sand, and clay with a probability of 48.81%, 44.05%, and 7.14%, respectively. The predicted depositional environment is glacial and lacustrine with a probability of 66.67% and 33.33%, respectively. The second layer is 358.9 million years old and consists of shale, sandstone, limestone, and dolomite with a probability of 37.5%, 12.5%, 31.25%, and 18.75%, respectively. The predicted depositional environment is marine and inferred marine with a probability of 6.25% and 93.75%, respectively.
Created a chunk of size 4084, which is longer than the specified 4000
If we step back and talk about the  regional geologic history  of  Ohio ,  United States  based on the wikpedia page Geological history of North America :  
North America's geologic history dates back to the formation of the Earth. During the Paleozoic era, the region was home to a variety of marine life, amphibians, and early reptiles. The Mesozoic era saw the evolution and dominance of dinosaurs until a mass extinction event. The Cenozoic era saw mammals take over the land and the emergence of whales in the coastal waters. During the Paleozoic era, coral reefs, seed-bearing plants, and the supercontinent Pangaea formed. Fossil footprints of giant insects and salamander-like amphibians have been found in various states. This history of North America's geology is a testament to the diversity of life that has existed in the region over millions of years.
```

##### New York, City
```
The point location of:  40.7128 latitude and  -74.006  longitude is located in  39 Park Row, New York, New York 10007, United States
The predicted geology near the surface of that point location of is  
    The top two layers at this location are separated by a gap of 0.3761 million years. The top layer is 0.0117 million years old and is composed of 100% sand, with a predicted depositional environment of 50% shoreface and 50% fluvial indeterminate. The second layer is 0.4398 million years old and is composed of 14.29% gravel and 85.72% sand, with a predicted depositional environment of 33.33% estuary/bay, 33.33% outwash plain, and 33.33% lacustrine indeterminate. This layer also has an economic value of sand and gravel for construction materials.
Created a chunk of size 6149, which is longer than the specified 4000
Created a chunk of size 4066, which is longer than the specified 4000
Created a chunk of size 4206, which is longer than the specified 4000
Created a chunk of size 4042, which is longer than the specified 4000
Created a chunk of size 4329, which is longer than the specified 4000
If we step back and talk about the  regional geologic history  of  New York ,  United States  based on the wikpedia page Manhattan :  
    Manhattan was historically part of the Lenapehoking territory inhabited by the Munsee Lenape and Wappinger tribes. In 1626, Peter Minuit and Walloon colonists of the West India Company acquired the island of Manhattan from native people for traded goods worth 60 guilders. This marked the beginning of the colonization of Manhattan by the Dutch and later the English. The island of Manhattan was an important part of the Lenapehoking territory, which was home to the Munsee Lenape and Wappinger tribes. The tribes had inhabited the area for centuries before the arrival of the Dutch and English colonists. The acquisition of the island of Manhattan by the West India Company in 1626 marked the beginning of the colonization of the area by Europeans. This colonization led to the displacement of the native tribes and the transformation of the island into the cultural, financial, media, and entertainment capital of the world. The island of Manhattan is now home to the world's two largest stock exchanges, the Metropolitan Museum of Art, and the United Nations, and is the most visited tourist destination in the United States.
```

### 2023-03-27

##### Houston, Texas - 2023-03-27
```
"Greeting my geology 101 students, welcome to our field trip to 903 Bagby St, Houston, Texas 77002, United States! Here, we can observe the geologic history of Texas, which has been shaped by a variety of geological events over millions of years. The top two layers of this area are separated by a gap of 29.525 million years. The top layer is from 0 to 90.825 million years old and is composed of gravel, sand, silt, shale, sandstone, conglomerate, limestone, tuff, and clay, with shale being the most common lithology at 53.99%. The predicted depositional environment is mostly marine, with the most common environment being coastal indet. at 13.56%. The second layer is from 91.8705 to 120.35 million years old and is composed of sand, shale, carbonate, and limestone, with limestone being the most common lithology at 36.51%. The predicted depositional environment is mostly marine, with the most common environment being shallow subtidal at 15.38%. The economic resources in this layer are mostly hydrocarbons, with gas indet. at 66.67% and oil indet. at 33.33%.",
        "date": "2023-03-27 22:15:45"
```

##### Yukon, Alaska - 2023-03-27
```
  "latitude": 64.881183,
    
        "As the professor of Geology 101, I am delighted to introduce the class to the geology of this area. The top two layers here are 0-0.6538 million years old and 61.6-83.6 million years old. The top layer is composed of gravel, sand, silt, and till, each making up 7%, 30%, 58%, and 5% respectively, and is eolian in origin, with dune, loess, fluvial indet., and end moraine each making up 25%. The second layer is composed of sandstone, conglomerate, coal, granite, monzonite, granodiorite, diorite, rhyolite, dacite, and andesite, each making up 7%, 36%, 7%, 3%, 3%, 3%, 3%, 13%, 13%, and 13% respectively, and is marine in origin, with inferred marine making up 100%. Alaska's geologic history is relatively young compared to other parts of North America, with the oldest rocks dating back to the Proterozoic era. During the Mesozoic era, North America separated from the supercontinent Pangea and experienced intense volcanism, leading to the formation of Alaska's mountains. In",
        "date": "2023-03-27 22:23:54"
```

##### Yukon, Alaska - 2023-03-27

```
"Good morning, class. Today we are here to explore the geology of this area. The top two layers of this location are separated by a gap of 22.9 million years. The top layer is 0 to 0.6538 million years old and is composed of gravel, sand, silt, and till in proportions of 7.14%, 29.87%, 58.44%, and 4.54%, respectively. This layer was deposited in a dune, loess, fluvial indet., and end moraine environment in proportions of 25%, 25%, 25%, and 25%, respectively. The second layer is 61.6 to 83.6 million years old and is composed of sandstone, conglomerate, coal, granite, monzonite, granodiorite, diorite, rhyolite, dacite, and andesite in proportions of 7.14%, 35.72%, 7.14%, 2.63%, 2.63%, 2.63%, 2.63%, 13.16%, 13.16%, and 13.16%, respectively. This layer is believed to have been deposited in a marine environment.\n\nAlaska's geology is relatively young compared to other parts of North America, with the oldest",
        "date": "2023-03-27 22:21:32"
    },
```