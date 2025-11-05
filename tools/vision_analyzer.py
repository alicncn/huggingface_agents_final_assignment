"""Vision and image analysis tools using Gemini Vision."""
import os
import base64
from typing import Optional
from langchain_core.tools import tool
import requests
from PIL import Image
import io


def encode_image(image_path: str) -> str:
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def download_image(url: str) -> str:
    """Download image from URL and save to temp file."""
    import tempfile
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    # Determine file extension from content type or URL
    content_type = response.headers.get('content-type', '')
    if 'jpeg' in content_type or 'jpg' in content_type:
        suffix = '.jpg'
    elif 'png' in content_type:
        suffix = '.png'
    elif 'gif' in content_type:
        suffix = '.gif'
    else:
        suffix = '.jpg'  # default
    
    # Save to temp file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_file.write(response.content)
    tmp_file.close()
    
    return tmp_file.name


@tool
def analyze_image(image_path: str, question: str) -> str:
    """
    Analyze an image and answer a question about it using Gemini Vision.
    
    Args:
        image_path: Path to the image file or URL
        question: Question to ask about the image
    
    Returns:
        Answer to the question based on image analysis
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        # Check if API key is configured
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return "Error: GOOGLE_API_KEY not configured in .env file"
        
        # Handle URL vs local file
        temp_file = None
        if image_path.startswith(('http://', 'https://')):
            print(f"Downloading image from: {image_path}")
            image_path = download_image(image_path)
            temp_file = image_path
        
        # Verify file exists
        if not os.path.exists(image_path):
            return f"Error: Image file not found: {image_path}"
        
        try:
            # Initialize Gemini Vision model
            model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=api_key
            )
            
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create message with image
            message = HumanMessage(
                content=[
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_data}"
                    }
                ]
            )
            
            # Get response
            response = model.invoke([message])
            
            return response.content
            
        finally:
            # Clean up temp file if we downloaded one
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
        
    except ImportError as e:
        return f"Error: Missing library: {str(e)}"
    except Exception as e:
        return f"Error analyzing image: {str(e)}"


@tool
def count_objects_in_image(image_path: str, object_type: str) -> str:
    """
    Count specific objects in an image.
    
    Args:
        image_path: Path to the image file or URL
        object_type: Type of object to count (e.g., "birds", "people", "cars")
    
    Returns:
        Count and description of the objects found
    """
    question = f"Count how many {object_type} are visible in this image. Be specific and provide the exact count. If there are different types or species, list them separately."
    return analyze_image.invoke({"image_path": image_path, "question": question})


@tool
def describe_image(image_path: str) -> str:
    """
    Get a detailed description of an image.
    
    Args:
        image_path: Path to the image file or URL
    
    Returns:
        Detailed description of the image
    """
    question = "Provide a detailed description of this image. Include all relevant objects, people, text, colors, and any other notable features."
    return analyze_image.invoke({"image_path": image_path, "question": question})


@tool
def extract_text_from_image(image_path: str) -> str:
    """
    Extract any text visible in an image (OCR).
    
    Args:
        image_path: Path to the image file or URL
    
    Returns:
        Text extracted from the image
    """
    question = "Extract all text visible in this image. Include any words, numbers, signs, labels, or other readable text. If there is no text, say 'No text found'."
    return analyze_image.invoke({"image_path": image_path, "question": question})


@tool
def analyze_chess_position(image_path: str) -> str:
    """
    Analyze a chess board position from an image.
    
    Args:
        image_path: Path to the chess board image or URL
    
    Returns:
        Chess position in FEN notation and analysis
    """
    question = """Analyze this chess board image. Provide:
1. The position in FEN (Forsyth-Edwards Notation) format
2. Whose turn it is
3. Any notable features of the position
Be very precise about piece positions."""
    return analyze_image.invoke({"image_path": image_path, "question": question})
