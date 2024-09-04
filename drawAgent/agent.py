from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Dict
from tools import draw_bar_graph

from database import db, query_as_list
from utils import pretty_print

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Initialize Toolkit and Tools
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

artists = query_as_list(db, "SELECT Name FROM Artist")
albums = query_as_list(db, "SELECT Title FROM Album")

vector_db = FAISS.from_texts(artists + albums, OpenAIEmbeddings())
retriever = vector_db.as_retriever(search_kwargs={"k": 5})
description = """Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
valid proper nouns. Use the noun most similar to the search."""
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

class GraphDataModel(BaseModel):
    data: Dict[str, float] = Field(
        description="Data: a dictionary of str and float values"
    )
    title: str = Field(description="Bar Graph Title")
    xlabel: str = Field(description="X Axis Label")
    ylabel: str = Field(description="Y Axis Label")


system = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.

If the user asks for data analysis, visualization, or trends, follow these steps:
1. Generate a SQL query to retrieve the relevant data.
2. Analyze the data to extract meaningful insights.
3. If the data is suitable for visualization, create a bar graph using the draw_bar_graph tool with the following structure:
{{"data": {{"country1": value1, "country2": value2, ...}}, "title": "Spending by Country", "xlabel": "Amount Spent ($)", "ylabel": "Country"}}.
4. If a bar graph is not possible with the given data, state that it is not possible.

You MUST double-check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

You have access to the following tables: {table_names}

If you need to filter on a proper noun, you must ALWAYS first look up the filter value using the "search_proper_nouns" tool!
Do not try to guess at the proper name - use this function to find similar ones.""".format(
    table_names=db.get_usable_table_names()
)

system_message = SystemMessage(content=system)

tools.append(retriever_tool)
tools.append(draw_bar_graph)

agent = create_react_agent(llm, tools, messages_modifier=system_message)

def run_agent(user_question):
    for s in agent.stream({"messages": [HumanMessage(content=user_question)]}):
        pretty_print(s)
        print("----")
