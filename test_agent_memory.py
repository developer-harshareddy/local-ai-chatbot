

from agent.agent_runner import run_fintech_agent


conversation_history = []


def ask_agent(question):

    global conversation_history

    print("\n====================================")
    print("USER:", question)
    print("====================================")

    result = run_fintech_agent(
        question=question,
        conversation_history=conversation_history
    )

    conversation_history = result["history"]

    print("\nASSISTANT:", result["answer"])

    print(
        "\nTool calls:",
        result["tool_calls_count"]
    )

    print(
        "Workflow status:",
        result["workflow_status"]
    )


if __name__ == "__main__":

    # First turn: identify an account.
    ask_agent(
        "Get account details for ACC1001"
    )

    # Second turn: refer to the previous account.
    ask_agent(
        "What is its available balance?"
    )

    # Third turn: ask another follow-up.
    ask_agent(
        "What type of account is it?"
    )

    print("\n========== CONVERSATION HISTORY ==========")

    for message in conversation_history:

        print(
            message["role"].upper() + ":",
            message["content"]
        )

    print("\nAgent memory test completed.")
