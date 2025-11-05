"""Web search tool using Tavily API."""
import os
from typing import Optional
from langchain_core.tools import tool


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for information using Tavily API.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        A formatted string containing search results with titles, URLs, and snippets
    """
    try:
        from tavily import TavilyClient
        
        # Get API key from environment
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not found in environment variables. Please add it to your .env file."
        
        # Initialize client
        client = TavilyClient(api_key=api_key)
        
        # Perform search
        response = client.search(
            query=query,
            max_results=max_results,
            include_answer=True,
            include_raw_content=False
        )
        
        # Format results
        results = []
        
        # Add the AI-generated answer if available
        if response.get("answer"):
            results.append(f"Quick Answer: {response['answer']}\n")
        
        # Add individual search results
        results.append("Search Results:")
        for i, result in enumerate(response.get("results", []), 1):
            title = result.get("title", "No title")
            url = result.get("url", "")
            content = result.get("content", "No content available")
            
            results.append(f"\n{i}. {title}")
            results.append(f"   URL: {url}")
            results.append(f"   {content}")
        
        return "\n".join(results) if results else "No results found."
        
    except ImportError:
        return "Error: Tavily library not installed. Run: pip install tavily-python"
    except Exception as e:
        return f"Error performing web search: {str(e)}"


@tool
def web_search_wikipedia(query: str, year: Optional[int] = None) -> str:
    """
    Search Wikipedia for information. Useful for historical data and factual queries.
    
    Args:
        query: The search query
        year: Optional year to focus the search (e.g., 2022 for "2022 version")
    
    Returns:
        Wikipedia search results
    """
    # Enhance query for Wikipedia
    wiki_query = f"{query} site:wikipedia.org"
    if year:
        wiki_query += f" {year}"
    
    return web_search(wiki_query, max_results=3)
