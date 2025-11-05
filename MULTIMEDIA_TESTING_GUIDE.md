# Multimedia Testing Guide

## Overview
This guide explains how to test the Vision, Audio, and Video analyzers in your Agentic AI project.

## Available Tools

### 📷 Vision Analysis Tools (5 tools)
1. **analyze_image** - Answer questions about an image
2. **describe_image** - Get a detailed description of an image
3. **count_objects_in_image** - Count specific objects in an image
4. **extract_text_from_image** - Extract text/OCR from an image
5. **analyze_chess_position** - Analyze chess board positions from images

### 🎵 Audio Processing Tools (3 tools)
1. **transcribe_audio** - Convert audio to text using Whisper
2. **transcribe_audio_from_url** - Download and transcribe audio from URL
3. **extract_audio_from_video** - Extract audio track from video files

### 🎬 Video Analysis Tools (3 tools)
1. **analyze_video** - Visual analysis of video frames
2. **transcribe_video** - Transcribe audio from video
3. **analyze_video_comprehensive** - Combined visual + audio analysis

---

## Testing Methods

### Method 1: Using the Interactive Agent (main.py)

The easiest way to test multimedia tools is through the agent:

1. **Start the agent:**
   ```bash
   python main.py
   ```

2. **Test Vision Analysis:**
   ```
   You: Analyze this image: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg and tell me what you see
   ```

3. **Test Audio (with local file):**
   ```
   You: Transcribe the audio file test_audio.mp3
   ```

4. **Test Video (with local file):**
   ```
   You: What's happening in the video test_video.mp4?
   ```

### Method 2: Using test_multimedia.py Script

Run the automated test script:

```bash
python test_multimedia.py
```

This will test:
- ✅ Vision analysis with public image URLs
- ✅ Audio transcription (if Whisper installed)
- ✅ Video analysis (if MoviePy installed)
- ✅ Local file testing (if test files exist)

### Method 3: Direct Tool Testing in Python

```python
from tools.vision_analyzer import analyze_image
from tools.audio_processor import transcribe_audio
from tools.video_analyzer import analyze_video

# Test vision
result = analyze_image.invoke({
    "image_path": "path/to/image.jpg",
    "question": "What's in this image?"
})
print(result)

# Test audio
result = transcribe_audio.invoke({
    "file_path": "path/to/audio.mp3",
    "language": "en"
})
print(result)

# Test video
result = analyze_video.invoke({
    "video_path": "path/to/video.mp4",
    "question": "What happens in this video?",
    "num_frames": 5
})
print(result)
```

---

## Setup Requirements

### 1. Vision Analysis
**Requirements:**
- ✅ `GOOGLE_API_KEY` in `.env` file
- ✅ `langchain-google-genai` package (already installed)

**No additional setup needed!** Works with URLs and local images.

### 2. Audio Processing
**Requirements:**
- ✅ Whisper library: `pip install openai-whisper`
- ⚠️ First run downloads ~140MB model

**Installation:**
```bash
pip install openai-whisper
```

**Note:** Whisper runs locally (no API key needed)

### 3. Video Analysis
**Requirements:**
- ✅ MoviePy library: `pip install moviepy`
- ✅ `GOOGLE_API_KEY` for visual analysis
- ✅ Whisper for audio transcription (optional)

**Installation:**
```bash
pip install moviepy
pip install openai-whisper  # Optional, for transcription
```

---

## Sample Test Files

### Create Test Files

Create these files in your project directory for local testing:

1. **test_image.jpg** - Any JPEG image
2. **test_audio.mp3** - Any audio file (mp3, wav, m4a, etc.)
3. **test_video.mp4** - Any video file (mp4, avi, mov, etc.)

### Download Sample Files

**Sample Image URLs (ready to use):**
```
https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg
https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Stop_sign_MUTCD.svg/1200px-Stop_sign_MUTCD.svg.png
```

**Sample Audio URLs:**
```
https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav
```

**Create your own video:**
- Record a short video with your phone
- Or download from: https://sample-videos.com/

---

## Example Test Prompts

### Vision Analysis Examples

```
🔍 Basic analysis:
"Analyze this image: [URL] and tell me what you see"

📝 Describe:
"Describe this image in detail: test_image.jpg"

🔢 Count objects:
"How many cars are in this image: [URL]?"

📄 Extract text:
"Extract all text from this image: test_image.jpg"

♟️ Chess position:
"Analyze the chess position in this image: chess_board.jpg"
```

### Audio Processing Examples

```
🎤 Transcribe:
"Transcribe the audio file test_audio.mp3"

🌍 With language:
"Transcribe this Spanish audio: audio_es.mp3"

🔗 From URL:
"Transcribe audio from: https://example.com/audio.mp3"

🎵 Extract from video:
"Extract audio from video test_video.mp4"
```

### Video Analysis Examples

