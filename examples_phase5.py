"""
Example prompts for Phase 5: Database Query Tools

These prompts test database querying capabilities using the agent.
Run these through main.py to test the agent's database query abilities.
"""

PHASE_5_PROMPTS = [
    # Prompt 10: Baseball statistics
    {
        "number": 10,
        "category": "Database Query",
        "prompt": "In the baseball database, which player had the most walks in a single season? Include the year and number of walks.",
        "expected_tools": ["query_database", "ask_database"],
        "notes": "Tests SQL aggregation and ordering"
    },
    
    # Prompt 13: Jersey numbers
    {
        "number": 13,
        "category": "Database Query",
        "prompt": "What was Derek Jeter's jersey number during his career with the Yankees?",
        "expected_tools": ["query_database", "ask_database"],
        "notes": "Tests table joins and player lookup"
    },
    
    # Prompt 17: Olympic team sizes
    {
        "number": 17,
        "category": "Database Query",
        "prompt": "Which country had the largest team at the Tokyo 2020 Olympics?",
        "expected_tools": ["query_database", "ask_database"],
        "notes": "Tests grouping and counting"
    },
    
    # Prompt 18: Historical countries
    {
        "number": 18,
        "category": "Database Query",
        "prompt": "List all countries in the Olympics database that no longer exist today.",
        "expected_tools": ["query_database", "ask_database"],
        "notes": "Tests filtering with boolean conditions"
    },
    
    # Prompt 20: Competition winners
    {
        "number": 20,
        "category": "Database Query",
        "prompt": "Who won the International Math Olympiad in 1990, and from which country that no longer exists?",
        "expected_tools": ["query_database", "ask_database"],
        "notes": "Tests complex joins across multiple tables"
    },
]


# Additional test prompts for database exploration
EXPLORATION_PROMPTS = [
    "What databases are available?",
    "Show me the schema of the baseball database.",
    "What tables are in the Olympics database?",
    "Show me the first 5 players in the baseball database.",
    "List the historical countries in the Olympics database.",
]


# Advanced query prompts
ADVANCED_PROMPTS = [
    "Calculate Derek Jeter's career batting average across all seasons.",
    "Which Yankee player had the highest batting average in any single season?",
    "How many countries participated in the Tokyo 2020 Olympics?",
    "Show me all competitions from the 1990s won by athletes from historical countries.",
    "What was Babe Ruth's best home run season?",
]


def print_all_prompts():
    """Print all Phase 5 example prompts."""
    print("="*80)
    print("PHASE 5 EXAMPLE PROMPTS: DATABASE QUERY TOOLS")
    print("="*80)
    
    print("\n📊 ORIGINAL CHALLENGE PROMPTS (Database-related)")
    print("-" * 80)
    for prompt_info in PHASE_5_PROMPTS:
        print(f"\nPrompt #{prompt_info['number']}: {prompt_info['category']}")
        print(f"  Question: {prompt_info['prompt']}")
        print(f"  Expected Tools: {', '.join(prompt_info['expected_tools'])}")
        print(f"  Notes: {prompt_info['notes']}")
    
    print("\n\n🔍 EXPLORATION PROMPTS")
    print("-" * 80)
    for i, prompt in enumerate(EXPLORATION_PROMPTS, 1):
        print(f"{i}. {prompt}")
    
    print("\n\n⚡ ADVANCED QUERY PROMPTS")
    print("-" * 80)
    for i, prompt in enumerate(ADVANCED_PROMPTS, 1):
        print(f"{i}. {prompt}")
    
    print("\n" + "="*80)
    print(f"Total: {len(PHASE_5_PROMPTS)} challenge prompts, "
          f"{len(EXPLORATION_PROMPTS)} exploration prompts, "
          f"{len(ADVANCED_PROMPTS)} advanced prompts")
    print("="*80)


if __name__ == "__main__":
    print_all_prompts()
    
    print("\n\n📝 USAGE INSTRUCTIONS")
    print("="*80)
    print("1. Make sure databases are set up:")
    print("   python setup_databases.py")
    print()
    print("2. Run the main agent:")
    print("   python main.py")
    print()
    print("3. Enter any of the prompts above to test database querying")
    print()
    print("4. The agent will:")
    print("   - Determine which database to query")
    print("   - Convert natural language to SQL (or use direct SQL)")
    print("   - Execute the query")
    print("   - Return formatted results")
    print("="*80)
