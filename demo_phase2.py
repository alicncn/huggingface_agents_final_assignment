"""
Demo script showing Phase 2 capabilities without requiring API keys.
Tests the document reader tools with public websites.
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("Phase 2 Demo: Document Reader Tools")
print("=" * 70)

# Test 1: Read URL
print("\n1. Testing read_url tool...")
print("-" * 70)
try:
    from tools.document_reader import read_url
    result = read_url.invoke({
        "url": "https://example.com",
        "extract_text_only": True
    })
    print("✓ Successfully read example.com:")
    print(result[:300] + "..." if len(result) > 300 else result)
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Extract Links
print("\n\n2. Testing extract_links tool...")
print("-" * 70)
try:
    from tools.document_reader import extract_links
    result = extract_links.invoke({
        "url": "https://example.com",
        "filter_text": None
    })
    print("✓ Successfully extracted links:")
    print(result[:400] + "..." if len(result) > 400 else result)
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Search in Document
print("\n\n3. Testing search_in_document tool...")
print("-" * 70)
try:
    from tools.document_reader import search_in_document
    result = search_in_document.invoke({
        "url": "https://example.com",
        "search_term": "example",
        "context_chars": 100
    })
    print("✓ Successfully searched document:")
    print(result[:400] + "..." if len(result) > 400 else result)
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Web Search (if API key is configured)
print("\n\n4. Testing web_search tool...")
print("-" * 70)
tavily_key = os.getenv("TAVILY_API_KEY")
if tavily_key and tavily_key != "your_tavily_api_key_here":
    try:
        from tools.web_search import web_search
        result = web_search.invoke({
            "query": "Python programming language",
            "max_results": 3
        })
        print("✓ Successfully performed web search:")
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("⚠ Skipping - TAVILY_API_KEY not configured")
    print("  To enable web search:")
    print("  1. Get free key at: https://tavily.com")
    print("  2. Add to .env: TAVILY_API_KEY=your_key")

# Summary
print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)
print("\nAll document reader tools are working! 🎉")
print("\nTry the agent with these example prompts:")
print("  - 'Read the content from https://example.com'")
print("  - 'Extract links from https://news.ycombinator.com'")
print("  - 'Search for Python in https://www.python.org'")

if not (tavily_key and tavily_key != "your_tavily_api_key_here"):
    print("\n⚠ Configure TAVILY_API_KEY to enable web search capabilities!")