```
🎬 Visual analysis:
"What's happening in the video test_video.mp4?"

🗣️ Transcribe audio:
"Transcribe the speech in video test_video.mp4"

🔍 Comprehensive:
"Analyze both visual and audio content of test_video.mp4"

⏱️ Specific frames:
"Analyze 10 frames from video test_video.mp4"
```

---

## Testing Checklist

Before testing, ensure:

- [ ] ✅ `GOOGLE_API_KEY` configured in `.env`
- [ ] ✅ Virtual environment activated
- [ ] ✅ All requirements installed (`pip install -r requirements.txt`)
- [ ] ✅ For audio: `pip install openai-whisper`
- [ ] ✅ For video: `pip install moviepy`
- [ ] ✅ Test files created OR sample URLs ready

---

## Quick Test Commands

### Test Everything
```bash
# Run comprehensive test
python test_multimedia.py
```

### Test Vision Only
```python
from tools.vision_analyzer import describe_image

result = describe_image.invoke({
    "image_path": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
})
print(result)
```

### Test Audio Only
```python
from tools.audio_processor import transcribe_audio

result = transcribe_audio.invoke({
    "file_path": "test_audio.mp3",
    "language": "en"
})
print(result)
```

### Test Video Only
```python
from tools.video_analyzer import analyze_video

result = analyze_video.invoke({
    "video_path": "test_video.mp4",
    "question": "What happens in this video?",
    "num_frames": 3
})
print(result)
```

---

## Expected Results

### ✅ Vision Analysis
- Should return detailed descriptions of images
- Can identify objects, colors, scenes, text
- Works with both URLs and local files
- Response time: 1-3 seconds

### ✅ Audio Processing
- Transcribes speech to text accurately
- Auto-detects language
- First run downloads ~140MB model (one-time)
- Response time: Varies by audio length

### ✅ Video Analysis
- Extracts and analyzes key frames
- Can transcribe audio track
- Combines visual + audio analysis
- Response time: Varies by video length and frames

---

## Troubleshooting

### Vision Analysis Issues

**Problem:** "GOOGLE_API_KEY not configured"
```bash
# Solution: Add to .env file
echo GOOGLE_API_KEY=your_api_key_here >> .env
```

**Problem:** "Image file not found"
```bash
# Solution: Use absolute path or verify file exists
ls test_image.jpg
```

**Problem:** 403 Forbidden on URL
```bash
# Solution: Use different image URL or download locally
wget URL -O test_image.jpg
```

### Audio Processing Issues

**Problem:** "Whisper library not installed"
```bash
# Solution: Install Whisper
pip install openai-whisper
```

**Problem:** First run is slow
```bash
# This is normal - downloads ~140MB model once
# Subsequent runs are much faster
```

**Problem:** "ffmpeg not found"
```bash
# Solution: Install ffmpeg
# Windows: Download from https://ffmpeg.org/download.html
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### Video Processing Issues

**Problem:** "MoviePy library not installed"
```bash
# Solution: Install MoviePy
pip install moviepy
```

**Problem:** Video processing is slow
```bash
# This is normal for video analysis
# Reduce num_frames parameter for faster processing
```

**Problem:** "No module named 'imageio_ffmpeg'"
```bash
# Solution: Install imageio_ffmpeg
pip install imageio-ffmpeg
```

---

## Performance Tips

1. **Vision Analysis:**
   - Use URLs when possible (faster than uploading)
   - Resize large images before analysis

2. **Audio Processing:**
   - Use shorter audio clips for testing
   - Specify language if known (faster than auto-detect)

3. **Video Analysis:**
   - Start with num_frames=3 for quick tests
   - Use num_frames=10-15 for detailed analysis
   - Long videos: Extract shorter segments first

---

## Integration with Agent

All multimedia tools are automatically available in the agent. The agent will:

1. **Select the right tool** based on your question
2. **Handle file paths** and URLs automatically
3. **Combine multiple tools** when needed
4. **Provide formatted results** in natural language

**Example Agent Flow:**
```
User: "What's in this image and what does the text say?"

Agent thinks:
1. Use describe_image for general content
2. Use extract_text_from_image for text
3. Combine results into comprehensive answer
```

---

## Summary

### ✅ Ready to Use (No extra setup):
- Vision analysis with images and URLs

### ⚙️ Requires Installation:
- Audio: `pip install openai-whisper`
- Video: `pip install moviepy`

### 🎯 Best Testing Approach:
1. Start with `test_multimedia.py` for automated tests
2. Use interactive agent (`main.py`) for real queries
3. Test with sample URLs first, then local files

### 📊 40 Tools Total:
- 5 Vision tools ✅
- 3 Audio tools ✅
- 3 Video tools ✅
- 29 other tools (web search, code, database, etc.) ✅

All tools work seamlessly within the agent! 🚀
