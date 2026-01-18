from cloudinary_config import upload_file_to_cloudinary, delete_file_from_cloudinary

# Create a test file
with open('test.txt', 'w') as f:
    f.write('Testing Cloudinary!')

print("📤 Uploading to Cloudinary...")

# Upload
url = upload_file_to_cloudinary('test.txt', folder='test')

if url:
    print(f"✅ Upload successful!")
    print(f"🔗 URL: {url}")
    print("\n✅ Cloudinary is working perfectly!")
else:
    print("❌ Upload failed!")

# Clean up
import os
os.remove('test.txt')