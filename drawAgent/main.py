from config import *
from agent import run_agent

# Prompt user for a question
user_question = input("Please enter your question: ")

# Run the agent with the user's question
run_agent(user_question)
