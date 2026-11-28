

import json
import requests

from llm_service import MODEL_NAME
from tool_definitions import TOOLS
from fintech_tools import execute_tool


OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """
You are a FinTech AI assistant.

You can answer general questions and use the available
banking tools to retrieve account and transaction information.

Rules:
1. Use tools when the user asks for account or transaction information.
2. Never invent account balances or transaction details.
3. Use only the information returned by the Python tools.
4. After receiving tool results, explain them clearly.
5. If a tool returns an error, communicate that error to the user.
"""


# --------------------------------------------------
# NODE 1: AGENT NODE
# --------------------------------------------------

def agent_node(state):

    print("\n========== AGENT NODE ==========")

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + state["messages"]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS,
        "stream": False
    }

    response = requests.post(
        OLLAMA_CHAT_URL,
        json=payload,
        timeout=(10, 300)
    )

    response.raise_for_status()

    response_data = response.json()

    assistant_message = response_data.get("message", {})

    print("Agent received Ollama response.")

    if assistant_message.get("tool_calls"):
        print("Agent requested tool execution.")
    else:
        print("Agent generated a normal response.")

    return {
        "messages": [assistant_message],
        "workflow_status": "processing"
    }


# --------------------------------------------------
# NODE 2: TOOL EXECUTION NODE
# --------------------------------------------------

def tool_node(state):

    print("\n========== TOOL EXECUTION NODE ==========")

    messages = state["messages"]

    last_message = messages[-1]

    tool_calls = last_message.get("tool_calls", [])

    tool_messages = []

    last_tool_result = None

    for tool_call in tool_calls:

        function_data = tool_call.get("function", {})

        tool_name = function_data.get("name")

        arguments = function_data.get("arguments", {})

        print(f"Executing tool: {tool_name}")
        print(f"Arguments: {arguments}")

        try:

            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments must be a dictionary.")

            result = execute_tool(
                tool_name,
                arguments
            )

        except Exception as exc:

            result = {
                "error": str(exc)
            }

        last_tool_result = result

        tool_messages.append({
            "role": "tool",
            "tool_name": tool_name,
            "content": json.dumps(result)
        })

        print("Tool execution completed.")

    return {
        "messages": tool_messages,
        "tool_calls_count": (
            state.get("tool_calls_count", 0) +
            len(tool_calls)
        ),
        "last_tool_result": last_tool_result,
        "workflow_status": "tool_executed"
    }
