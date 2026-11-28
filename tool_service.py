

import requests
import json

from tool_definitions import TOOLS
from fintech_tools import execute_tool


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"


SYSTEM_MESSAGE = """
You are a FinTech payment operations assistant.

You can retrieve mock account and transaction information
using the available tools.

Rules:
1. Use tools when the user asks about account information.
2. Use tools when the user asks about transaction status.
3. Never invent account or transaction details.
4. Never claim a tool succeeded unless it returned successfully.
5. Explain the returned result clearly.
6. These are mock banking records.
"""


def execute_tool_call(tool_call):

    function_data = tool_call.get("function", {})

    tool_name = function_data.get("name")

    arguments = function_data.get("arguments", {})

    print("\nExecuting tool:", tool_name)
    print("Arguments:", arguments)

    result = execute_tool(
        tool_name=tool_name,
        arguments=arguments
    )

    print("Tool execution successful.")

    return result


def chat_with_tools(user_question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    # First request: Ask Ollama whether a tool is needed.

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=(10, 300)
    )

    response.raise_for_status()

    assistant_message = response.json()["message"]

    messages.append(assistant_message)

    tool_calls = assistant_message.get("tool_calls", [])

    if not tool_calls:

        return assistant_message.get("content", "")

    # Execute requested tools.

    for tool_call in tool_calls:

        result = execute_tool_call(tool_call)

        messages.append({
            "role": "tool",
            "tool_name": tool_call["function"]["name"],
            "content": json.dumps(result)
        })

    # Second request: Send tool results back to Ollama.

    final_payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS,
        "stream": False
    }

    final_response = requests.post(
        OLLAMA_URL,
        json=final_payload,
        timeout=(10, 300)
    )

    final_response.raise_for_status()

    final_message = final_response.json()["message"]

    return final_message.get("content", "")
