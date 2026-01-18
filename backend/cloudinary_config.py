import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configure Cloudinary
def configure_cloudinary():
    cloudinary.config(
        cloud_name = "dillobvw3",  # Replace with yours
        api_key = "611239543672646",        # Replace with yours
        api_secret = "qup0tpwtmGtdlT65Gc1Ws5qrWyU"   # Replace with yours
    )

def upload_file_to_cloudinary(file_path, folder="deepfake-uploads"):
    """Upload file to Cloudinary"""
    try:
        configure_cloudinary()
        
        # Upload
        result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type="auto"  # Automatically detects image/video
        )
        
        return result['secure_url']  # Returns HTTPS URL
    
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None

def delete_file_from_cloudinary(public_id):
    """Delete file from Cloudinary"""
    try:
        configure_cloudinary()
        result = cloudinary.uploader.destroy(public_id)
        return result['result'] == 'ok'
    
    except Exception as e:
        print(f"Error deleting from Cloudinary: {e}")
        return False

def get_file_info(public_id):
    """Get file information"""
    try:
        configure_cloudinary()
        result = cloudinary.api.resource(public_id)
        return result
    
    except Exception as e:
        print(f"Error getting file info: {e}")
        return None



