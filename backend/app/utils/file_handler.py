import os
from fastapi import UploadFile, HTTPException

# Configuration
UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename
    Example: 'image.jpg' returns '.jpg'
    """
    return os.path.splitext(filename)[1].lower()


def is_allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed
    Returns True if file is an allowed image or video
    """
    ext = get_file_extension(filename)
    return ext in ALLOWED_IMAGE_EXTENSIONS or ext in ALLOWED_VIDEO_EXTENSIONS


def is_image(filename: str) -> bool:
    """Check if file is an image"""
    ext = get_file_extension(filename)
    return ext in ALLOWED_IMAGE_EXTENSIONS


def is_video(filename: str) -> bool:
    """Check if file is a video"""
    ext = get_file_extension(filename)
    return ext in ALLOWED_VIDEO_EXTENSIONS


def validate_file(file: UploadFile) -> dict:
    """
    Validate uploaded file
    Returns dict with file info if valid
    Raises HTTPException if invalid
    """
    # Check if filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Check file extension
    if not is_allowed_file(file.filename):
        allowed = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed)}"
        )
    
    # Determine file type
    file_type = "image" if is_image(file.filename) else "video"
    
    return {
        "filename": file.filename,
        "extension": get_file_extension(file.filename),
        "type": file_type
    }


def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)


def validate_file_size(file_path: str) -> bool:
    """
    Check if file size is within limits
    Returns True if valid, raises HTTPException if too large
    """
    file_size = get_file_size(file_path)
    
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.2f}MB). Maximum size: {max_mb}MB"
        )
    
    return True