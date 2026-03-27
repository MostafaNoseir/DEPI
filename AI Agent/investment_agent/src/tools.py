# src/tools.py
import os
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def search_web(query: str) -> str:
    """Search for stock price, company news, or financial updates."""
    search = DuckDuckGoSearchRun()
    try:
        return search.invoke(query)
    except Exception as e:
        return f"Search error: {str(e)}"

@tool
def calculate_difference(expression: str) -> str:
    """
    Calculate difference between target price and current price.
    """
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"

@tool
def write_report(filename: str, content: str) -> str:
    """Write final investment report to a file."""
    try:
        filepath = os.path.join("data", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report saved to {filepath}"
    except Exception as e:
        return f"Write error: {str(e)}"