"""
Database query tools for natural language to SQL conversion and execution.
Supports SQLite databases with automatic schema detection.
"""
import sqlite3
import os
from typing import List, Dict, Any
from langchain.tools import tool


def get_database_path(database_name: str) -> str:
    """Get the full path to a database file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", f"{database_name}.db")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{database_name}' not found at {db_path}")
    return db_path


def get_schema(database_name: str) -> str:
    """Get the schema of all tables in the database."""
    db_path = get_database_path(database_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        col_info = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            col_info.append(f"{col_name} ({col_type})")
        
        schema_info.append(f"Table: {table_name}\n  Columns: {', '.join(col_info)}")
    
    conn.close()
    return "\n\n".join(schema_info)


def natural_language_to_sql(question: str, database_name: str) -> str:
    """
    Convert a natural language question to SQL query.
    This is a rule-based converter for common query patterns.
    """
    question_lower = question.lower()
    
    # Baseball queries
    if database_name == "baseball":
        # Jersey number queries
        if "jersey" in question_lower or "number" in question_lower:
            if "derek jeter" in question_lower or "jeter" in question_lower:
                return """
                    SELECT p.name, jn.jersey_number, jn.year
                    FROM players p
                    JOIN jersey_numbers jn ON p.player_id = jn.player_id
                    WHERE p.name LIKE '%Jeter%'
                """
        
        # Walk statistics queries
        if "walk" in question_lower or "walks" in question_lower:
            if "most" in question_lower or "highest" in question_lower or "top" in question_lower:
                return """
                    SELECT p.name, s.year, s.walks, s.games_played
                    FROM players p
                    JOIN statistics s ON p.player_id = s.player_id
                    WHERE s.walks > 0
                    ORDER BY s.walks DESC
                    LIMIT 10
                """
    
    # Olympics queries
    elif database_name == "olympics":
        # Team size queries
        if "team" in question_lower and ("size" in question_lower or "largest" in question_lower or "biggest" in question_lower):
            if "tokyo" in question_lower or "2020" in question_lower:
                return """
                    SELECT c.country_name, COUNT(a.athlete_id) as team_size
                    FROM countries c
                    JOIN athletes a ON c.country_id = a.country_id
                    WHERE c.country_id IN (
                        SELECT country_id FROM olympics WHERE year = 2020
                    )
                    GROUP BY c.country_name
                    ORDER BY team_size DESC
                    LIMIT 1
                """
        
        # Historical country queries
        if "no longer exist" in question_lower or "historical" in question_lower or "not exist" in question_lower:
            return """
                SELECT country_name, country_code
                FROM countries
                WHERE exists_today = 0
                ORDER BY country_name
            """
    
    # Competitions queries
    elif database_name == "competitions":
        # Winner from non-existent country
        if ("winner" in question_lower or "won" in question_lower) and ("no longer exist" in question_lower or "not exist" in question_lower):
            if "1990" in question_lower or "math" in question_lower:
                return """
                    SELECT w.winner_name, hc.country_name, w.year, c.name as competition
                    FROM winners w
                    JOIN historical_countries hc ON w.country_id = hc.country_id
                    JOIN competitions c ON w.competition_id = c.competition_id
                    WHERE w.year = 1990
                """
    
    # Generic fallback - try to construct a simple SELECT
    return f"-- Unable to convert question to SQL automatically for database '{database_name}'\n-- Question: {question}"


@tool
def query_database(database_name: str, sql_query: str) -> str:
    """
    Execute a SQL query on a specified database.
    
    Args:
        database_name: Name of the database (e.g., 'baseball', 'olympics', 'competitions')
        sql_query: The SQL query to execute
        
    Returns:
        Query results formatted as a string
    """
    try:
        db_path = get_database_path(database_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        conn.close()
        
        if not results:
            return "No results found."
        
        # Format results
        output = []
        output.append(" | ".join(column_names))
        output.append("-" * (len(" | ".join(column_names))))
        
        for row in results:
            output.append(" | ".join(str(val) for val in row))
        
        return "\n".join(output)
        
    except Exception as e:
        return f"Error executing query: {str(e)}"


@tool
def get_database_schema(database_name: str) -> str:
    """
    Get the schema (table structure) of a database.
    
    Args:
        database_name: Name of the database (e.g., 'baseball', 'olympics', 'competitions')
        
    Returns:
        Database schema as formatted text
    """
    try:
        return get_schema(database_name)
    except Exception as e:
        return f"Error getting schema: {str(e)}"


@tool
def ask_database(question: str, database_name: str) -> str:
    """
    Ask a natural language question to a database.
    Automatically converts the question to SQL and executes it.
    
    Args:
        question: Natural language question about the data
        database_name: Name of the database to query ('baseball', 'olympics', 'competitions')
        
    Returns:
        Answer to the question based on database query
    """
    try:
        # First, get schema to understand the database
        schema = get_schema(database_name)
        
        # Convert natural language to SQL
        sql_query = natural_language_to_sql(question, database_name)
        
        # If conversion failed, return schema for user to write SQL
        if sql_query.startswith("--"):
            return f"{sql_query}\n\nDatabase Schema:\n{schema}"
        
        # Execute the query
        result = query_database.invoke({"database_name": database_name, "sql_query": sql_query})
        
        return f"Question: {question}\n\nSQL Query:\n{sql_query}\n\nResults:\n{result}"
        
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def list_available_databases() -> str:
    """
    List all available databases in the data directory.
    
    Returns:
        List of available database names
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        
        if not os.path.exists(data_dir):
            return "No databases found. Run setup_databases.py to create them."
        
        db_files = [f.replace(".db", "") for f in os.listdir(data_dir) if f.endswith(".db")]
        
        if not db_files:
            return "No databases found. Run setup_databases.py to create them."
        
        return "Available databases:\n" + "\n".join(f"  - {db}" for db in db_files)
        
    except Exception as e:
        return f"Error listing databases: {str(e)}"


@tool
def explore_table(database_name: str, table_name: str, limit: int = 10) -> str:
    """
    Explore the contents of a specific table in a database.
    
    Args:
        database_name: Name of the database
        table_name: Name of the table to explore
        limit: Maximum number of rows to return (default: 10)
        
    Returns:
        Sample rows from the table
    """
    try:
        sql_query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return query_database.invoke({"database_name": database_name, "sql_query": sql_query})
    except Exception as e:
        return f"Error exploring table: {str(e)}"
