"""
Simple multimedia demo - Create and test with local files

This script:
1. Creates a simple test image with text
2. Demonstrates vision analysis tools
3. Shows how to use the tools programmatically
"""

import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load environment variables
load_dotenv()

def create_test_image():
    """Create a simple test image with text and shapes."""
    print("Creating test image...")
    
    # Create a new image with white background
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw some shapes
    # Blue rectangle
    draw.rectangle([50, 50, 300, 200], fill='blue', outline='black', width=3)
    
    # Red circle
    draw.ellipse([450, 50, 700, 300], fill='red', outline='black', width=3)
    
    # Green triangle (polygon)
    draw.polygon([(150, 350), (400, 350), (275, 500)], fill='green', outline='black')
    
    # Add text
    try:
        # Try to use a nice font
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    draw.text((200, 250), "HELLO WORLD", fill='black', font=font)
    draw.text((50, 520), "Test Image - 3 Shapes", fill='black')
    
    # Save the image
    filename = "test_image.jpg"
    image.save(filename)
    print(f"✅ Created: {filename}")
    return filename


def test_vision_tools(image_path):
    """Test vision analysis tools with the created image."""
    from tools.vision_analyzer import (
        analyze_image,
        describe_image,
        count_objects_in_image,
        extract_text_from_image
    )
    
    print("\n" + "="*80)
    print("  VISION ANALYSIS DEMONSTRATIONS")
    print("="*80 + "\n")
    
    # Test 1: Describe the image
    print("Test 1: DESCRIBE IMAGE")
    print("-" * 40)
    try:
        result = describe_image.invoke({"image_path": image_path})
        print(f"📷 Result:\n{result}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    # Test 2: Answer a question about the image
    print("\nTest 2: ANALYZE IMAGE (Answer Question)")
    print("-" * 40)
    try:
        result = analyze_image.invoke({
            "image_path": image_path,
            "question": "What shapes are in this image and what colors are they?"
        })
        print(f"❓ Question: What shapes are in this image and what colors are they?")
        print(f"📷 Result:\n{result}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    # Test 3: Count objects
    print("\nTest 3: COUNT OBJECTS")
    print("-" * 40)
    try:
        result = count_objects_in_image.invoke({
            "image_path": image_path,
            "object_type": "shapes"
        })
        print(f"🔢 Counting: shapes")
        print(f"📷 Result:\n{result}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    # Test 4: Extract text
    print("\nTest 4: EXTRACT TEXT (OCR)")
    print("-" * 40)
    try:
        result = extract_text_from_image.invoke({"image_path": image_path})
        print(f"📝 Result:\n{result}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")


def show_usage_examples():
    """Show examples of using multimedia tools in the agent."""
    print("\n" + "="*80)
    print("  HOW TO USE MULTIMEDIA TOOLS IN THE AGENT")
    print("="*80 + "\n")
    
    examples = [
        {
            "category": "🖼️ VISION ANALYSIS",
            "examples": [
                "Describe this image: test_image.jpg",
                "What colors are in test_image.jpg?",
                "How many shapes are in test_image.jpg?",
                "Extract any text from test_image.jpg",
            ]
        },
        {
            "category": "🎵 AUDIO PROCESSING",
            "examples": [
                "Transcribe the audio file test_audio.mp3",
                "What language is spoken in test_audio.mp3?",
                "Extract audio from video test_video.mp4",
            ]
        },
        {
            "category": "🎬 VIDEO ANALYSIS",
            "examples": [
                "What happens in the video test_video.mp4?",
                "Transcribe the speech from test_video.mp4",
                "Analyze both visual and audio content of test_video.mp4",
            ]
        }
    ]
    
    for section in examples:
        print(f"\n{section['category']}")
        print("-" * 40)
        for i, example in enumerate(section['examples'], 1):
            print(f"{i}. {example}")
    
    print("\n" + "="*80)
    print("💡 TIP: The agent automatically selects the right tool based on your question!")
    print("="*80 + "\n")


def main():
    """Run the multimedia demonstration."""
    print("\n" + "="*80)
    print("  MULTIMEDIA TOOLS DEMONSTRATION")
    print("="*80 + "\n")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ Error: GOOGLE_API_KEY not configured in .env file")
        print("Please add your Google API key to the .env file to continue.\n")
        return
    
    print("✅ GOOGLE_API_KEY is configured")
    
    # Create test image
    image_path = create_test_image()
    
    # Test vision tools
    test_vision_tools(image_path)
    
    # Show usage examples
    show_usage_examples()
    
    print("\n" + "="*80)
    print("  NEXT STEPS")
    print("="*80 + "\n")
    
    print("1. ✅ Vision tools tested with test_image.jpg")
    print("2. 📝 See MULTIMEDIA_TESTING_GUIDE.md for full documentation")
    print("3. 🚀 Use the interactive agent (python main.py) to test with real queries")
    print("4. 🎵 Add test_audio.mp3 to test audio transcription")
    print("5. 🎬 Add test_video.mp4 to test video analysis")
    print("\n")


if __name__ == "__main__":
    main()
