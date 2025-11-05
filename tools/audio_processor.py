"""Audio processing tools for transcription and analysis."""
import os
import tempfile
from typing import Optional
from langchain_core.tools import tool


@tool
def transcribe_audio(file_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe audio file to text using OpenAI Whisper.
    
    Args:
        file_path: Path to the audio file (mp3, wav, m4a, etc.)
        language: Optional language code (e.g., 'en', 'es'). Auto-detected if not provided.
    
    Returns:
        Transcribed text from the audio file
    """
    try:
        import whisper
        
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: Audio file not found: {file_path}"
        
        # Configure ffmpeg path from imageio_ffmpeg (bundled with MoviePy)
        try:
            from imageio_ffmpeg import get_ffmpeg_exe
            ffmpeg_path = get_ffmpeg_exe()
            # Monkey patch whisper's ffmpeg command
            import whisper.audio
            original_load = whisper.audio.load_audio
            
            def load_audio_with_ffmpeg(file: str, sr: int = 16000):
                import subprocess
                import numpy as np
                cmd = [
                    ffmpeg_path,
                    "-nostdin",
                    "-threads", "0",
                    "-i", file,
                    "-f", "s16le",
                    "-ac", "1",
                    "-acodec", "pcm_s16le",
                    "-ar", str(sr),
                    "-"
                ]
                out = subprocess.run(cmd, capture_output=True, check=True).stdout
                return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
            
            whisper.audio.load_audio = load_audio_with_ffmpeg
        except ImportError:
            pass  # Fall back to default behavior
        
        # Load the Whisper model (base model for balance of speed and accuracy)
        print(f"Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Transcribe the audio
        print(f"Transcribing audio from: {file_path}")
        result = model.transcribe(
            file_path,
            language=language,
            verbose=False,
            fp16=False  # Disable fp16 for better CPU compatibility
        )
        
        transcription = result["text"].strip()
        detected_language = result.get("language", "unknown")
        
        return f"Transcription (language: {detected_language}):\n\n{transcription}"
        
    except ImportError:
        return "Error: Whisper library not installed. Run: pip install openai-whisper"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error transcribing audio: {str(e)}\n\nDetails:\n{error_details}"


@tool
def transcribe_audio_from_url(url: str, language: Optional[str] = None) -> str:
    """
    Download and transcribe audio from a URL.
    
    Args:
        url: URL of the audio file
        language: Optional language code (e.g., 'en', 'es')
    
    Returns:
        Transcribed text from the audio
    """
    try:
        import requests
        
        # Download the audio file
        print(f"Downloading audio from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name
        
        try:
            # Transcribe the downloaded file
            result = transcribe_audio.invoke({
                "file_path": tmp_path,
                "language": language
            })
            return result
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except requests.exceptions.RequestException as e:
        return f"Error downloading audio from {url}: {str(e)}"
    except Exception as e:
        return f"Error processing audio from URL: {str(e)}"


@tool
def extract_audio_from_video(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract audio track from a video file.
    
    Args:
        video_path: Path to the video file
        output_path: Optional path for the output audio file. If not provided, uses temp file.
    
    Returns:
        Path to the extracted audio file
    """
    try:
        from moviepy.editor import VideoFileClip
        
        if not os.path.exists(video_path):
            return f"Error: Video file not found: {video_path}"
        
        # Generate output path if not provided
        if not output_path:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            output_path = temp_file.name
            temp_file.close()
        
        print(f"Extracting audio from: {video_path}")
        
        # Load video and extract audio
        video = VideoFileClip(video_path)
        
        if video.audio is None:
            video.close()
            return f"Error: No audio track found in video: {video_path}"
        
        video.audio.write_audiofile(output_path, verbose=False, logger=None)
        video.close()
        
        return f"Audio extracted successfully to: {output_path}"
        
    except ImportError:
        return "Error: moviepy library not installed. Run: pip install moviepy"
    except Exception as e:
        return f"Error extracting audio from video: {str(e)}"
