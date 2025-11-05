"""Video analysis tools combining frame extraction and vision analysis."""
import os
import tempfile
from typing import Optional
from langchain_core.tools import tool


def download_video_from_url(url: str) -> str:
    """
    Download video from URL (supports YouTube, direct URLs, etc).
    
    Args:
        url: URL of the video
    
    Returns:
        Path to the downloaded video file
    """
    import requests
    
    # Check if it's a YouTube URL
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            import yt_dlp
            
            # Create temp file path
            temp_dir = tempfile.gettempdir()
            output_template = os.path.join(temp_dir, f'yt_video_{os.getpid()}.%(ext)s')
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'worst[ext=mp4]/worst',  # Use worst quality for faster download
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',  # Force mp4 output
            }
            
            print(f"Downloading YouTube video from: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
            
            if not os.path.exists(downloaded_file):
                return f"Error: Downloaded file not found at {downloaded_file}"
            
            return downloaded_file
            
        except ImportError:
            return "Error: yt-dlp not installed. Install it with: pip install yt-dlp"
        except Exception as e:
            return f"Error downloading YouTube video: {str(e)}"
    
    else:
        # Handle regular URLs
        try:
            print(f"Downloading video from: {url}")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video.write(response.content)
            temp_video.close()
            
            return temp_video.name
            
        except Exception as e:
            return f"Error downloading video: {str(e)}"


@tool
def analyze_video(video_path: str, question: str, num_frames: int = 5) -> str:
    """
    Analyze a video by extracting frames and analyzing them with vision AI.
    Supports local files, YouTube URLs, and direct video URLs.
    
    Args:
        video_path: Path to the video file, YouTube URL, or direct video URL
        question: Question to ask about the video
        num_frames: Number of frames to extract and analyze (default: 5)
    
    Returns:
        Analysis of the video based on the extracted frames
    """
    try:
        from moviepy.editor import VideoFileClip
        from tools.vision_analyzer import analyze_image
        
        # Handle URL download
        temp_video = None
        if video_path.startswith(('http://', 'https://')):
            downloaded_path = download_video_from_url(video_path)
            if downloaded_path.startswith("Error"):
                return downloaded_path
            temp_video = downloaded_path
            video_path = temp_video
        
        # Verify file exists
        if not os.path.exists(video_path):
            return f"Error: Video file not found: {video_path}"
        
        print(f"Loading video: {video_path}")
        video = VideoFileClip(video_path)
        duration = video.duration
        
        # Calculate frame extraction times (evenly spaced)
        frame_times = [duration * i / (num_frames + 1) for i in range(1, num_frames + 1)]
        
        # Extract frames and analyze
        frame_analyses = []
        temp_frames = []
        
        try:
            for i, time in enumerate(frame_times, 1):
                # Extract frame
                frame = video.get_frame(time)
                
                # Save frame to temp file
                from PIL import Image
                frame_image = Image.fromarray(frame)
                temp_frame = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                frame_image.save(temp_frame.name)
                temp_frames.append(temp_frame.name)
                
                print(f"Analyzing frame {i}/{num_frames} at {time:.2f}s...")
                
                # Analyze frame
                analysis = analyze_image.invoke({
                    "image_path": temp_frame.name,
                    "question": f"{question} (Frame at {time:.2f}s)"
                })
                
                frame_analyses.append(f"Frame {i} ({time:.2f}s): {analysis}")
            
            video.close()
            
            # Combine analyses
            result = f"Video Analysis ({num_frames} frames analyzed):\n\n"
            result += "\n\n".join(frame_analyses)
            
            return result
            
        finally:
            # Clean up temp frames
            for temp_frame in temp_frames:
                if os.path.exists(temp_frame):
                    os.unlink(temp_frame)
            
            # Clean up temp video
            if temp_video and os.path.exists(temp_video):
                os.unlink(temp_video)
        
    except ImportError as e:
        return f"Error: Missing library: {str(e)}"
    except Exception as e:
        return f"Error analyzing video: {str(e)}"


@tool
def transcribe_video(video_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe the audio from a video file.
    Supports local files, YouTube URLs, and direct video URLs.
    
    Args:
        video_path: Path to the video file, YouTube URL, or direct video URL
        language: Optional language code for transcription
    
    Returns:
        Transcribed text from the video's audio
    """
    try:
        from tools.audio_processor import extract_audio_from_video, transcribe_audio
        
        # Handle URL download
        temp_video = None
        if video_path.startswith(('http://', 'https://')):
            downloaded_path = download_video_from_url(video_path)
            if downloaded_path.startswith("Error"):
                return downloaded_path
            temp_video = downloaded_path
            video_path = temp_video
        
        # Extract audio
        audio_result = extract_audio_from_video.invoke({"video_path": video_path})
        
        if "Error" in audio_result:
            return audio_result
        
        # Get audio file path from result
        audio_path = audio_result.split(": ")[-1]
        
        try:
            # Transcribe audio
            transcription = transcribe_audio.invoke({
                "file_path": audio_path,
                "language": language
            })
            
            return transcription
            
        finally:
            # Clean up temp audio file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            
            # Clean up temp video
            if temp_video and os.path.exists(temp_video):
                os.unlink(temp_video)
        
    except Exception as e:
        return f"Error transcribing video: {str(e)}"


@tool
def analyze_video_comprehensive(video_path: str, question: str, include_audio: bool = True) -> str:
    """
    Comprehensive video analysis including both visual and audio content.
    Supports local files, YouTube URLs, and direct video URLs.
    
    Args:
        video_path: Path to the video file, YouTube URL, or direct video URL
        question: Question to ask about the video
        include_audio: Whether to include audio transcription (default: True)
    
    Returns:
        Combined analysis of video frames and audio transcription
    """
    results = []
    
    # Analyze visual content
    print("Analyzing visual content...")
    visual_analysis = analyze_video.invoke({
        "video_path": video_path,
        "question": question,
        "num_frames": 5
    })
    results.append("=== VISUAL ANALYSIS ===")
    results.append(visual_analysis)
    
    # Transcribe audio if requested
    if include_audio:
        print("Transcribing audio...")
        audio_transcription = transcribe_video.invoke({
            "video_path": video_path
        })
        results.append("\n=== AUDIO TRANSCRIPTION ===")
        results.append(audio_transcription)
    
    return "\n".join(results)
