"""Tool registry for managing all available tools."""
from typing import List
from langchain_core.tools import Tool

# Phase 2: Information Retrieval Tools
from tools.web_search import web_search, web_search_wikipedia
from tools.document_reader import read_url, extract_links, search_in_document

# Phase 3: Multimedia Analysis Tools
from tools.audio_processor import transcribe_audio, transcribe_audio_from_url, extract_audio_from_video
from tools.vision_analyzer import (
    analyze_image, count_objects_in_image, describe_image,
    extract_text_from_image, analyze_chess_position
)
from tools.video_analyzer import analyze_video, transcribe_video, analyze_video_comprehensive

# Phase 4: Code, Data, and Logic Tools
from tools.code_interpreter import execute_python_code, evaluate_python_expression, analyze_code_output
from tools.data_analyzer import (
    read_excel_file, read_csv_file, analyze_excel_data,
    filter_excel_data, calculate_from_excel
)
from tools.chess_engine import analyze_chess_fen, get_chess_position_info, validate_chess_move
from tools.text_logic import (
    reverse_text, reverse_words, get_word_at_position, find_antonym,
    check_palindrome, count_words, extract_numbers, categorize_fruits_vegetables
)

# Phase 5: Database Query Tools
from tools.database_query import (
    query_database, get_database_schema, ask_database,
    list_available_databases, explore_table
)


def get_all_tools() -> List[Tool]:
    """
    Get all available tools for the agent.
    
    Returns:
        List of LangChain Tool objects
    """
    tools = []
    
    # Phase 2: Web search and document reader
    tools.extend([
        web_search,
        web_search_wikipedia,
        read_url,
        extract_links,
        search_in_document,
    ])
    
    # Phase 3: Multimedia analysis
    tools.extend([
        # Audio tools
        transcribe_audio,
        transcribe_audio_from_url,
        extract_audio_from_video,
        # Vision tools
        analyze_image,
        count_objects_in_image,
        describe_image,
        extract_text_from_image,
        analyze_chess_position,
        # Video tools
        analyze_video,
        transcribe_video,
        analyze_video_comprehensive,
    ])
    
    # Phase 4: Code interpreter, data analysis, chess, logic
    tools.extend([
        # Code execution
        execute_python_code,
        evaluate_python_expression,
        analyze_code_output,
        # Data analysis
        read_excel_file,
        read_csv_file,
        analyze_excel_data,
        filter_excel_data,
        calculate_from_excel,
        # Chess engine
        analyze_chess_fen,
        get_chess_position_info,
        validate_chess_move,
        # Text and logic
        reverse_text,
        reverse_words,
        get_word_at_position,
        find_antonym,
        check_palindrome,
        count_words,
        extract_numbers,
        categorize_fruits_vegetables,
    ])
    
    # Phase 5: Database query tools
    tools.extend([
        query_database,
        get_database_schema,
        ask_database,
        list_available_databases,
        explore_table,
    ])
    
    return tools
