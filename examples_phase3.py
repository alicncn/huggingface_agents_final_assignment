"""
Test examples for Phase 3: Multimedia Analysis Tools

These examples demonstrate the capabilities added in Phase 3.
"""

# Example prompts that Phase 3 can now handle:

PHASE_3_EXAMPLES = [
    # Prompt 2: Birds in Video
    {
        "prompt": "How many different species of birds are visible in this video: video.mp4",
        "required_tools": ["analyze_video", "count_objects_in_image"],
        "explanation": "Extracts frames from video and uses vision AI to identify and count bird species"
    },
    
    # Prompt 4: Chess Position
    {
        "prompt": "Analyze this chess board image (chess.jpg) and tell me the best move",
        "required_tools": ["analyze_chess_position"],
        "explanation": "Uses vision to read the board position and suggest optimal move"
    },
    
    # Prompt 7: Video Dialogue
    {
        "prompt": "What does the character say in response to the question about time in this video: movie.mp4",
        "required_tools": ["transcribe_video"],
        "explanation": "Transcribes video audio and finds the specific dialogue"
    },
    
    # Prompt 11: Pie Ingredients from Audio
    {
        "prompt": "Listen to this audio recipe (recipe.mp3) and list only the ingredients for the pie, excluding measurements",
        "required_tools": ["transcribe_audio"],
        "explanation": "Transcribes audio and extracts ingredient names"
    },
    
    # Prompt 14: Homework from Audio
    {
        "prompt": "What page numbers are mentioned in this homework assignment audio: homework.mp3",
        "required_tools": ["transcribe_audio"],
        "explanation": "Transcribes audio and extracts page numbers"
    },
]

# Simple test examples for interactive testing:
SIMPLE_TESTS = [
    "Describe this image: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/300px-Cat03.jpg",
    "Count how many people are in this image: [image_url]",
    "Extract any text from this image: [image_url]",
    "Transcribe this audio file: sample.mp3",
]

# Combined examples (using multiple Phase 2 + Phase 3 tools):
COMBINED_EXAMPLES = [
    {
        "prompt": "Search for a video of birds, download it, and count how many different species appear",
        "phases": ["Phase 2 (web_search)", "Phase 3 (analyze_video, count_objects)"],
        "explanation": "Searches web for video, then analyzes it with vision AI"
    },
    {
        "prompt": "Find a chess puzzle image online and tell me the best move",
        "phases": ["Phase 2 (web_search)", "Phase 3 (analyze_chess_position)"],
        "explanation": "Searches for chess puzzle, analyzes position with vision"
    },
]

if __name__ == "__main__":
    print("Phase 3 Test Examples")
    print("=" * 70)
    
    print("\nSimple Tests:")
    for i, test in enumerate(SIMPLE_TESTS, 1):
        print(f"{i}. {test}")
    
    print("\n\nChallenge Prompts (Phase 3):")
    for i, example in enumerate(PHASE_3_EXAMPLES, 1):
        print(f"\n{i}. {example['prompt']}")
        print(f"   Tools: {', '.join(example['required_tools'])}")
        print(f"   How: {example['explanation']}")
    
    print("\n\nCombined Multi-Phase Examples:")
    for i, example in enumerate(COMBINED_EXAMPLES, 1):
        print(f"\n{i}. {example['prompt']}")
        print(f"   Phases: {' + '.join(example['phases'])}")
        print(f"   How: {example['explanation']}")
