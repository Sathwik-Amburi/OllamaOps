from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from graph import draw_bar_graph

def create_agent(llm, tools, db):
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
    """.format(table_names=db.get_usable_table_names())

    system_message = SystemMessage(content=system)
    tools.append(draw_bar_graph)

    return create_react_agent(llm, tools, messages_modifier=system_message)
