

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"

# Conversation instructions
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI assistant specializing in "
            "Java, Spring Boot, Python, GenAI and fintech. "
            "Explain concepts clearly with practical examples."
        )
    }
]


def get_llm_response(conversation):
    """Send conversation history to Ollama and return its response."""

    payload = {
        "model": MODEL_NAME,
        "messages": conversation,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama."

    except requests.exceptions.Timeout:
        return "ERROR: The model response timed out."

    except requests.exceptions.RequestException as error:
        return f"API ERROR: {error}"

    except (ValueError, KeyError):
        return "ERROR: Invalid response received from Ollama."


def start_chatbot():
    print("\n===================================")
    print("       LOCAL AI CHATBOT")
    print("===================================")
    print("Model:", MODEL_NAME)
    print("Type 'exit' to stop the chatbot.")
    print("Type 'clear' to clear conversation history.")

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            print("Please enter a question.")
            continue

        if user_input.lower() == "exit":
            print("\nChatbot stopped. Goodbye!")
            break

        if user_input.lower() == "clear":
            messages[:] = messages[:1]
            print("Conversation history cleared.")
            continue

        # Add user message to conversation
        messages.append({
            "role": "user",
            "content": user_input
        })

        # Get response using complete conversation
        answer = get_llm_response(messages)

        print("\nAI:", answer)

        # Save assistant response
        if not answer.startswith("ERROR:") and not answer.startswith("API ERROR:"):
            messages.append({
                "role": "assistant",
                "content": answer
            })
        else:
            # Remove failed user request so history stays consistent
            messages.pop()


if __name__ == "__main__":
    start_chatbot()
