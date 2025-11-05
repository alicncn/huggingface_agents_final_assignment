"""
Test examples for Phase 2: Information Retrieval Tools

These examples demonstrate the capabilities added in Phase 2.
Run these after configuring TAVILY_API_KEY in .env
"""

# Example prompts that Phase 2 can now handle:

PHASE_2_EXAMPLES = [
    # Prompt 1: Mercedes Sosa Albums (requires web search + Wikipedia)
    {
        "prompt": "How many albums did Mercedes Sosa release between 1990 and 2000? Search Wikipedia for information.",
        "required_tools": ["web_search_wikipedia", "read_url"],
        "explanation": "Uses web search to find Wikipedia article, then reads the content to count albums in date range"
    },
    
    # Prompt 8: Veterinarian Surname (requires finding and reading specific webpage)
    {
        "prompt": "Find the online veterinary textbook at example.vet.edu and tell me the surname of the veterinarian mentioned in Chapter 5.",
        "required_tools": ["web_search", "read_url", "search_in_document"],
        "explanation": "Searches for the textbook, reads the specific chapter, finds the veterinarian's name"
    },
    
    # Prompt 15: NASA Award Number (multi-step: news article → paper → award number)
    {
        "prompt": "Find the recent NASA news article about exoplanets, locate the linked research paper, and extract the NASA award number from the paper.",
        "required_tools": ["web_search", "read_url", "extract_links", "search_in_document"],
        "explanation": "Searches for article, extracts link to paper, reads paper, searches for award number"
    },
    
    # Prompt 16: Specimen Deposition (scientific paper retrieval)
    {
        "prompt": "Find the scientific paper titled 'New Species Discovery in Amazon' and tell me where the type specimen was deposited.",
        "required_tools": ["web_search", "read_url", "search_in_document"],
        "explanation": "Searches for the paper, reads it, finds specimen deposition information"
    },
]

# Simple test examples for interactive testing:
SIMPLE_TESTS = [
    "Search the web for information about Python programming",
    "Read the content from https://en.wikipedia.org/wiki/Artificial_intelligence",
    "Extract all links from https://news.ycombinator.com",
    "Search for the word 'example' in the webpage https://example.com",
]

if __name__ == "__main__":
    print("Phase 2 Test Examples")
    print("=" * 70)
    print("\nSimple Tests (try these first):")
    for i, test in enumerate(SIMPLE_TESTS, 1):
        print(f"{i}. {test}")
    
    print("\n\nComplex Challenge Prompts:")
    for i, example in enumerate(PHASE_2_EXAMPLES, 1):
        print(f"\n{i}. {example['prompt']}")
        print(f"   Tools: {', '.join(example['required_tools'])}")
        print(f"   How: {example['explanation']}")
