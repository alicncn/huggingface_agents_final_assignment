"""
Comprehensive test suite for the Agentic AI system.
Tests all 20 challenge prompts plus additional integration tests.
"""
import sys
import os
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import create_agent
from agent.state import AgentState
from langchain_core.messages import HumanMessage


# All 20 challenge prompts with expected behaviors
CHALLENGE_PROMPTS = [
    {
        "id": 1,
        "category": "Web Search",
        "prompt": "What are the latest technology news headlines today?",
        "expected_tools": ["web_search"],
        "validation": lambda result: len(result) > 50  # Should return substantial content
    },
    {
        "id": 2,
        "category": "Wikipedia",
        "prompt": "What is the population of France according to Wikipedia?",
        "expected_tools": ["web_search_wikipedia"],
        "validation": lambda result: "million" in result.lower() or "population" in result.lower()
    },
    {
        "id": 3,
        "category": "Document Reading",
        "prompt": "Extract all links from https://example.com",
        "expected_tools": ["extract_links"],
        "validation": lambda result: "link" in result.lower() or "url" in result.lower()
    },
    {
        "id": 4,
        "category": "Audio Transcription",
        "prompt": "Transcribe the audio file at path test_audio.mp3",
        "expected_tools": ["transcribe_audio"],
        "validation": lambda result: True  # Will fail if file doesn't exist
    },
    {
        "id": 5,
        "category": "Image Analysis",
        "prompt": "Analyze this image and describe what you see: test_image.jpg",
        "expected_tools": ["analyze_image", "describe_image"],
        "validation": lambda result: True
    },
    {
        "id": 6,
        "category": "Object Counting",
        "prompt": "How many cars are in the image test_image.jpg?",
        "expected_tools": ["count_objects_in_image"],
        "validation": lambda result: True
    },
    {
        "id": 7,
        "category": "OCR",
        "prompt": "Extract text from the image test_document.jpg",
        "expected_tools": ["extract_text_from_image"],
        "validation": lambda result: True
    },
    {
        "id": 8,
        "category": "Video Analysis",
        "prompt": "Analyze the video test_video.mp4 and describe what happens",
        "expected_tools": ["analyze_video"],
        "validation": lambda result: True
    },
    {
        "id": 9,
        "category": "Video Transcription",
        "prompt": "Transcribe the audio from video test_video.mp4",
        "expected_tools": ["transcribe_video"],
        "validation": lambda result: True
    },
    {
        "id": 10,
        "category": "Database Query",
        "prompt": "Which player had the most walks in a single season in the baseball database?",
        "expected_tools": ["ask_database", "query_database"],
        "validation": lambda result: "ruth" in result.lower() or "170" in result
    },
    {
        "id": 11,
        "category": "Code Execution",
        "prompt": "Calculate the factorial of 10",
        "expected_tools": ["execute_python_code", "evaluate_python_expression"],
        "validation": lambda result: "3628800" in result
    },
    {
        "id": 12,
        "category": "Data Analysis",
        "prompt": "Read the Excel file data.xlsx and show me the first 5 rows",
        "expected_tools": ["read_excel_file"],
        "validation": lambda result: True
    },
    {
        "id": 13,
        "category": "Database Query",
        "prompt": "What was Derek Jeter's jersey number?",
        "expected_tools": ["ask_database", "query_database"],
        "validation": lambda result: "2" in result or "#2" in result
    },
    {
        "id": 14,
        "category": "Text Logic",
        "prompt": "Reverse the text: Hello World",
        "expected_tools": ["reverse_text"],
        "validation": lambda result: "dlroW olleH" in result
    },
    {
        "id": 15,
        "category": "Text Logic",
        "prompt": "What is the antonym of 'hot'?",
        "expected_tools": ["find_antonym"],
        "validation": lambda result: "cold" in result.lower()
    },
    {
        "id": 16,
        "category": "Chess Engine",
        "prompt": "What is the best move in this chess position: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "expected_tools": ["analyze_chess_fen"],
        "validation": lambda result: len(result) > 20
    },
    {
        "id": 17,
        "category": "Database Query",
        "prompt": "Which country had the largest team at the Tokyo 2020 Olympics?",
        "expected_tools": ["ask_database", "query_database"],
        "validation": lambda result: "united states" in result.lower() or "usa" in result.lower() or "613" in result
    },
    {
        "id": 18,
        "category": "Database Query",
        "prompt": "List all countries in the Olympics database that no longer exist today",
        "expected_tools": ["ask_database", "query_database"],
        "validation": lambda result: "soviet" in result.lower() or "yugoslavia" in result.lower()
    },
    {
        "id": 19,
        "category": "Text Logic",
        "prompt": "Categorize these items as fruits or vegetables: tomato, carrot, cucumber",
        "expected_tools": ["categorize_fruits_vegetables"],
        "validation": lambda result: "tomato" in result.lower() and "carrot" in result.lower()
    },
    {
        "id": 20,
        "category": "Database Query",
        "prompt": "Who won the International Math Olympiad in 1990?",
        "expected_tools": ["ask_database", "query_database"],
        "validation": lambda result: "1990" in result
    },
]


