"""LangGraph agent definition with enhanced error handling and logging."""
import os
import logging
from typing import Literal
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from agent.state import AgentState
from tools.registry import get_all_tools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_agent():
    """Create and configure the LangGraph agent."""
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    # Initialize the Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.7,
    )
    
    # Get all available tools
    tools = get_all_tools()
    
    # Bind tools to the model
    model_with_tools = model.bind_tools(tools)
    
    # Define the agent node
    def agent_node(state: AgentState) -> AgentState:
        """
        The main agent node that decides what to do next.
        Uses the LLM to either call a tool or respond to the user.
        """
        try:
            messages = state["messages"]
            
            # Add system message if this is the first interaction
            if len(messages) == 1 and isinstance(messages[0], HumanMessage):
                system_message = SystemMessage(content="""You are an advanced AI assistant capable of complex reasoning and multi-step problem solving.

You have access to various tools for:
- Web search and information retrieval
- Multimedia analysis (audio, video, images)
- Data analysis and file processing
- Code interpretation
- Database queries
- Specialized logic engines

When given a task:
1. Break it down into logical steps
2. Use the appropriate tools in sequence
3. Store intermediate results for use in subsequent steps
4. Provide a clear, accurate final answer

Always think step-by-step and use tools when needed rather than guessing.""")
                messages = [system_message] + list(messages)
            
            # Call the model
            response = model_with_tools.invoke(messages)
            
            logger.info(f"Agent generated response")
            
            # Update state with enhanced tracking
            return {
                "messages": [response],
                "intermediate_results": state.get("intermediate_results", {}),
                "next_action": state.get("next_action", ""),
                "tools_used": state.get("tools_used", []),
                "error_count": state.get("error_count", 0),
                "last_error": state.get("last_error")
            }
            
        except Exception as e:
            logger.error(f"Error in agent_node: {str(e)}")
            error_message = AIMessage(content=f"I encountered an error: {str(e)}")
            
            return {
                "messages": [error_message],
                "intermediate_results": state.get("intermediate_results", {}),
                "next_action": "end",
                "tools_used": state.get("tools_used", []),
                "error_count": state.get("error_count", 0) + 1,
                "last_error": str(e)
            }
    
    # Define the routing function
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """
        Determine if we should call tools or end the conversation.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the LLM makes a tool call, route to the tools node
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        # Otherwise, end the conversation
        return "end"
    
    # Create the tool node
    tool_node = ToolNode(tools)
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Set the entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    app = workflow.compile()
    
    return app
