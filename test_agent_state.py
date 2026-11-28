
from agent.agent_state import AgentState


test_state: AgentState = {
    "messages": [
        {
            "role": "user",
            "content": "Check transaction status of TXN1002"
        }
    ],
    "tool_calls_count": 0,
    "last_tool_result": None,
    "workflow_status": "started"
}

print("\n========== AGENT STATE TEST ==========")

print("Messages:", test_state["messages"])
print("Tool calls:", test_state["tool_calls_count"])
print("Last tool result:", test_state["last_tool_result"])
print("Workflow status:", test_state["workflow_status"])

print("\nAgent state test completed successfully.")