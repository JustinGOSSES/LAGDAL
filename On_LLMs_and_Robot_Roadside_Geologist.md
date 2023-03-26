# On Large Language Models and Roadside Bot Geologists

## Summary

Although geology education is largely classroom-based, geology field trips are a common shared experiece that 
makes up an important part of geology education. The experience of standing beside a cliff face while someone 
expertly points out the subtle details of the rock formations, contextualizing them within the broader regional 
geology, and using them as examples to illustrate fundamental geological concepts is a quintessential part of 
geology education. In fact, there exists an entire genre of books called "roadside geology of ____" that 
capitalize on the idea of using point locations along a route to build a larger understanding of geological 
phenomena. The information in these books is often presented in a manner that mirrors the traditional field 
trip experience.

Usually, someone with deep knowledge of the area is needed to lead these excursions, 
as they are familiar with the stops along the way and have spent countless hours researching and organizing 
the information to be delivered at each stop. This includes accounting for the audience's level of knowledge 
and the time available to deliver the content. However, there are times when such a knowledgeable guide 
is not available. Perhaps a geologist, or simply someone with an interest in geology, is driving along a road 
or looking at a map and wishes they had access to information about the local geology and its broader context. 

> Is it possible to create a bot that can take on at least some of the role of a field trip leader, by 
finding and presenting relevant geological information to those who seek it?

As technology continues to improve, with advancements in machine learning and natural language processing, 
it becomes increasingly plausible to automate information delivery in this way. 
This document poses the question of whether we are approaching the day when an AI geology professor can 
at least provide an introductury statement that might be delivered at the beginning of a field trip stop. 

> This document explores the ways in which large language models make it easier to accomplish certain tasks that were 
once impossible to do programmatically, while also highlighting the challenges that remain.

## The context of when was this written

This was written in March of 2023. 
The tech community has been swept up by a surge of interest and activity, 
fueled in part by the incredible capabilities of OpenAI's ChatGPT application and its foundational models.

While, I've previously done some work and side projects in more traditional natural language processing areas, 
this is my first experiment using pre-built large language models in a side project. Needless to say, I have 
no idea what I'm doing. There's a high chance I'll look back on this writing in 3-12 months and groan, but for now 
it is helping me collect my thoughts.

![Image of a dog at a computer with the words "I have no ideal what I'm doing".](https://i.kym-cdn.com/photos/images/original/000/234/765/b7e.jpg) [RIP Bailey the dog](https://www.reddit.com/r/pics/comments/7oym1s/reddit_you_made_our_dog_semifamous_years_ago_you/)

## The user experiences I aim to build

To user experience I am trying to build is: 
1. The user inputs a latitude and longitude. 
  - This could be via text input form, it could be through you giving your phone's browswer permission to access your location, or it could be through inputting a city, state, and country name that is then geocoded to a point. In all cases, it is a point location.
2. The user is told a narrative about the geology at that point. 
  - Initially, the idea is the information involved is: 
    - Geology at the surface at that point.
    - Regional context of that local geology. 

This mirrors in many ways the "real-world" geology field trip experience. Someone tells you about the rocks in front of 
you and then puts them into context.

### Prior art with Macrostrat API and text-to-speech in a simple webpage

I've previously experimented with this sort of idea in an Observable notebook called *["Stratigraphy Speech"](https://observablehq.com/@justingosses/stratigraphy-speech)* that was created shortly before a multi-state road trip. 

> I wanted to have something an automated "road-side geology of ___" book that I could turn on from my phone while driving.

This approach uses no large language model or any other type of natural language processing. It calls a singular API 
with a point location and parses the data it gets in response.

An observable notebook is a website that holds the code and executes it at the same time. The webpage asks for the user's 
location via the location API built into every browswer & permission to play sound. Once it has those, it uses the location to call the [Macrostrat API](https://macrostrat.org/), which returns data in a JSON that describes the top two geologic units at that location. This JSON file is parsed by several different JavaScript functions 
that you can see in the notebook and the resulting inforation is combined with pre-written text into a standard one-size 
fits all narrative. That narrative is then spoken to the user via browser's text-to-speech capabilities, which all 
browsers now have but are rarely used.

The end effect is a webpage you can give permissions for in advance and then open later. Upon pushing one 
button, it will tell you about the geologic unit at the surface at that location.

#### Limitations of this approach

Upon using this, there are a few limitations that quickly become obvious. First, due to the narrative being one-size fits 
all and deterministically created from well structured data, it can get kind of boring to hear again and again as you 
drive down the road. Even if the 
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