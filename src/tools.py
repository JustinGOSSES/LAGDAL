from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent, tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool

from langchain.chains import LLMChain
from langchain.llms import OpenAI

from util import append_experiment_results

from prompts import promptCombineAndRewordInStyle, promptIsThisAbout, promptGeologicalRegions, promptLocationWithinRegions

from prompts import promptDecideIfCountySmall, promptCombineAndRewordInStyleB

### functions functions
from native_skills.macrostrat.macrostrat import getPointLocationStratColumn, macrostratOnlyReturnFirstTwoLayers, macrostratOnlyReturnFirstLayer, ifNoSurfaceGeology
#### macrostrat prompts
from native_skills.macrostrat.macrostrat import macroStratColSummarizationTop, macroStratColSummarizationSecondMostLayer, macroStratColSummarization, macroStratColSummarizationWhenNoColumn

from native_skills.bing.geocoding import getStateAndCountyFromLatLong, getAddressFromLatLong

from native_skills.wikipedia.wikipedia import getWikipediaPageAndProcess, extractContentFromWikipediaPageContent

# llm = ChatOpenAI(temperature=0)
# llm = OpenAI(model_name="text-davinci-003",temperature=0.2, max_tokens=256)
llm = OpenAI(model_name="text-davinci-003",temperature=0.2)

llm_math_chain = LLMMathChain(llm=llm, verbose=True)



#### from main
# from main import macrostratGeologyForLocation

def getMacroStratAPIBasic(latLong:str):
    a, b = latLong.split(",")
    macrostrat_column_json  = getPointLocationStratColumn(float(a),float(b))
    #return macrostrat_column_json
    return macrostratGeologyForLocation(macrostrat_column_json)
                                

def macrostratGeologyForLocation(macrostrat_column_json):
    # macrostrat_column_json = getPointLocationStratColumn(latitude,longitude)
    if macrostrat_column_json == "No stratigraphic column data available for this location.":
        #print("No stratigraphic column data available for this location of: ",latitude,longitude, " so we will try to get surface geology data.")
        macrostrat_map_json = ifNoSurfaceGeology(latitude,longitude)
        #print("macrostrat_map_json map geologic data is",macrostrat_map_json)
        #### Using prompt for map data when there is no stratigraphic column data
        chainMacroStratWhenNotColum = LLMChain(llm=llm, prompt=macroStratColSummarizationWhenNoColumn)
        response = chainMacroStratWhenNotColum.run(macrostrat_map_json)
        
    else:
        #print("Found a stratigraphic column data available for this location of. ",latitude,longitude)
        macrostrat_column_json = macrostratOnlyReturnFirstTwoLayers(macrostrat_column_json)
        #### Using prompt for stratigraphic column data
        chainMacroStrat = LLMChain(llm=llm, prompt=macroStratColSummarization)
        response = chainMacroStrat.run(macrostrat_column_json)
        
    return response



# You can also define an args_schema to provide more information about inputs
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    query: str = Field(description="should be a math expression")
        
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="Useful for when you need to answer questions about math",
        # args_schema=CalculatorInput
    ),
]

tools.append(
    Tool(
        name="Macrostrat-Geology-For-Location",
        func=getMacroStratAPIBasic,
        description="""
        Useful for finding a description the top two layers of the stratigraphic column for a given point location.
        The input to this tool should be a comma separated list of numbers of length two,representing latitude and longitude. 
        For example, `40.7128,-74.0060` would be the input for a location at latitude 40.7128 and longitude -74.0060
        """,
    )
)


agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# agent.run("""
#           Get the latitude and longitude of Port Clinton, Ohio and 
#           tell me the geology of that location, 
#           if there is any age gap between the top two layers, 
#           and how that local geology fits into regional geologic story.
#           Do so as if you are talking to students on a geology field trip looking at an outcrop.
#           """)

# agent.run("""
#           Get the latitude and longitude of Port Clinton, Ohio.
#           Is there any volcanic rocks there?
#           """)

# agent.run("""
#           Get the latitude and longitude of Houston, Texas.
#           Is there any sedimentary rocks there?
#           """)

### This one does not work out well!
# agent.run("""
#           Get the latitude and longitude of Olso, Norway and the local geology.
#           Determine the age of any rocks there that are metamorphic.
#           """)

agent.run("""
          Get the latitude and longitude of Estes Park, Colorado and 
          tell me the geology of that location, 
          and how the local geology fits into regional geologic story of Colarado.
          """)