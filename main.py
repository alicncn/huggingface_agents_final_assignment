"""Main entry point for the Agentic AI solution."""
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent.graph import create_agent
from agent.state import AgentState


def main():
    """Run the agent in interactive mode."""
    # Load environment variables
    load_dotenv()
    
    # Verify API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in .env file")
        print("Please copy .env.example to .env and add your API key")
        return
    
    # Create the agent
    print("Initializing agent...")
    app = create_agent()
    print("Agent initialized successfully!\n")
    
    # Interactive loop
    print("Agentic AI Assistant (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Create initial state
        initial_state: AgentState = {
            "messages": [HumanMessage(content=user_input)],
            "next_action": "",
            "intermediate_results": {}
        }
        
        # Run the agent
        try:
            print("\nAssistant: ", end="", flush=True)
            
            final_state = app.invoke(initial_state)
            
            # Get the last AI message
            last_message = final_state["messages"][-1]
            print(last_message.content)
            
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
