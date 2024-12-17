#!python3
import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI

def describe_image(image_url):
    """
    Generate a description of an image using OpenAI's GPT-4o vision model.
    
    Args:
        image_url (str): URL of the image to describe
    
    Returns:
        str: Descriptive text about the image
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Ensure API key is available
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize OpenAI client
    client = OpenAI()
    
    try:
        # Create image description request
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail. Focus on clothing-related attributes like color, style, fit, fabric, and any distinctive features."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        
        # Extract and return the description
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error describing image: {e}", file=sys.stderr)
        return None

def main():
    """
    Command-line interface for image description
    """
    parser = argparse.ArgumentParser(description="Generate image description using OpenAI")
    parser.add_argument("image_url", help="URL of the image to describe")
    
    args = parser.parse_args()
    
    description = describe_image(args.image_url)
    
    if description:
        print(description)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()