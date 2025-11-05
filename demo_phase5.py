"""
Demonstration of Phase 5: Database Query Tools
Shows database querying capabilities with real examples.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.database_query import (
    list_available_databases,
    get_database_schema,
    query_database,
    explore_table,
    ask_database
)


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_list_databases():
    """Demo: List available databases."""
    print_header("DEMO 1: List Available Databases")
    
    result = list_available_databases.invoke({})
    print(result)


def demo_schema_exploration():
    """Demo: Explore database schema."""
    print_header("DEMO 2: Explore Database Schema")
    
    print("\nBaseball Database Schema:")
    print("-" * 70)
    result = get_database_schema.invoke({"database_name": "baseball"})
    print(result)
    
    print("\n\nOlympics Database Schema:")
    print("-" * 70)
    result = get_database_schema.invoke({"database_name": "olympics"})
    print(result)


def demo_direct_queries():
    """Demo: Direct SQL queries."""
    print_header("DEMO 3: Direct SQL Queries")
    
    # Query 1: Top players by walks
    print("\nQuery 1: Top 5 players by walks in a single season")
    print("-" * 70)
    sql = """
        SELECT p.name, s.year, s.walks, s.games_played
        FROM players p
        JOIN statistics s ON p.player_id = s.player_id
        WHERE s.walks > 0
        ORDER BY s.walks DESC
        LIMIT 5
    """
    result = query_database.invoke({"database_name": "baseball", "sql_query": sql})
    print(result)
    
    # Query 2: Historical countries
    print("\n\nQuery 2: Countries that no longer exist")
    print("-" * 70)
    sql = "SELECT country_name, country_code FROM countries WHERE exists_today = 0"
    result = query_database.invoke({"database_name": "olympics", "sql_query": sql})
    print(result)


def demo_table_exploration():
    """Demo: Quick table exploration."""
    print_header("DEMO 4: Explore Table Contents")
    
    print("\nExploring 'players' table (first 5 rows):")
    print("-" * 70)
    result = explore_table.invoke({
        "database_name": "baseball",
        "table_name": "players",
        "limit": 5
    })
    print(result)
    
    print("\n\nExploring 'jersey_numbers' table:")
    print("-" * 70)
    result = explore_table.invoke({
        "database_name": "baseball",
        "table_name": "jersey_numbers",
        "limit": 5
    })
    print(result)


def demo_natural_language():
    """Demo: Natural language queries."""
    print_header("DEMO 5: Natural Language Queries")
    
    # Question 1: Jersey number
    print("\nQuestion 1: What was Derek Jeter's jersey number?")
    print("-" * 70)
    result = ask_database.invoke({
        "question": "What was Derek Jeter's jersey number?",
        "database_name": "baseball"
    })
    print(result)
    
    # Question 2: Most walks
    print("\n\nQuestion 2: Who had the most walks?")
    print("-" * 70)
    result = ask_database.invoke({
        "question": "Who had the most walks in a single season?",
        "database_name": "baseball"
    })
    print(result)
    
    # Question 3: Historical countries
    print("\n\nQuestion 3: Which Olympic countries no longer exist?")
    print("-" * 70)
    result = ask_database.invoke({
        "question": "Which countries no longer exist?",
        "database_name": "olympics"
    })
    print(result)


def demo_complex_queries():
    """Demo: Complex analytical queries."""
    print_header("DEMO 6: Complex Analytical Queries")
    
    # Team size analysis
    print("\nQuery: Tokyo 2020 Olympic team sizes")
    print("-" * 70)
    sql = """
        SELECT c.country_name, COUNT(a.athlete_id) as team_size
        FROM countries c
        JOIN athletes a ON c.country_id = a.country_id
        WHERE c.exists_today = 1
        GROUP BY c.country_name
        ORDER BY team_size DESC
        LIMIT 5
    """
    result = query_database.invoke({"database_name": "olympics", "sql_query": sql})
    print(result)
    
    # Player statistics summary
    print("\n\nQuery: Derek Jeter career statistics")
    print("-" * 70)
    sql = """
        SELECT 
            p.name,
            COUNT(s.stat_id) as seasons,
            SUM(s.games_played) as total_games,
            SUM(s.hits) as total_hits,
            SUM(s.walks) as total_walks,
            ROUND(AVG(s.batting_average), 3) as avg_batting_avg
        FROM players p
        JOIN statistics s ON p.player_id = s.player_id
        WHERE p.name LIKE '%Jeter%'
        GROUP BY p.name
    """
    result = query_database.invoke({"database_name": "baseball", "sql_query": sql})
    print(result)


def main():
    """Run all demonstrations."""
    print("="*70)
    print("  PHASE 5 DEMONSTRATION: DATABASE QUERY TOOLS")
    print("="*70)
    print("\nThis demo showcases database querying capabilities including:")
    print("  • Database discovery and schema exploration")
    print("  • Direct SQL query execution")
    print("  • Table content exploration")
    print("  • Natural language to SQL conversion")
    print("  • Complex analytical queries")
    
    try:
        demo_list_databases()
        demo_schema_exploration()
        demo_direct_queries()
        demo_table_exploration()
        demo_natural_language()
        demo_complex_queries()
        
        print("\n" + "="*70)
        print("  DEMO COMPLETE")
        print("="*70)
        print("\n✅ All database tools demonstrated successfully!")
        print("\nKey Features:")
        print("  ✓ 3 databases available (baseball, olympics, competitions)")
        print("  ✓ SQL query execution with formatted results")
        print("  ✓ Schema inspection and table exploration")
        print("  ✓ Natural language to SQL conversion (for common patterns)")
        print("  ✓ Support for complex joins and aggregations")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("\nMake sure to run setup_databases.py first!")


if __name__ == "__main__":
    main()
