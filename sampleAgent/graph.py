import matplotlib.pyplot as plt
from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Dict

class GraphDataModel(BaseModel):
    data: Dict[str, float] = Field(description="Data: a dictionary of str and float values")
    title: str = Field(description="Bar Graph Title")
    xlabel: str = Field(description="X Axis Label")
    ylabel: str = Field(description="Y Axis Label")

@tool
def draw_bar_graph(data: Dict[str, float], title: str, xlabel: str, ylabel: str) -> str:
    """Draw a Bar Graph"""
    countries = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(15, 10))
    plt.barh(countries, values, color="skyblue")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.savefig("bar_graph.png")
    plt.close()  # Close the plot to avoid memory issues
    return "Graph has been saved as bar_graph.png"
