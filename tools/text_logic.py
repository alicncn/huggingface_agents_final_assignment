"""Text manipulation and logic tools for puzzles and reasoning tasks."""
from typing import Optional, List
from langchain_core.tools import tool


@tool
def reverse_text(text: str) -> str:
    """
    Reverse a text string.
    
    Args:
        text: Text to reverse
    
    Returns:
        Reversed text
    """
    return f"Reversed: {text[::-1]}"


@tool
def reverse_words(text: str) -> str:
    """
    Reverse the order of words in text.
    
    Args:
        text: Text with words to reverse
    
    Returns:
        Text with words in reversed order
    """
    words = text.split()
    reversed_words = words[::-1]
    return " ".join(reversed_words)


@tool
def get_word_at_position(text: str, position: int) -> str:
    """
    Get the word at a specific position in text.
    
    Args:
        text: The text to search
        position: Position of the word (1-indexed, e.g., 1 = first word, 3 = third word)
    
    Returns:
        The word at that position
    """
    words = text.split()
    
    if position < 1 or position > len(words):
        return f"Error: Position {position} is out of range. Text has {len(words)} words."
    
    word = words[position - 1]
    return f"Word at position {position}: {word}"


@tool
def find_antonym(word: str) -> str:
    """
    Find common antonyms for a word.
    
    Args:
        word: Word to find antonym for
    
    Returns:
        Antonym or suggestions
    """
    # Common antonym pairs
    antonyms = {
        # Basic adjectives
        "hot": "cold", "cold": "hot",
        "big": "small", "small": "big",
        "large": "small", "tiny": "huge",
        "tall": "short", "short": "tall",
        "long": "short",
        "wide": "narrow", "narrow": "wide",
        "thick": "thin", "thin": "thick",
        "heavy": "light", "light": "heavy",
        "hard": "soft", "soft": "hard",
        "strong": "weak", "weak": "strong",
        "fast": "slow", "slow": "fast",
        "quick": "slow",
        "high": "low", "low": "high",
        "deep": "shallow", "shallow": "deep",
        "loud": "quiet", "quiet": "loud",
        "bright": "dark", "dark": "bright",
        "clean": "dirty", "dirty": "clean",
        "new": "old", "old": "new",
        "young": "old",
        "early": "late", "late": "early",
        "near": "far", "far": "near",
        "close": "far",
        
        # Verbs
        "start": "stop", "stop": "start",
        "begin": "end", "end": "begin",
        "open": "close", "close": "open",
        "push": "pull", "pull": "push",
        "give": "take", "take": "give",
        "buy": "sell", "sell": "buy",
        "love": "hate", "hate": "love",
        "win": "lose", "lose": "win",
        "remember": "forget", "forget": "remember",
        
        # Adverbs
        "always": "never", "never": "always",
        "often": "rarely", "rarely": "often",
        "up": "down", "down": "up",
        "in": "out", "out": "in",
        "inside": "outside", "outside": "inside",
        "before": "after", "after": "before",
        "above": "below", "below": "above",
        "over": "under", "under": "over",
        
        # Nouns
        "day": "night", "night": "day",
        "summer": "winter", "winter": "summer",
        "friend": "enemy", "enemy": "friend",
        "question": "answer", "answer": "question",
        "beginning": "end",
        "front": "back", "back": "front",
        "top": "bottom", "bottom": "top",
    }
    
    word_lower = word.lower()
    
    if word_lower in antonyms:
        return f"Antonym of '{word}': {antonyms[word_lower]}"
    else:
        return f"No built-in antonym found for '{word}'. This tool has {len(antonyms)//2} common antonym pairs. For other words, use web search or ask the LLM directly."


@tool  
def check_palindrome(text: str) -> str:
    """
    Check if text is a palindrome.
    
    Args:
        text: Text to check
    
    Returns:
        Whether the text is a palindrome
    """
    # Remove spaces and convert to lowercase
    clean_text = text.replace(" ", "").lower()
    is_palindrome = clean_text == clean_text[::-1]
    
    if is_palindrome:
        return f"'{text}' IS a palindrome"
    else:
        return f"'{text}' is NOT a palindrome"


@tool
def count_words(text: str) -> str:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
    
    Returns:
        Word count
    """
    words = text.split()
    return f"Word count: {len(words)}"


@tool
def extract_numbers(text: str) -> str:
    """
    Extract all numbers from text.
    
    Args:
        text: Text to extract numbers from
    
    Returns:
        List of numbers found
    """
    import re
    numbers = re.findall(r'\d+', text)
    
    if numbers:
        return f"Numbers found: {', '.join(numbers)}"
    else:
        return "No numbers found in text"


@tool
def categorize_fruits_vegetables(items: List[str]) -> str:
    """
    Categorize items as fruits or vegetables based on botanical definitions.
    
    Args:
        items: List of food items to categorize
    
    Returns:
        Categorization of each item (botanical classification)
    """
    # Botanical definitions:
    # Fruit: developed from the flower and contains seeds
    # Vegetable: other edible plant parts (leaves, stems, roots)
    
    fruits = {
        "tomato", "cucumber", "pepper", "bell pepper", "eggplant", "aubergine",
        "squash", "zucchini", "pumpkin", "avocado", "olive", "okra",
        "apple", "banana", "orange", "grape", "strawberry", "blueberry",
        "peach", "pear", "plum", "cherry", "watermelon", "melon",
        "mango", "pineapple", "papaya", "kiwi", "lemon", "lime",
        "bean", "green bean", "pea", "peas", "corn", "maize"
    }
    
    vegetables = {
        "carrot", "potato", "onion", "garlic", "lettuce", "spinach",
        "cabbage", "broccoli", "cauliflower", "celery", "asparagus",
        "radish", "beet", "turnip", "parsnip", "kale", "chard",
        "leek", "scallion", "artichoke", "rhubarb"
    }
    
    results = []
    for item in items:
        item_lower = item.lower().strip()
        
        if item_lower in fruits:
            results.append(f"{item}: FRUIT (botanical)")
        elif item_lower in vegetables:
            results.append(f"{item}: VEGETABLE (botanical)")
        else:
            results.append(f"{item}: UNKNOWN (not in database)")
    
    return "\n".join(results)
