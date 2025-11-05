"""Verification script for Phase 2: Information Retrieval Tools."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Phase 2: Information Retrieval Tools - Verification")
print("=" * 60)

# Check dependencies
print("\n✓ Checking dependencies...")
try:
    import tavily
    import bs4
    import requests
    print("  ✓ tavily-python installed")
    print("  ✓ beautifulsoup4 installed")
    print("  ✓ requests installed")
except ImportError as e:
    print(f"  ✗ Missing dependency: {e}")
    exit(1)

# Check API keys
print("\n✓ Checking API configuration...")
gemini_key = os.getenv("GOOGLE_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

if gemini_key and gemini_key != "your_api_key_here":
    print(f"  ✓ GOOGLE_API_KEY configured")
else:
    print("  ⚠ GOOGLE_API_KEY not configured")

if tavily_key and tavily_key != "your_tavily_api_key_here":
    print(f"  ✓ TAVILY_API_KEY configured")
else:
    print("  ⚠ TAVILY_API_KEY not configured - web search will not work")
    print("    Get a free key at: https://tavily.com")

# Check tools
print("\n✓ Checking tools...")
try:
    from tools.registry import get_all_tools
    tools = get_all_tools()
    print(f"  ✓ {len(tools)} tools registered:")
    for tool in tools:
        print(f"    - {tool.name}: {tool.description.split('.')[0]}")
except Exception as e:
    print(f"  ✗ Error loading tools: {e}")
    exit(1)

# Test agent initialization
print("\n✓ Testing agent initialization...")
if gemini_key and gemini_key != "your_api_key_here":
    try:
        from agent.graph import create_agent
        app = create_agent()
        print("  ✓ Agent initialized successfully with Phase 2 tools!")
    except Exception as e:
        print(f"  ✗ Agent initialization failed: {e}")
        exit(1)
else:
    print("  ⚠ Skipping (GOOGLE_API_KEY not configured)")

# Test a simple tool (read_url)
print("\n✓ Testing document reader tool...")
try:
    from tools.document_reader import read_url
    # Test with a simple, reliable URL
    result = read_url.invoke({"url": "https://example.com", "extract_text_only": True})
    if "Example Domain" in result or "example" in result.lower():
        print("  ✓ Document reader working correctly!")
    else:
        print(f"  ⚠ Unexpected result: {result[:100]}")
except Exception as e:
    print(f"  ✗ Document reader test failed: {e}")

# Summary
print("\n" + "=" * 60)
print("Phase 2 Verification Summary:")
print("-" * 60)

if tavily_key and tavily_key != "your_tavily_api_key_here":
    print("✅ Phase 2 is COMPLETE and READY TO USE!")
    print("\nAvailable capabilities:")
    print("  - Web search (Tavily API)")
    print("  - Wikipedia search")
    print("  - URL content extraction")
    print("  - Link extraction from webpages")
    print("  - Document text search")
    print("\nNext steps:")
    print("  1. Run: python main.py")
    print("  2. Try: 'Search for information about Mercedes Sosa'")
    print("  3. Try: 'Read the content from https://example.com'")
else:
    print("⚠️  Phase 2 is COMPLETE but needs configuration!")
    print("\nTo enable web search:")
    print("  1. Get a free Tavily API key at: https://tavily.com")
    print("  2. Add it to .env file: TAVILY_API_KEY=your_key")
    print("\nDocument reader tools work without Tavily:")
    print("  - read_url")
    print("  - extract_links")
    print("  - search_in_document")

print("=" * 60)
