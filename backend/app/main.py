from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload

# Create FastAPI app
app = FastAPI(
    title="Deepfake Detector API",
    description="API for detecting deepfakes in images and videos",
    version="1.0.0"
)

# Configure CORS (so frontend can call your API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5001"],  # React default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Deepfake Detector API!",
        "team": "Team Pikachu",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "deepfake-detector-api"
    }