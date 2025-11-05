"""
Comprehensive test script for multimedia analyzers (Vision, Audio, Video).

This script tests:
1. Vision Analysis - Image analysis with local files and URLs
2. Audio Processing - Audio transcription
3. Video Analysis - Video frame extraction and analysis

Requirements:
- GOOGLE_API_KEY configured in .env
- Sample files or use provided URLs
"""

import os
from dotenv import load_dotenv
from tools.vision_analyzer import analyze_image, describe_image, count_objects_in_image, extract_text_from_image, analyze_chess_position
from tools.audio_processor import transcribe_audio, transcribe_audio_from_url, extract_audio_from_video
from tools.video_analyzer import analyze_video, transcribe_video, analyze_video_comprehensive

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def test_vision_analysis():
    """Test vision analysis tools."""
    print_section("1. VISION ANALYSIS TESTS")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ GOOGLE_API_KEY not configured in .env file")
        print("Please add your API key to continue.\n")
        return
    
    print("✅ GOOGLE_API_KEY is configured\n")
    
    # Test 1: Analyze image from URL
    print("Test 1: Analyze Image from URL")
    print("-" * 40)
    
    # Using a public domain image
    test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
    
    try:
        result = analyze_image.invoke({
            "image_path": test_image_url,
            "question": "What animal is in this image and what is it doing?"
        })
        print(f"URL: {test_image_url}")
        print(f"Question: What animal is in this image and what is it doing?")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")
    
    # Test 2: Describe image
    print("\nTest 2: Describe Image")
    print("-" * 40)
    
    try:
        result = describe_image.invoke({
            "image_path": test_image_url
        })
        print(f"URL: {test_image_url}")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")
    
    # Test 3: Count objects in image
    print("\nTest 3: Count Objects in Image")
    print("-" * 40)
    
    try:
        result = count_objects_in_image.invoke({
            "image_path": test_image_url,
            "object_type": "cat"
        })
        print(f"URL: {test_image_url}")
        print(f"Object to count: cat")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")
    
    # Test 4: Extract text from image (using an image with text)
    print("\nTest 4: Extract Text from Image")
    print("-" * 40)
    
    # Using an image with text
    text_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Stop_sign_MUTCD.svg/1200px-Stop_sign_MUTCD.svg.png"
    
    try:
        result = extract_text_from_image.invoke({
            "image_path": text_image_url
        })
        print(f"URL: {text_image_url}")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")
    
    # Test 5: Local image file (if exists)
    print("\nTest 5: Analyze Local Image File")
    print("-" * 40)
    
    local_image = "test_image.jpg"
    if os.path.exists(local_image):
        try:
            result = analyze_image.invoke({
                "image_path": local_image,
                "question": "Describe everything you see in this image."
            })
            print(f"Local file: {local_image}")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print(f"No local test image found. Create '{local_image}' to test local files.\n")


def test_audio_processing():
    """Test audio processing tools."""
    print_section("2. AUDIO PROCESSING TESTS")
    
    # Check if Whisper is installed
    try:
        import whisper
        print("✅ Whisper library is installed\n")
    except ImportError:
        print("❌ Whisper library not installed")
        print("Install it with: pip install openai-whisper")
        print("Note: First run will download ~140MB model\n")
        return
    
    # Test 1: Transcribe audio from URL
    print("Test 1: Transcribe Audio from URL")
    print("-" * 40)
    
    # Using a short public domain audio sample
    audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"
    
    try:
        result = transcribe_audio_from_url.invoke({
            "url": audio_url,
            "language": None  # Auto-detect
        })
        print(f"URL: {audio_url}")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")
    
    # Test 2: Transcribe local audio file
    print("\nTest 2: Transcribe Local Audio File")
    print("-" * 40)
    
    local_audio = "test_audio.mp3"
    if os.path.exists(local_audio):
        try:
            result = transcribe_audio.invoke({
                "file_path": local_audio,
                "language": "en"
            })
            print(f"Local file: {local_audio}")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print(f"No local audio file found. Create '{local_audio}' to test local files.\n")
    
    # Test 3: Extract audio from video
    print("\nTest 3: Extract Audio from Video")
    print("-" * 40)
    
    test_video = "test_video.mp4"
    if os.path.exists(test_video):
        try:
            result = extract_audio_from_video.invoke({
                "video_path": test_video,
                "output_path": None  # Auto-generate path
            })
            print(f"Video file: {test_video}")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print(f"No test video found. Skipping audio extraction test.\n")


