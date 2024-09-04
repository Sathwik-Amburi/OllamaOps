import getpass
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Prompt user for OpenAI API Key if not set
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass(prompt="Enter OpenAI API Key: ")

# Prompt user for LangChain API Key if not set
if not os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = getpass.getpass(
        prompt="Enter LangChain API Key: "
    )
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Prompt user for LangChain Project if not set
if not os.environ.get("LANGCHAIN_PROJECT"):
    os.environ["LANGCHAIN_PROJECT"] = getpass.getpass(
        prompt="Enter your Langchain Project: "
    )
