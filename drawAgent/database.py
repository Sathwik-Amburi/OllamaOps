from langchain_community.utilities import SQLDatabase

# Load Database
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

def query_as_list(db, query):
    import ast
    import re

    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))
