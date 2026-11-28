

import requests
import json

from llm_service import OLLAMA_URL, MODEL_NAME
from tool_definitions import TOOLS


def main():

    print("\n========== OLLAMA TOOL CALL TEST ==========")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a FinTech payment operations assistant. "
                "When the user asks about a specific transaction, "
                "use the appropriate available function. "
                "Do not invent transaction details."
            )
        },
        {
            "role": "user",
            "content": "Check the status of transaction TXN1002."
        }
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    print("\nModel:", MODEL_NAME)
    print("Sending request to Ollama...")

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=(10, 300)
    )

    response.raise_for_status()

    result = response.json()

    assistant_message = result.get("message", {})

    print("\n========== MODEL RESPONSE ==========")

    print("Content:")
    print(assistant_message.get("content", ""))

    tool_calls = assistant_message.get("tool_calls", [])

    if not tool_calls:

        print("\nNo tool call was generated.")
        print("We need to investigate model tool-calling support.")

        return

    print("\n========== TOOL CALL REQUEST ==========")

    for call in tool_calls:

        function = call.get("function", {})

        tool_name = function.get("name")
        arguments = function.get("arguments", {})

        print("Tool name:", tool_name)

        print("Arguments:")
        print(json.dumps(arguments, indent=4))

    print("\nTool calls received:", len(tool_calls))

    print("\nIMPORTANT:")
    print("No Python business function was executed in this test.")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()
