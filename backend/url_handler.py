import requests
from PIL import Image
from io import BytesIO
import os

def download_image_from_url(url, save_path='temp/url_image.jpg'):
    """Download image from URL"""
    
    try:
        print(f"🔗 Downloading image from URL...")
        
        # Set headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Download
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, f"Failed to download: Status {response.status_code}"
        
        # Check if it's an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            return None, "URL does not point to an image"
        
        # Save image
        image = Image.open(BytesIO(response.content))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save
        image.save(save_path)
        
        print(f"✅ Image downloaded successfully!")
        return save_path, None
    
    except requests.exceptions.Timeout:
        return None, "Request timeout - URL took too long to respond"
    
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    
    except Exception as e:
        return None, f"Error: {str(e)}"

def validate_url(url):
    """Check if URL is valid"""
    
    if not url:
        return False, "No URL provided"
    
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    
    # Check if URL ends with image extension
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    has_extension = any(url.lower().endswith(ext) for ext in image_extensions)
    
    # It's okay if it doesn't have extension, we'll check content-type
    
    return True, "Valid URL"