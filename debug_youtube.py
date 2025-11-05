"""
Debug YouTube download and audio extraction
"""

import os
import tempfile
from tools.video_analyzer import download_video_from_url
from tools.audio_processor import extract_audio_from_video

# Test 1: Download the video
print("="*80)
print("Step 1: Download YouTube video")
print("="*80 + "\n")

youtube_url = "https://www.youtube.com/shorts/dVhL45S1H2M"
video_path = download_video_from_url(youtube_url)

if video_path.startswith("Error"):
    print(f"❌ Download failed: {video_path}")
    exit(1)

print(f"✅ Video downloaded to: {video_path}")
print(f"   File exists: {os.path.exists(video_path)}")
print(f"   File size: {os.path.getsize(video_path) / 1024:.2f} KB\n")

# Test 2: Extract audio
print("="*80)
print("Step 2: Extract audio from video")
print("="*80 + "\n")

result = extract_audio_from_video.invoke({"video_path": video_path})
print(f"Result: {result}\n")

if "successfully" in result:
    audio_path = result.split(": ")[-1]
    print(f"✅ Audio extracted!")
    print(f"   Audio file: {audio_path}")
    print(f"   File exists: {os.path.exists(audio_path)}")
    if os.path.exists(audio_path):
        print(f"   File size: {os.path.getsize(audio_path) / 1024:.2f} KB")
    
    # Test 3: Transcribe
    print("\n" + "="*80)
    print("Step 3: Transcribe audio")
    print("="*80 + "\n")
    
    from tools.audio_processor import transcribe_audio
    
    transcription = transcribe_audio.invoke({
        "file_path": audio_path,
        "language": None
    })
    
    print("Transcription result:")
    print(transcription)
    
    # Clean up
    if os.path.exists(audio_path):
        os.unlink(audio_path)
else:
    print(f"❌ Audio extraction failed")

# Clean up video
if os.path.exists(video_path):
    os.unlink(video_path)
    print("\n✅ Cleanup complete")
