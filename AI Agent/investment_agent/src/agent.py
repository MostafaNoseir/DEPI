# src/agent.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

from src.tools import search_web, calculate_difference, write_report
from src.memory import retrieve_strategy

def build_agent():
    llm = ChatOllama(model="llama3.1", temperature=0)

    tools = [
        search_web,
        retrieve_strategy,
        calculate_difference,
        write_report
    ]

    system_prompt = (
        "You are a financial AI analyst.\n"
        "Follow STRICT steps:\n"
        "1. Search for current stock price/news.\n"
        "2. Retrieve internal target price.\n"
        "3. Calculate difference (target - current).\n"
        "4. Write final investment report.\n\n"
        "Rules:\n"
        "- No placeholders.\n"
        "- Always use real values.\n"
        "- Execute tools step-by-step."
    )
    
    # system_prompt = (
    # "You are a financial AI analyst.\n\n"

    # "Follow STRICT steps:\n"
    # "1. Use search_web to find the current stock price.\n"
    # "2. Use retrieve_strategy to get the target buy price.\n"
    # "3. Carefully READ both results and extract the correct numbers.\n"
    # "4. Build a mathematical expression in this EXACT format:\n"
    # "   target_price - current_price\n"
    # "5. Pass ONLY the expression (e.g., '350 - 320') to calculate_difference.\n"
    # "6. Use write_report to save final report.\n\n"

    # "Rules:\n"
    # "- NEVER pass text to calculate_difference.\n"
    # "- ONLY pass a clean math expression.\n"
    # "- Identify correct values using reasoning (ignore historical values).\n"
    # "- If multiple numbers exist, choose:\n"
    # "  • target price from internal docs\n"
    # "  • current price from web search\n"
    # "- Do NOT guess numbers.\n"
    # )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )