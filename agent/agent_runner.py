

from agent.graph import fintech_agent


def run_fintech_agent(question, conversation_history=None):

    if conversation_history is None:
        conversation_history = []

    # Add the current user question to previous conversation.
    input_messages = conversation_history + [
        {
            "role": "user",
            "content": question
        }
    ]

    initial_state = {
        "messages": input_messages,
        "tool_calls_count": 0,
        "last_tool_result": None,
        "workflow_status": "started"
    }

    # Execute the LangGraph workflow.
    result = fintech_agent.invoke(initial_state)

    # Find the final assistant response.
    final_answer = ""

    for message in reversed(result["messages"]):

        if (
            message.get("role") == "assistant"
            and message.get("content")
            and not message.get("tool_calls")
        ):
            final_answer = message["content"]
            break

    # Maintain clean conversational history.
    # Keep user and final assistant messages, but not
    # intermediate tool-call and tool-result messages.
    updated_history = conversation_history + [
        {
            "role": "user",
            "content": question
        },
        {
            "role": "assistant",
            "content": final_answer
        }
    ]

    return {
        "answer": final_answer,
        "history": updated_history,
        "tool_calls_count": result["tool_calls_count"],
        "last_tool_result": result["last_tool_result"],
        "workflow_status": result["workflow_status"]
    }
