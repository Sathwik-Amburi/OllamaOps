import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from typing import Dict

@tool
def draw_line_graph(data: Dict[str, float], title: str, xlabel: str, ylabel: str) -> str:
    """Draw a Line Graph"""
    countries = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(15, 10))
    plt.plot(countries, values, marker='o', color="skyblue")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.savefig("line_graph.png")
    plt.close()  # Close the plot to avoid memory issues
    return "Graph has been saved as line_graph.png"

@tool
def draw_pie_chart(data: Dict[str, float], title: str) -> str:
    """Draw a Pie Chart"""
    countries = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 10))
    plt.pie(values, labels=countries, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.savefig("pie_chart.png")
    plt.close()  # Close the plot to avoid memory issues
    return "Graph has been saved as pie_chart.png"
from typing import Dict

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
