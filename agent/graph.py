

from langgraph.graph import StateGraph, START, END

from agent.agent_state import AgentState

from agent.fintech_agent import (
    agent_node,
    tool_node
)


# Maximum number of tool calls before stopping
MAX_TOOL_CALLS = 5


# --------------------------------------------------
# CONDITIONAL ROUTING
# --------------------------------------------------

def route_after_agent(state: AgentState):

    last_message = state["messages"][-1]

    tool_calls = last_message.get("tool_calls", [])

    # No tool request: finish the workflow.
    if not tool_calls:
        return "end"

    # Stop repeated tool execution.
    if state.get("tool_calls_count", 0) >= MAX_TOOL_CALLS:
        return "limit"

    # Tool request found: execute the tool.
    return "tools"


# --------------------------------------------------
# TOOL LIMIT NODE
# --------------------------------------------------

def tool_limit_node(state: AgentState):

    return {
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "I reached the maximum allowed number "
                    "of tool calls for this request. "
                    "Please try a more specific question."
                )
            }
        ],
        "workflow_status": "completed"
    }


# --------------------------------------------------
# GRAPH CONSTRUCTION
# --------------------------------------------------

builder = StateGraph(AgentState)


# Register nodes
builder.add_node("agent", agent_node)

builder.add_node("tools", tool_node)

builder.add_node("tool_limit", tool_limit_node)


# Define the starting point
builder.add_edge(START, "agent")


# Conditional routing from agent
builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        "end": END,
        "limit": "tool_limit"
    }
)


# After tool execution, return to agent
builder.add_edge("tools", "agent")


# Stop after tool limit
builder.add_edge("tool_limit", END)


# Compile the graph
fintech_agent = builder.compile()


print("FinTech LangGraph workflow compiled successfully.")