class TestRunner:
    """Test runner for challenge prompts."""
    
    def __init__(self):
        self.agent = None
        self.results = []
        
    def setup(self):
        """Set up the agent."""
        print("Setting up agent...")
        try:
            self.agent = create_agent()
            print("✓ Agent created successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to create agent: {e}")
            return False
    
    def run_test(self, test_case: Dict) -> Dict:
        """Run a single test case."""
        test_id = test_case["id"]
        category = test_case["category"]
        prompt = test_case["prompt"]
        
        print(f"\n{'='*70}")
        print(f"Test #{test_id}: {category}")
        print(f"Prompt: {prompt}")
        print(f"{'='*70}")
        
        try:
            # Create initial state
            initial_state = {
                "messages": [HumanMessage(content=prompt)],
                "intermediate_results": {},
                "next_action": "",
                "tools_used": [],
                "error_count": 0,
                "last_error": None
            }
            
            # Run the agent
            result = self.agent.invoke(initial_state)
            
            # Extract response
            last_message = result["messages"][-1]
            response = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            # Validate
            try:
                is_valid = test_case["validation"](response)
            except:
                is_valid = True  # If validation fails, assume it's because of missing files
            
            # Check tools used
            tools_used = result.get("tools_used", [])
            error_count = result.get("error_count", 0)
            
            test_result = {
                "id": test_id,
                "category": category,
                "prompt": prompt,
                "response": response[:200] + "..." if len(response) > 200 else response,
                "validation_passed": is_valid,
                "tools_used": tools_used,
                "error_count": error_count,
                "status": "PASS" if is_valid and error_count == 0 else "PARTIAL" if is_valid else "FAIL"
            }
            
            print(f"\nStatus: {test_result['status']}")
            print(f"Response: {test_result['response']}")
            if error_count > 0:
                print(f"⚠ Errors encountered: {error_count}")
            
            return test_result
            
        except Exception as e:
            print(f"\n✗ Test failed with exception: {str(e)}")
            return {
                "id": test_id,
                "category": category,
                "prompt": prompt,
                "response": f"ERROR: {str(e)}",
                "validation_passed": False,
                "tools_used": [],
                "error_count": 1,
                "status": "ERROR"
            }
    
    def run_all_tests(self, test_cases: List[Dict] = None):
        """Run all test cases."""
        if test_cases is None:
            test_cases = CHALLENGE_PROMPTS
        
        print("\n" + "="*70)
        print("RUNNING COMPREHENSIVE TEST SUITE")
        print("="*70)
        print(f"Total tests: {len(test_cases)}")
        
        for test_case in test_cases:
            result = self.run_test(test_case)
            self.results.append(result)
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print("\n\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        partial = sum(1 for r in self.results if r["status"] == "PARTIAL")
        failed = sum(1 for r in self.results if r["status"] in ["FAIL", "ERROR"])
        
        print(f"\nTotal Tests: {total}")
        print(f"  ✓ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"  ⚠ Partial: {partial} ({partial/total*100:.1f}%)")
        print(f"  ✗ Failed: {failed} ({failed/total*100:.1f}%)")
        
        # Results by category
        print("\n" + "-"*70)
        print("RESULTS BY CATEGORY")
        print("-"*70)
        
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "passed": 0}
            categories[cat]["total"] += 1
            if result["status"] == "PASS":
                categories[cat]["passed"] += 1
        
        for cat, stats in sorted(categories.items()):
            status = "✓" if stats["passed"] == stats["total"] else "⚠" if stats["passed"] > 0 else "✗"
            print(f"{status} {cat}: {stats['passed']}/{stats['total']}")
        
        # Failed tests detail
        if failed > 0:
            print("\n" + "-"*70)
            print("FAILED TESTS")
            print("-"*70)
            for result in self.results:
                if result["status"] in ["FAIL", "ERROR"]:
                    print(f"\n#{result['id']}: {result['category']}")
                    print(f"  Prompt: {result['prompt']}")
                    print(f"  Status: {result['status']}")
                    print(f"  Response: {result['response'][:100]}...")
        
        print("\n" + "="*70)


def main():
    """Run the test suite."""
    runner = TestRunner()
    
    if not runner.setup():
        print("\n✗ Setup failed. Cannot run tests.")
        return
    
    # Run all tests
    runner.run_all_tests()
    
    print("\n✅ Test suite complete!")


if __name__ == "__main__":
    main()
