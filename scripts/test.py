import os
import ast
import re
import asyncio
import json
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from typing import Dict
from langchain_community.utilities import SQLDatabase
import ollama

# Load environment variables from .env file
load_dotenv()

# Database setup
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# Prompt user for a question
user_question = input("Please enter your question: ")

# Function to execute SQL queries
def query_as_list(query: str):
    res = db.run(query)
    # Ensure all elements are strings before applying regex and other operations
    res = [str(el) for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

# Function to draw a bar graph
def draw_bar_graph(data: Dict[str, float], title: str, xlabel: str, ylabel: str) -> str:
    items = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(15, 10))
    plt.barh(items, values, color="skyblue")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.savefig("bar_graph.png")
    plt.close()  # Close the plot to avoid memory issues
    return "Graph has been saved as bar_graph.png"

# Ollama client interaction
async def run_ollama():
    client = ollama.AsyncClient()

    # Initial system message
    system_message = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
    If the user asks for data analysis, visualization, or trends, follow these steps:
    1. Generate a SQL query to retrieve the relevant data.
    2. Analyze the data to extract meaningful insights.
    3. If the data is suitable for visualization, create a bar graph using the draw_bar_graph tool."""

    # Define the messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_question}
    ]

    # Define the available tools
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'query_as_list',
                'description': 'Execute a SQL query and return a list of results',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {'type': 'string', 'description': 'The SQL query to execute'}
                    },
                    'required': ['query'],
                },
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'draw_bar_graph',
                'description': 'Draw a Bar Graph',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'data': {'type': 'object', 'description': 'Data to plot'},
                        'title': {'type': 'string', 'description': 'Graph Title'},
                        'xlabel': {'type': 'string', 'description': 'X Axis Label'},
                        'ylabel': {'type': 'string', 'description': 'Y Axis Label'},
                    },
                    'required': ['data', 'title', 'xlabel', 'ylabel'],
                },
            }
        }
    ]

    # Initial chat interaction with tool calling
    response = await client.chat(model="llama3.1", messages=messages, tools=tools)

    # Check if the model decided to use a function
    if response.get('message').get('tool_calls'):
        for tool_call in response['message']['tool_calls']:
            function_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']

            if function_name == 'query_as_list':
                tool_response = query_as_list(arguments['query'])
            elif function_name == 'draw_bar_graph':
                # Filter out unexpected parameters before calling the function
                valid_args = {k: arguments[k] for k in ['data', 'title', 'xlabel', 'ylabel']}
                tool_response = draw_bar_graph(**valid_args)

            # Add tool response to the conversation
            messages.append({'role': 'tool', 'content': json.dumps(tool_response)})

        # Get the final response
        final_response = await client.chat(model="llama3.1", messages=messages)
        print(final_response['message']['content'])
    else:
        print(response['message']['content'])

# Run the async function
asyncio.run(run_ollama())
