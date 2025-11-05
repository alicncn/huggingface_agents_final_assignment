"""
Test YouTube video transcription

This script tests the ability to download and transcribe YouTube videos.
"""

from dotenv import load_dotenv
from tools.video_analyzer import transcribe_video

# Load environment variables
load_dotenv()

def test_youtube_transcription():
    """Test transcribing a YouTube video."""
    print("="*80)
    print("  YOUTUBE VIDEO TRANSCRIPTION TEST")
    print("="*80 + "\n")
    
    # YouTube Shorts URL from your example
    youtube_url = "https://www.youtube.com/shorts/dVhL45S1H2M"
    
    print(f"Testing with YouTube URL: {youtube_url}\n")
    print("This will:")
    print("1. Download the YouTube video using yt-dlp")
    print("2. Extract the audio track")
    print("3. Transcribe it using Whisper")
    print("\n" + "-"*80 + "\n")
    
    try:
        # Transcribe the video
        result = transcribe_video.invoke({
            "video_path": youtube_url,
            "language": None  # Auto-detect
        })
        
        print("\n" + "="*80)
        print("  TRANSCRIPTION RESULT")
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80 + "\n")
        
        # Check if it mentions "bite size"
        if "bite" in result.lower():
            print("✅ SUCCESS! Found the word 'bite' in the transcription!")
        else:
            print("⚠️ Transcription completed but 'bite' not found in the text.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        return False
    
    return True


if __name__ == "__main__":
    print("\nStarting YouTube transcription test...")
    print("Note: This may take a minute to download and process the video.\n")
    
    success = test_youtube_transcription()
    
    if success:
        print("\n✅ YouTube video transcription is WORKING!")
        print("\nYou can now ask the agent questions like:")
        print('  - "Transcribe this YouTube video: [URL]"')
        print('  - "What does he say in this video: [YouTube URL]"')
        print('  - "Analyze this YouTube video: [URL]"')
    else:
        print("\n❌ Test failed. Check the error message above.")
    
    print()
