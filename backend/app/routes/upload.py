from app.utils.logger import logger
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import time
from app.utils.file_handler import (
    validate_file, 
    validate_file_size,
    UPLOAD_DIR,
    TEMP_DIR
)

# Create router
router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single image or video file"""
    
    logger.info(f"Received upload request for file: {file.filename}")
    
    try:
        # Validate file
        file_info = validate_file(file)
        logger.info(f"File validated: {file_info}")
        
        # ... rest of your code ...
        
        logger.info(f"File uploaded successfully: {filename}")
        
        return JSONResponse({...})
        
    except HTTPException as e:
        logger.error(f"Validation error: {str(e)}")
        raise e
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        # ... rest of error handling ...

@router.post("/upload/temp")
async def upload_temp_file(file: UploadFile = File(...)):
    """
    Upload file to temporary directory
    Useful for files that will be processed and deleted
    
    Args:
        file: Image or video file
        
    Returns:
        JSON with temporary file path
    """
    try:
        # Validate file
        file_info = validate_file(file)
        
        # Create unique filename
        timestamp = int(time.time())
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(TEMP_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validate size
        validate_file_size(file_path)
        
        return JSONResponse({
            "success": True,
            "message": "File uploaded to temporary storage",
            "data": {
                "file_path": file_path,
                "file_type": file_info["type"]
            }
        })
        
    except HTTPException as e:
        raise e
        
    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.delete("/upload/{filename}")
async def delete_file(filename: str):
    """
    Delete an uploaded file
    
    Args:
        filename: Name of file to delete
        
    Returns:
        Success/failure message
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        os.remove(file_path)
        
        return JSONResponse({
            "success": True,
            "message": f"File {filename} deleted successfully"
        })
        
    except HTTPException as e:
        raise e
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )
@router.post("/upload/batch")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    """
    Upload multiple files at once
    
    Args:
        files: List of image/video files
        
    Returns:
        JSON with results for each file
    """
    results = []
    successful_uploads = 0
    failed_uploads = 0
    
    for file in files:
        try:
            # Validate file
            file_info = validate_file(file)
            
            # Create unique filename
            timestamp = int(time.time())
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Validate size
            validate_file_size(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            
            results.append({
                "success": True,
                "original_filename": file.filename,
                "saved_filename": filename,
                "file_type": file_info["type"],
                "file_size_mb": round(file_size, 2)
            })
            
            successful_uploads += 1
            
        except Exception as e:
            results.append({
                "success": False,
                "original_filename": file.filename,
                "error": str(e)
            })
            
            failed_uploads += 1
            
            # Clean up if file was saved
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
    
    return JSONResponse({
        "success": True,
        "message": f"Processed {len(files)} files",
        "summary": {
            "total": len(files),
            "successful": successful_uploads,
            "failed": failed_uploads
        },
        "results": results
    })
@router.get("/upload/{filename}")
async def get_file_info(filename: str):
    """
    Get information about an uploaded file
    
    Args:
        filename: Name of the file
        
    Returns:
        File information (size, type, etc.)
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get file stats
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size / (1024 * 1024)  # Convert to MB
        
        # Determine file type
        from app.utils.file_handler import is_image, is_video
        if is_image(filename):
            file_type = "image"
        elif is_video(filename):
            file_type = "video"
        else:
            file_type = "unknown"
        
        return JSONResponse({
            "success": True,
            "data": {
                "filename": filename,
                "file_path": file_path,
                "file_type": file_type,
                "file_size_mb": round(file_size, 2),
                "created_at": file_stats.st_ctime
            }
        })
        
    except HTTPException as e:
        raise e
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.get("/upload")
async def list_uploaded_files():
    """
    List all uploaded files
    
    Returns:
        List of uploaded files with their info
    """
    try:
        files = []
        
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                    
                    files.append({
                        "filename": filename,
                        "file_size_mb": round(file_size, 2)
                    })
        
        return JSONResponse({
            "success": True,
            "total_files": len(files),
            "files": files
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )
