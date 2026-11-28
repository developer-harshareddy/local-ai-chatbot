

from agent.fintech_agent import tool_node


print("\n========== LANGGRAPH TOOL NODE TEST ==========")

test_state = {
    "messages": [
        {
            "role": "user",
            "content": "Check transaction status of TXN1002"
        },
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "function": {
                        "name": "get_transaction_status",
                        "arguments": {
                            "transaction_id": "TXN1002"
                        }
                    }
                }
            ]
        }
    ],
    "tool_calls_count": 0,
    "last_tool_result": None,
    "workflow_status": "processing"
}

result = tool_node(test_state)

print("\n========== TOOL NODE OUTPUT ==========")

print("Tool messages:", result["messages"])

print("Tool calls count:", result["tool_calls_count"])

print("Last tool result:", result["last_tool_result"])

print("Workflow status:", result["workflow_status"])

assert result["tool_calls_count"] == 1

assert result["last_tool_result"]["transaction_id"] == "TXN1002"

assert result["workflow_status"] == "tool_executed"

print("\nTool node test completed successfully.")
