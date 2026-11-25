import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"

def stream_llm_response(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": True
    }
    with requests.post(
        OLLAMA_URL, json=payload, stream=True, timeout=(10, 300)
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line.decode("utf-8"))
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
            if chunk.get("done"):
                break