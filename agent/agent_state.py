
from typing import Annotated, Any, TypedDict
import operator


class AgentState(TypedDict):

    # Conversation messages are appended as the graph executes.
    messages: Annotated[list[dict[str, Any]], operator.add]

    # Number of tools executed during this workflow.
    tool_calls_count: int

    # Most recent result returned by a Python tool.
    last_tool_result: dict[str, Any] | None

    # Current workflow status.
    workflow_status: str
