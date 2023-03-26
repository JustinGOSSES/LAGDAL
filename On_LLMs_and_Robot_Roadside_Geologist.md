# On Large Language Models and Roadside Bot Geologists

## Summary

This document describes how I'm thinking about what large language models and what new capabilities they 
bring to the table for building a roadside geology bot. It describes the challenges of such a product and 
lessons learned building an experimental version using tools like: OpenAI, Langchain, Macrostrat API, 
wikipedia API, etc.

## Premise

Although geology education mostly takes place in the classroom, getting out to see rocks outcropping in 
the real world is a common part of geology training be it in a university or as part of an occupation. 
Listening to someone speak about the details of the rocks in front of them at the side of a cliff, interpreting 
their features, putting them into the regional context, or speaking to them as an excellent example of some concept 
is a core experience shared of geology education. There is an entire collection 
books called "roadside geology of ____ ", because understanding the geology of point locations across a 
transit as a way to understand the larger geological picture is a core experience. Information is organized 
to parallel that experience. 

Of course, to make this experience requires a person knowledgable about the geology of the area, who is already 
familiar with all the stops as well as many others in the area. This person has likely spent considerable time 
researching the geology of the area beforehand as well as time organizing the information into content 
that can be delivered at each stop along the field trip. Available time and knowledge level of the audience is 
typically taken into account when creating the content to be delivered. Such a person is not always available 
though. Sometimes a geologist, or anyone interested in geology, is just driving along in their car, riding a 
train, sitting in a plane, or even not moving and just interested in the geology of one or more points 
on planet Earth. They wish to know about that local rock on the side of the road and how it fits into the 
larger regional context.

> _Can we create a bot that fullfills to some extent the role of the geology field trip leader, at least in terms of 
finding and presenting relevant content to those that wish to hear about it?_

As machine learning, natural language processing, and technology in general continue to improve, it starts
to become more reasonable to think about automating some of this information delivering. This document 
poses the question of how far we are from having an AI geology professor in the field? It attempts to 
identify what do large language models make easier that was previously harder to accomplish and what 
difficult problems remain?

## The context of when was this written

This was written in March of 2023. OpenAI's ChatGPT application and foundational models have created a surge 
in interest and development activity due to their new natural language processing capabilities. 

I've previously done some work and side projects in more traditional natural language processing areas. 
This is my first experiment using pre-built large language models in a side project. Needless to say, I have 
no idea what I'm doing. There's a high chance I'll look back on this writing in 3-12 months and groan, but for now 
it is helping me collect my thoughts.

