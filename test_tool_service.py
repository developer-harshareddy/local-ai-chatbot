

from tool_service import chat_with_tools


def main():

    print("\n========== FINTECH AI TOOL SERVICE TEST ==========")

    question = "Check the transaction status of TXN1002"

    print("\nUser question:")
    print(question)

    print("\nProcessing with Ollama and Python tools...")

    answer = chat_with_tools(question)

    print("\n========== FINAL AI RESPONSE ==========")
    print(answer)

    assert answer.strip(), "LLM returned an empty response"

    print("\nTool service test completed successfully.")


if __name__ == "__main__":
    main()
