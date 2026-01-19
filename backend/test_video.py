from video_processor import extract_frames_from_video, get_video_info, cleanup_frames

# You need a test video file
# Download any short video (5-10 seconds) and save as 'test_video.mp4' in backend folder

video_path = 'test_video.mp4'

print("🎬 Testing Video Processing...")
print("-" * 50)

# Get video info
info = get_video_info(video_path)
if info:
    print(f"📊 Video Information:")
    print(f"   Duration: {info['duration_seconds']} seconds")
    print(f"   Resolution: {info['width']}x{info['height']}")
    print(f"   FPS: {info['fps']}")
    print(f"   Total Frames: {info['total_frames']}")
    print()

# Extract frames
frames = extract_frames_from_video(video_path, max_frames=10)

print()
print(f"✅ Test complete! Extracted {len(frames)} frames")
print(f"📁 Frames saved in: temp/frames/")

# Cleanup
cleanup_frames()