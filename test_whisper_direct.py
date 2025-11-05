"""
Simple Whisper test with the extracted audio file
"""

import os
import whisper

# The audio file that was extracted
audio_file = r"C:\Users\alican.can\AppData\Local\Temp\tmpddanp5xe.mp3"

if not os.path.exists(audio_file):
    print(f"Audio file not found: {audio_file}")
    print("\nRun debug_youtube.py first to create the audio file, then immediately run this script")
    exit(1)

print(f"Audio file exists: {os.path.exists(audio_file)}")
print(f"Audio file size: {os.path.getsize(audio_file)} bytes\n")

print("Loading Whisper model...")
model = whisper.load_model("base")

print("Transcribing...")
try:
    result = model.transcribe(audio_file, fp16=False)  # Disable fp16 for CPU
    print("\n" + "="*80)
    print("SUCCESS!")
    print("="*80)
    print(f"\nTranscription: {result['text']}")
    print(f"Language: {result['language']}")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
