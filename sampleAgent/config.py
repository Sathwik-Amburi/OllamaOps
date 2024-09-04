import os
import getpass
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(prompt="Enter OpenAI API Key: ")

    if not os.environ.get("LANGCHAIN_API_KEY"):
        os.environ["LANGCHAIN_API_KEY"] = getpass.getpass(prompt="Enter LangChain API Key: ")
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

    if not os.environ.get("LANGCHAIN_PROJECT"):
        os.environ["LANGCHAIN_PROJECT"] = getpass.getpass(prompt="Enter your LangChain Project: ")