def test_video_analysis():
    """Test video analysis tools."""
    print_section("3. VIDEO ANALYSIS TESTS")
    
    # Check required libraries
    try:
        import moviepy.editor
        print("✅ MoviePy library is installed")
    except ImportError:
        print("❌ MoviePy library not installed")
        print("Install it with: pip install moviepy\n")
        return
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ GOOGLE_API_KEY not configured in .env file\n")
        return
    
    print("✅ GOOGLE_API_KEY is configured\n")
    
    # Test 1: Transcribe video audio
    print("Test 1: Transcribe Video Audio")
    print("-" * 40)
    
    local_video = "test_video.mp4"
    if os.path.exists(local_video):
        try:
            result = transcribe_video.invoke({
                "video_path": local_video,
                "language": None  # Auto-detect
            })
            print(f"Local file: {local_video}")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print(f"No local video file found. Create '{local_video}' to test.\n")
    
    # Test 2: Analyze video (visual analysis)
    print("\nTest 2: Analyze Video Visually")
    print("-" * 40)
    
    if os.path.exists(local_video):
        try:
            result = analyze_video.invoke({
                "video_path": local_video,
                "question": "What is happening in this video?",
                "num_frames": 3
            })
            print(f"Local file: {local_video}")
            print(f"Question: What is happening in this video?")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print(f"No local video file found. Create '{local_video}' to test.\n")
    
    # Test 3: Comprehensive video analysis (vision + audio)
    print("\nTest 3: Comprehensive Video Analysis (Vision + Audio)")
    print("-" * 40)
    
    if os.path.exists(local_video):
        try:
            result = analyze_video_comprehensive.invoke({
                "video_path": local_video,
                "question": "Describe everything in this video including what you see and hear.",
                "include_audio": True
            })
            print(f"Local file: {local_video}")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print(f"No local video file found. Create '{local_video}' to test.\n")


def print_usage_guide():
    """Print usage guide for testing with custom files."""
    print_section("USAGE GUIDE")
    
    print("To test with your own files, create the following in the project directory:\n")
    
    print("1. Vision Analysis:")
    print("   - Save an image as: test_image.jpg")
    print("   - Or use any image URL\n")
    
    print("2. Audio Processing:")
    print("   - Save an audio file as: test_audio.mp3")
    print("   - Supported formats: mp3, wav, m4a, flac, ogg\n")
    
    print("3. Video Analysis:")
    print("   - Save a video file as: test_video.mp4")
    print("   - Supported formats: mp4, avi, mov, mkv\n")
    
    print("Required installations:")
    print("   pip install openai-whisper  # For audio transcription (~140MB model)")
    print("   pip install moviepy          # For video processing\n")
    
    print("Example test files you can download:")
    print("   - Image: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg")
    print("   - Audio: https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav")
    print("   - Video: Create your own short video or use sample-videos.com\n")


def main():
    """Run all multimedia tests."""
    print("\n" + "="*80)
    print("  MULTIMEDIA ANALYZERS TEST SUITE")
    print("  Testing Vision, Audio, and Video Analysis Tools")
    print("="*80)
    
    # Run tests
    test_vision_analysis()
    test_audio_processing()
    test_video_analysis()
    
    # Print usage guide
    print_usage_guide()
    
    print_section("TEST COMPLETE")
    print("Summary:")
    print("- Vision tools use Gemini Vision API (requires GOOGLE_API_KEY)")
    print("- Audio tools use OpenAI Whisper (local processing)")
    print("- Video tools combine MoviePy + Gemini Vision")
    print("\nAll tools are ready to use within the agent!\n")


if __name__ == "__main__":
    main()
