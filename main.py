from config import load_env_variables
from database import db, query_as_list
from llm import initialize_llm, initialize_tools
from agent import create_agent
from utils import pretty_print
from langchain_core.messages import HumanMessage

# Load environment variables
load_env_variables()

# Initialize Database
artists = query_as_list(db, "SELECT Name FROM Artist")
albums = query_as_list(db, "SELECT Title FROM Album")

# Initialize LLM and Tools
llm = initialize_llm()
tools = initialize_tools(llm, db, artists, albums)

# Create and run the agent
agent = create_agent(llm, tools, db)

# Prompt user for a question
user_question = input("Please enter your question: ")

# Process the question
for s in agent.stream({"messages": [HumanMessage(content=user_question)]}):
    pretty_print(s)
    print("----")