![Image of a dog at a computer with the words "I have no ideal what I'm doing".](https://i.kym-cdn.com/photos/images/original/000/234/765/b7e.jpg) [RIP Bailey the dog](https://www.reddit.com/r/pics/comments/7oym1s/reddit_you_made_our_dog_semifamous_years_ago_you/)

## The user experiences I aim to build

To user experience I'm trying to build is: 
- The user inputs a latitude and longitude. 
  - This could be via text input form, it could be through you giving your phone's browswer permission to access your location, or it could be through inputting a city, state, and country name that is then geocoded to a point. In all cases, it is a point location.
- The user is told a narrative about the geology at that point. 
  - Initially, the idea is the information involved is: 
    - Geology at the surface at that point.
    - Regional context of that local geology. 

This mirrors in many ways the "real-world" geology field trip experience. Someone tells you about the rocks in front of 
you and then puts them into context.

### Prior art with Macrostrat API and text-to-speech in a simple webpage

I've previously experimented with this sort of idea in an Observable notebook called *["Stratigraphy Speech"](https://observablehq.com/@justingosses/stratigraphy-speech)* that was created shortly before a multi-state road trip. 

> I wanted to have something an automated "road-side geology of ___" book that I could turn on from my phone while driving.

This approach uses no large language model or any other type of natural language processing.

An observable notebook is a website that holds the code and executes it at the same time. The webpage asks for the user's 
location via the location API built into every browswer & permission to play sound. Once it has those, it uses the location to call the [Macrostrat API](https://macrostrat.org/), which returns data in a JSON that describes the top two geologic units at that location. This JSON file is parsed by several different JavaScript functions 
that you can see in the notebook and the resulting inforation is combined with pre-written text into a standard one-size 
fits all narrative. That narrative is then spoken to the user via browser's text-to-speech capabilities, which all 
browsers now have but are rarely used.

The end effect is a webpage you can give permissions for in advance and then open later. Upon pushing one 
button, it will tell you about the geologic unit at the surface at that location.

#### Limitations of this approach

Upon using this, there are a few limitations that quickly become obvious. First, due to the narrative being one-size fits 
all and deterministically created from well structured data, it can get kind of boring to hear again and again. Even if the 
units age and lithology vary, all of the glue words stay the same every single time you try to get information. Second, 
there is not regional information of contextual information. All you get is what the API gives you, which is lithology, age, and maybe interpreted depositional environment, all data originally extracted from a geologic map.


## The problem of trying to scale creating geological narratives from data APIs.
Ideally, you'd be able to not just get an individual point location data read back to you in a single construction. You would also get regional geology, historical narrative, information on what is unique, etc. The content you want as 
narrative could reasonably vary, just like actual field trips. There are a variety of other variations in what information 
is provided, how it is provided, and how the user interacts with it that quickly start to pile up if you want to make 
something useful and pleasant to use.

Types of variations in the information that might be desired:
- Short summary vs long with details
- Point-based information vs. regional-based information
- General information vs. sub-field specific
- For general audience vs. for expert audience

Types of interactions with information
- one-way or chat
- statement vs. question & answer
- text or speech

To do all this with deterministic traditional programming becomes both complex and tedious rather quickly. 
Well structured standarized sources of information must be located, assuming they exist. Often times, they don't exist. 
Where they do exist, many different functions must be written for each new piece of well-structured information and 
each new way to present that information. 

> Using traditional deterministical coding to programmatically create narratives from data APIs becomes too laborious quickly unless all the information needed is already very well structured in a finite number of known places and the 
number of ways people want to interact and hear about that information is limited.

## What Large Language Models Offer
Large language models (LLM) offer an improvement on this experience. Their outstanding ability to predict reasonable sounding 
next words given a prompt enables them to do a variety of tasks directed by plain instructions, also known as "prompts".

Because they are good at predicting the next words given a sequence, they can do the following tasks:

### Skilled summarization
LLM can summarize three pages of text into a single paragraph. They can also summarize text with a focus on specific 
types of content or in a specific style of writing or speaking.

### Flexible extraction 
LLM can extract keywords, concepts, and specific information from text. When my previous team at NASA created a model to predict topic tags against abstracts and READMEs, it required a pre-existing dataset of millions of labeled abstracts 
and months of training and evaluating different models. Now you can get comparable performance from an OpenAI model without 
having to do any of the data preparation or training yourself. Additionally, you can just provide a list of possible 
tags in the prompt, or none at all, and it returns useful predictions. It is serious jump in capabilities compared to 
what existing one or two years ago. 

### General knowledge....to some extent
Althogh LLMs are infamous for making up things that sound right, they can also return general knowledge accurately at 
times. Figuring out when to trust such information evolves a lot of trial and error before you can be confident of 
accuracy for a given request. 

As an example, if you just ask ChatGPT to "Describe the geology of [insert a city]", the answer it gives varies in accuracy. For Port Clinton, Ohio, it tends to be do well, perhaps becaues the only writing that involves both "Geology" and "Port Clinton, Ohio" is about the geology of Port Clinton. In constrast, the same question for Houston, Texas gets 
some information wrong. The formation ages given are common formations to be discussed where the world "Houston" is used 
but not actually the top two formations.

As supurb prediction machines LLMs can give inaccurate information when the most common text that shares the words in the 
prompt isn't exactly what the prompt is asking. Other times, it seems there likely isn't anything in its training that relates to the question in prompt.

> To get around these knowledge limitations, we can combine LLMs with geologic data APIs and easily searchable text 
on the subjects requested in the prompt. We can also use cleaning and validation functions to figure out what information 
might be more trustworthy or relate the most to the given question.

## Large Language Model Techniques
By combinging determnistitic APIs, LLMs API calls with different prompts, and various validation and data cleaning 
functions we can create "chains" that get around some of the limitations of using just deterministic approaches or 
just LLM approaches. 

For more about "agents", "chains", and other concepts, check out the documentation for [Lanchain](https://python.langchain.com/en/latest/) or [Semantic-Kernal](https://devblogs.microsoft.com/semantic-kernel/), two libraries for calling OpenAI-type model APIs.

## Where to get data and what to do with it


### Chains


### Agents


### Rule-based Functions


### Prompt-based Functions


### MacroStrat: and other well-structured sources of relevent information


### Wikipedia: and other semi-structured sources of relevant information


### Bing Search: and other unstructured sources of relevant information



### Literature 



## Current experiments on part of a weekend



### Learnings from current experiments

TODO

Main benefit is in changing slope of the developer labor vs. product functionality curve.


## What is still hard

TODO

1. Figuring out what is "good" is hard programmatically and as a human
2. Limited number of places to pull well structured data or text

## What might be in near-future


### Other directions to go besides the give me geology for this point application