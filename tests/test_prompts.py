"""Test cases for all 20 prompts."""
import pytest
from langchain_core.messages import HumanMessage
from agent.graph import create_agent
from agent.state import AgentState


class TestPrompts:
    """Test all 20 challenge prompts."""
    
    @classmethod
    def setup_class(cls):
        """Set up the agent once for all tests."""
        cls.app = create_agent()
    
    def run_prompt(self, prompt: str) -> str:
        """Helper method to run a prompt and get the response."""
        initial_state: AgentState = {
            "messages": [HumanMessage(content=prompt)],
            "next_action": "",
            "intermediate_results": {}
        }
        
        final_state = self.app.invoke(initial_state)
        return final_state["messages"][-1].content
    
    @pytest.mark.skip(reason="Not implemented yet")
    def test_01_mercedes_sosa_albums(self):
        """Test: Mercedes Sosa Albums."""
        prompt = "How many albums did Mercedes Sosa release between 1990 and 2000? Use English Wikipedia 2022 version."
        response = self.run_prompt(prompt)
        # Add assertion once tool is implemented
    
    @pytest.mark.skip(reason="Not implemented yet")
    def test_02_birds_in_video(self):
        """Test: Birds in Video."""
        prompt = "How many different species of birds are visible in this video?"
        # Add test once video analysis is implemented
    
    @pytest.mark.skip(reason="Not implemented yet")
    def test_03_reversed_sentence(self):
        """Test: Reversed Sentence."""
        prompt = "Read this sentence backwards and find an antonym for the third word."
        # Add test once implemented
    
    # Add remaining 17 test cases...
