"""Agent state definition for LangGraph."""
from typing import TypedDict, Annotated, Sequence, List, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Enhanced state of the agent with improved tracking.
    
    Attributes:
        messages: The conversation history
        next_action: The next action to take (either a tool name or "END")
        intermediate_results: Storage for results from previous steps
        tools_used: List of tools used in this conversation
        error_count: Number of errors encountered
        last_error: Last error message if any
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_action: str
    intermediate_results: dict
    tools_used: List[str]
    error_count: int
    last_error: Optional[str]
