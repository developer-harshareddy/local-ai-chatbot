

from agent.agent_runner import run_fintech_agent


def run_test_conversation():
    conversation_history = []

    questions = [
        "Get the transaction details for TXN1002",
        "What is its status?",
        "How much is the transaction?"
    ]

    for question in questions:
        print("\n" + "=" * 50)
        print("USER:", question)
        print("=" * 50)

        result = run_fintech_agent(
            question,
            conversation_history
        )

        conversation_history = result["history"]

        print("\nASSISTANT:", result["answer"])
        print("Tool calls:", result["tool_calls_count"])
        print("Workflow status:", result["workflow_status"])

    print("\n========== FINAL CONVERSATION HISTORY ==========")

    for message in conversation_history:
        print(
            message["role"].upper() + ":",
            message["content"]
        )


def test_missing_transaction_id():
    print("\n" + "=" * 50)
    print("TEST: MISSING TRANSACTION ID")
    print("=" * 50)

    result = run_fintech_agent(
        "What is the status of my transaction?"
    )

    print("\nASSISTANT:", result["answer"])
    print("Tool calls:", result["tool_calls_count"])


if __name__ == "__main__":
    run_test_conversation()
    test_missing_transaction_id()
