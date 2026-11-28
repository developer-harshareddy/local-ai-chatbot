

from agent.graph import fintech_agent


def run_agent(question):

    print("\n======================================")
    print("USER QUESTION:", question)
    print("======================================")

    initial_state = {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "tool_calls_count": 0,
        "last_tool_result": None,
        "workflow_status": "started"
    }

    result = fintech_agent.invoke(initial_state)

    print("\n========== FINAL RESPONSE ==========")

    for message in reversed(result["messages"]):

        if (
            message.get("role") == "assistant"
            and message.get("content")
        ):
            print(message["content"])
            break

    print("\n========== WORKFLOW DETAILS ==========")

    print(
        "Tool calls:",
        result["tool_calls_count"]
    )

    print(
        "Last tool result:",
        result["last_tool_result"]
    )

    print(
        "Workflow status:",
        result["workflow_status"]
    )


if __name__ == "__main__":

    # Test 1: Agent should execute a banking tool.
    run_agent(
        "Check transaction status of TXN1002"
    )

    # Test 2: Agent should respond without a tool.
    run_agent(
        "What is the difference between savings and current accounts?"
    )
