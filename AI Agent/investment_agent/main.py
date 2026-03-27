# main.py
import os
from src.agent import build_agent

if not os.path.exists("data"):
    os.makedirs("data")

def main():
    agent = build_agent()

    query = (
        "1. Find the current news and price for Microsoft. "
        "2. Then check our internal strategy docs for our target price. "
        "3. Calculate the difference."
        "4. Write a summary report to 'msft_report.txt'."
    )

    result = agent.invoke({"input": query})

    print("\nFINAL OUTPUT:\n", result["output"])

if __name__ == "__main__":
    main()