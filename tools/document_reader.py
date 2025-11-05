"""Document and URL reading tools."""
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from typing import Optional


@tool
def read_url(url: str, extract_text_only: bool = True) -> str:
    """
    Read and extract content from a URL.
    
    Args:
        url: The URL to read
        extract_text_only: If True, extracts only text content. If False, includes some HTML structure.
    
    Returns:
        The extracted content from the URL
    """
    try:
        # Send GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        if extract_text_only:
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up excessive whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)
            
            # Limit length to avoid token overflow
            max_chars = 10000
            if len(text) > max_chars:
                text = text[:max_chars] + f"\n\n[Content truncated - {len(text)} total characters]"
            
            return f"Content from {url}:\n\n{text}"
        else:
            # Return formatted HTML
            return f"Content from {url}:\n\n{soup.prettify()[:10000]}"
        
    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 10 seconds"
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL {url}: {str(e)}"
    except Exception as e:
        return f"Error processing URL {url}: {str(e)}"


@tool
def extract_links(url: str, filter_text: Optional[str] = None) -> str:
    """
    Extract all links from a webpage.
    
    Args:
        url: The URL to extract links from
        filter_text: Optional text to filter links (only return links containing this text)
    
    Returns:
        A list of links found on the page
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            
            # Make relative URLs absolute
            if href.startswith('/'):
                from urllib.parse import urljoin
                href = urljoin(url, href)
            
            # Apply filter if specified
            if filter_text:
                if filter_text.lower() in href.lower() or filter_text.lower() in text.lower():
                    links.append(f"{text}: {href}")
            else:
                if href.startswith('http'):  # Only include absolute URLs
                    links.append(f"{text}: {href}")
        
        if not links:
            return "No links found matching the criteria."
        
        # Limit number of links to avoid overwhelming output
        max_links = 50
        result = f"Found {len(links)} links on {url}:\n\n"
        result += "\n".join(links[:max_links])
        
        if len(links) > max_links:
            result += f"\n\n[{len(links) - max_links} more links not shown]"
        
        return result
        
    except Exception as e:
        return f"Error extracting links from {url}: {str(e)}"


@tool
def search_in_document(url: str, search_term: str, context_chars: int = 200) -> str:
    """
    Search for specific text within a document/webpage and return surrounding context.
    
    Args:
        url: The URL of the document to search
        search_term: The text to search for
        context_chars: Number of characters of context to show before and after the match
    
    Returns:
        All occurrences of the search term with surrounding context
    """
    try:
        # Get the document content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        # Find all occurrences
        occurrences = []
        search_lower = search_term.lower()
        text_lower = text.lower()
        
        start = 0
        while True:
            pos = text_lower.find(search_lower, start)
            if pos == -1:
                break
            
            # Get context
            context_start = max(0, pos - context_chars)
            context_end = min(len(text), pos + len(search_term) + context_chars)
            
            context = text[context_start:context_end]
            
            # Add ellipsis if truncated
            if context_start > 0:
                context = "..." + context
            if context_end < len(text):
                context = context + "..."
            
            occurrences.append(context)
            start = pos + 1
        
        if not occurrences:
            return f"'{search_term}' not found in {url}"
        
        result = f"Found {len(occurrences)} occurrence(s) of '{search_term}' in {url}:\n\n"
        for i, occurrence in enumerate(occurrences[:10], 1):  # Limit to 10 occurrences
            result += f"{i}. {occurrence}\n\n"
        
        if len(occurrences) > 10:
            result += f"[{len(occurrences) - 10} more occurrences not shown]"
        
        return result
        
    except Exception as e:
        return f"Error searching document {url}: {str(e)}"
