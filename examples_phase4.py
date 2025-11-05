"""
Test examples for Phase 4: Data, Code, and Specialized Logic Tools

These examples demonstrate the capabilities added in Phase 4.
"""

# Example prompts that Phase 4 can now handle:

PHASE_4_EXAMPLES = [
    # Prompt 3: Reversed Sentence
    {
        "prompt": "Read this sentence backwards: 'The quick brown fox jumps over the lazy dog' and find an antonym for the third word.",
        "required_tools": ["reverse_words", "get_word_at_position", "find_antonym"],
        "explanation": "Reverses word order, gets 3rd word, finds its antonym"
    },
    
    # Prompt 6: Math Table  
    {
        "prompt": "Check if this table is commutative (a*b = b*a for all entries): [[1,2],[3,4]]",
        "required_tools": ["execute_python_code"],
        "explanation": "Executes Python code to systematically check commutativity"
    },
    
    # Prompt 9: Grocery List Categorization
    {
        "prompt": "Categorize these grocery items as fruits or vegetables using botanical rules: tomato, carrot, cucumber, lettuce, bell pepper",
        "required_tools": ["categorize_fruits_vegetables"],
        "explanation": "Uses botanical definitions to categorize correctly"
    },
    
    # Prompt 12: Python Code Output
    {
        "prompt": "What will this Python code output?\n\nx = 5\ny = 10\nz = x + y\nprint(z * 2)",
        "required_tools": ["execute_python_code", "analyze_code_output"],
        "explanation": "Executes code safely and returns the output"
    },
    
    # Prompt 19: Sales from Excel
    {
        "prompt": "Open sales_data.xlsx and sum all sales in the 'Electronics' category",
        "required_tools": ["read_excel_file", "filter_excel_data", "calculate_from_excel"],
        "explanation": "Reads Excel, filters by category, calculates sum"
    },
    
    # Combined with Phase 2+3: Chess puzzle
    {
        "prompt": "Find a chess puzzle online, analyze the position, and tell me the best move",
        "required_tools": ["web_search", "analyze_image", "analyze_chess_position", "analyze_chess_fen"],
        "explanation": "Searches for puzzle, analyzes board image, gets FEN, calculates best move"
    },
]

# Simple test examples for interactive testing:
SIMPLE_TESTS = [
    "Execute this Python code: print('Hello World')",
    "What is 2 ** 10?",
    "Reverse the text: 'Python programming'",
    "Find the antonym of 'fast'",
    "Is 'tomato' a fruit or vegetable botanically?",
    "Analyze this chess position: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
]

# Code execution examples
CODE_EXAMPLES = [
    {
        "name": "Fibonacci Sequence",
        "code": """
fib = [0, 1]
for i in range(8):
    fib.append(fib[-1] + fib[-2])
print(fib)
        """
    },
    {
        "name": "Prime Numbers",
        "code": """
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [n for n in range(2, 50) if is_prime(n)]
print(f"Primes up to 50: {primes}")
        """
    },
    {
        "name": "String Manipulation",
        "code": """
text = "Hello World"
print(f"Uppercase: {text.upper()}")
print(f"Reversed: {text[::-1]}")
print(f"Word count: {len(text.split())}")
        """
    }
]

if __name__ == "__main__":
    print("Phase 4 Test Examples")
    print("=" * 70)
    
    print("\nSimple Tests:")
    for i, test in enumerate(SIMPLE_TESTS, 1):
        print(f"{i}. {test}")
    
    print("\n\nChallenge Prompts (Phase 4):")
    for i, example in enumerate(PHASE_4_EXAMPLES, 1):
        print(f"\n{i}. {example['prompt']}")
        print(f"   Tools: {', '.join(example['required_tools'])}")
        print(f"   How: {example['explanation']}")
    
    print("\n\nCode Execution Examples:")
    for i, example in enumerate(CODE_EXAMPLES, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Code:{example['code']}")
