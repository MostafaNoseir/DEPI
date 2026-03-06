# app/llm_client.py

"""
This module is responsible for:
- Sending prompts + tool schemas to the LLM
- Receiving structured tool calls
- Validating inputs
- Routing execution to backend functions

The LLM NEVER executes code.
It only decides WHAT should be called.
"""

from app.tools import get_weather, update_ticket_status
from app.schemas import TicketUpdate
from app.security import sanitize_string

# Toggle this flag depending on the lab setup
USE_MOCK_LLM = True  # Set to False when Ollama + model are ready

if not USE_MOCK_LLM:
    import ollama


# ----------------------------
# Tool definitions (LLM-visible)
# ----------------------------
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get current weather by city",
        "parameters": {
            "type": "object",  # Named key-value pairs
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "update_ticket_status",
        "description": "Update the status of a support ticket",
        "parameters": {
            "type": "object",  # Named key-value pairs
            "properties": {
                "ticket_id": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["open", "pending", "closed"]  # Whitelist
                }
            },
            "required": ["ticket_id", "status"]
        }
    }
]


# ----------------------------
# Mock LLM (for fast labs)
# ----------------------------
def mock_llm(prompt: str):
    """
    Simulates what a real LLM would output.
    This is NOT fake logic — it mirrors real tool-call JSON.
    """

    prompt_lower = prompt.lower()

    if "weather" in prompt_lower:
        return {
            "tool_calls": [
                {
                    "name": "get_weather",
                    "arguments": {"city": "Cairo"}
                }
            ]
        }

    if "close" in prompt_lower or "update ticket" in prompt_lower:
        return {
            "tool_calls": [
                {
                    "name": "update_ticket_status",
                    "arguments": {
                        "ticket_id": "T-101",
                        "status": "closed"
                    }
                }
            ]
        }

    # No tool needed
    return {"content": "No function call required."}


# ----------------------------
# Main LLM orchestration logic
# ----------------------------
def run_llm(prompt: str):
    """
    Main entry point used by the application.
    """

    # 1. Get response from either real LLM or mock
    if USE_MOCK_LLM:
        response = mock_llm(prompt)
        message = response
    else:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": prompt}],
            tools=TOOLS
        )
        message = response["message"]

    # 2. If the LLM decided to call a tool
    if "tool_calls" in message:
        tool_call = message["tool_calls"][0]
        name = tool_call["name"]
        args = tool_call["arguments"]

        # 3. Route to backend function safely
        if name == "get_weather":
            city = sanitize_string(args["city"])
            return get_weather(city)

        if name == "update_ticket_status":
            # Validate against schema (required fields, enums, types)
            validated = TicketUpdate(**args)

            return update_ticket_status(
                validated.ticket_id,
                validated.status
            )

    # 4. Otherwise, return plain text
    return message.get("content", "")