"""
Quick test of Phase 5 database tools solving Challenge Prompt #13.
Tests the agent's ability to answer: "What was Derek Jeter's jersey number?"
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.database_query import ask_database


def test_challenge_prompt_13():
    """Test Challenge Prompt #13: Derek Jeter's jersey number."""
    print("="*70)
    print("TESTING CHALLENGE PROMPT #13")
    print("="*70)
    print("\nPrompt: What was Derek Jeter's jersey number?")
    print("\nExpected Answer: #2")
    print("\n" + "-"*70)
    
    result = ask_database.invoke({
        "question": "What was Derek Jeter's jersey number?",
        "database_name": "baseball"
    })
    
    print("\nAgent Response:")
    print(result)
    
    # Verify the answer
    if "2" in result and ("Jeter" in result or "Derek" in result):
        print("\n" + "="*70)
        print("✅ TEST PASSED - Correct answer found!")
        print("="*70)
        return True
    else:
        print("\n" + "="*70)
        print("❌ TEST FAILED - Answer not found")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_challenge_prompt_13()
    sys.exit(0 if success else 1)
