import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test if API is running"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())
    assert response.status_code == 200

def test_upload_file():
    """Test single file upload"""
    # Create a test file (you can replace with real image path)
    test_file_path = "test_image.jpg"
    
    with open(test_file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    print("Upload Test:", response.json())
    assert response.status_code == 200

def test_list_files():
    """Test listing uploaded files"""
    response = requests.get(f"{BASE_URL}/api/upload")
    print("List Files:", response.json())
    assert response.status_code == 200

if __name__ == "__main__":
    print("Running tests...\n")
    
    try:
        test_health_check()
        print("✓ Health check passed\n")
        
        test_list_files()
        print("✓ List files passed\n")
        
        print("All tests passed! ✓")
    except Exception as e:
        print(f"Test failed: {e}")