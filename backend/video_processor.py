import cv2
import os
from PIL import Image

def extract_frames_from_video(video_path, output_folder='temp/frames', max_frames=30):
    """
    Extract frames from video
    
    Args:
        video_path: Path to video file
        output_folder: Where to save frames
        max_frames: Maximum number of frames to extract
    
    Returns:
        List of frame paths
    """
    
    # Create output folder if doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open video
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print("❌ Error: Could not open video")
        return []
    
    # Get video info
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    print(f"📹 Video Info:")
    print(f"   Total Frames: {total_frames}")
    print(f"   FPS: {fps}")
    
    # Calculate frame interval (to get max_frames evenly distributed)
    if total_frames <= max_frames:
        frame_interval = 1
        frames_to_extract = total_frames
    else:
        frame_interval = total_frames // max_frames
        frames_to_extract = max_frames
    
    frame_paths = []
    frame_count = 0
    extracted_count = 0
    
    print(f"⏳ Extracting {frames_to_extract} frames...")
    
    while True:
        success, frame = video.read()
        
        if not success:
            break
        
        # Extract frame at intervals
        if frame_count % frame_interval == 0 and extracted_count < max_frames:
            frame_filename = f"frame_{extracted_count:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            
            # Save frame
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            
            extracted_count += 1
            print(f"   Extracted frame {extracted_count}/{frames_to_extract}")
        
        frame_count += 1
    
    video.release()
    
    print(f"✅ Extracted {len(frame_paths)} frames successfully!")
    return frame_paths

def get_video_info(video_path):
    """Get video metadata"""
    
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        return None
    
    info = {
        'total_frames': int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': int(video.get(cv2.CAP_PROP_FPS)),
        'width': int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'duration_seconds': int(video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS))
    }
    
    video.release()
    return info

def cleanup_frames(folder='temp/frames'):
    """Delete all extracted frames"""
    
    if not os.path.exists(folder):
        return
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
    
    print("✅ Cleaned up extracted frames")