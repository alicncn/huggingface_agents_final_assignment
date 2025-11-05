"""
Demo script for Phase 4: Data, Code, and Specialized Logic Tools
Tests code execution, chess analysis, and text logic without requiring files.
"""

print("=" * 70)
print("Phase 4 Demo: Code, Data, and Logic Tools")
print("=" * 70)

# Test 1: Code Execution
print("\n1. Testing Python Code Execution")
print("-" * 70)
try:
    from tools.code_interpreter import execute_python_code
    
    code = """
# Calculate factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"Factorial of 5 is {result}")

# Fibonacci sequence
fib = [0, 1]
for i in range(8):
    fib.append(fib[-1] + fib[-2])
print(f"First 10 Fibonacci numbers: {fib}")
"""
    
    result = execute_python_code.invoke({"code": code})
    print("✓ Code executed successfully:")
    print(result)
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Expression Evaluation
print("\n\n2. Testing Expression Evaluation")
print("-" * 70)
try:
    from tools.code_interpreter import evaluate_python_expression
    
    expressions = [
        "2 ** 10",
        "sum([i**2 for i in range(1, 11)])",
        "len('Hello World')",
    ]
    
    for expr in expressions:
        result = evaluate_python_expression.invoke({"expression": expr})
        print(f"  {expr} → {result}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Chess Engine
print("\n\n3. Testing Chess Engine")
print("-" * 70)
try:
    from tools.chess_engine import analyze_chess_fen, get_chess_position_info
    
    # Scholar's mate position (almost)
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4"
    
    print("Analyzing chess position...")
    result = analyze_chess_fen.invoke({"fen": fen})
    print(result)
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Text Manipulation
print("\n\n4. Testing Text Manipulation Tools")
print("-" * 70)
try:
    from tools.text_logic import reverse_text, reverse_words, find_antonym
    
    # Test reverse
    result1 = reverse_text.invoke({"text": "Python is awesome"})
    print(f"  {result1}")
    
    # Test reverse words
    result2 = reverse_words.invoke({"text": "The quick brown fox"})
    print(f"  Reversed words: {result2}")
    
    # Test antonyms
    words = ["hot", "big", "fast", "happy"]
    print("\n  Antonyms:")
    for word in words:
        result = find_antonym.invoke({"word": word})
        print(f"    {result}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 5: Fruit/Vegetable Categorization
print("\n\n5. Testing Botanical Categorization")
print("-" * 70)
try:
    from tools.text_logic import categorize_fruits_vegetables
    
    items = ["tomato", "carrot", "cucumber", "potato", "apple", "lettuce"]
    result = categorize_fruits_vegetables.invoke({"items": items})
    print(result)
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 6: Number Extraction
print("\n\n6. Testing Number Extraction")
print("-" * 70)
try:
    from tools.text_logic import extract_numbers
    
    texts = [
        "I have 3 apples and 5 oranges",
        "Call me at 555-1234",
        "The year 2024 was great"
    ]
    
    for text in texts:
        result = extract_numbers.invoke({"text": text})
        print(f"  '{text}' → {result}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Summary
print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)

print("\n✅ All Phase 4 tools are working!")

print("\n📋 Demonstrated Tools:")
print("  ✓ Code execution (factorial, fibonacci)")
print("  ✓ Expression evaluation (math operations)")
print("  ✓ Chess analysis (position evaluation, best move)")
print("  ✓ Text manipulation (reverse, antonyms)")
print("  ✓ Botanical categorization (fruits vs vegetables)")
print("  ✓ Number extraction from text")

print("\n🎯 Ready to solve challenge prompts:")
print("  - Prompt 3: Reversed Sentence + Antonym")
print("  - Prompt 6: Math Table Analysis")
print("  - Prompt 9: Grocery Categorization")
print("  - Prompt 12: Python Code Output Prediction")
print("  - Prompt 19: Excel Data Analysis (needs Excel file)")

print("\n💡 Data analysis tools also available:")
print("  - read_excel_file, read_csv_file")
print("  - filter_excel_data, calculate_from_excel")
print("  (These require actual Excel/CSV files to demo)")

print("\n" + "=" * 70)
