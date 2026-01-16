from fastapi import FastAPI

# Create FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Deepfake Detector API!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "deepfake-detector-api",
        "version": "1.0.0"
    }

# Test endpoint
@app.get("/test")
def test_endpoint():
    return {
        "message": "API is working!",
        "team": "Team Pikachu"
    }