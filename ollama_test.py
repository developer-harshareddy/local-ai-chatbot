

import requests
import json

# Step 1: Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/chat"

# Step 2: Model name
MODEL_NAME = "qwen2.5:1.5b"

# Step 3: Prepare user question
payload = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user",
            "content": "Explain how a payment gateway processes an ISO 8583 transaction."
        }
    ],
    "stream": False
}

try:
    # Step 4: Send HTTP POST request
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    # Step 5: Check HTTP response
    response.raise_for_status()

    # Step 6: Convert JSON response
    result = response.json()

    # Step 7: Extract AI-generated answer
    answer = result["message"]["content"]

    print("\n========== AI RESPONSE ==========\n")
    print(answer)

    print("\n=================================")

except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to Ollama.")

except requests.exceptions.Timeout:
    print("ERROR: Ollama response timed out.")

except requests.exceptions.HTTPError as error:
    print("HTTP ERROR:", error)

except (ValueError, KeyError) as error:
    print("RESPONSE PARSING ERROR:", error)
