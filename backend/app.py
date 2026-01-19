from flask import app, jsonify
from urllib3 import request
from cloudinary_config import upload_file_to_cloudinary
import os
from video_processor import extract_frames_from_video, get_video_info, cleanup_frames
from file_validator import is_video
from url_handler import download_image_from_url, validate_url
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from request_logger import log_request
import time


@app.route('/api/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Validate file
    is_valid, message = validate_file(file)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    try:
        # Save file temporarily
        temp_path = os.path.join('temp', file.filename)
        file.save(temp_path)
        
        # Upload to Cloudinary
        cloudinary_url = upload_file_to_cloudinary(temp_path, folder='deepfake-uploads')
        
        if cloudinary_url:
            print(f"✅ File uploaded to Cloudinary: {cloudinary_url}")
        
        # Run ML prediction (your existing code)
        # prediction = model.predict(temp_path)
        
        # Delete local temp file
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'file_url': cloudinary_url,
            'prediction': 'Real',  # Replace with actual prediction
            'confidence': 85.5
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    @app.route('/api/analyze-video', methods=['POST'])
    def analyze_video():
       """Analyze video frame by frame"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Validate
    is_valid, message = validate_file(file)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    # Check if it's a video
    if not is_video(file.filename):
        return jsonify({'error': 'Please upload a video file'}), 400
    
    try:
        # Save video temporarily
        temp_video_path = os.path.join('temp', file.filename)
        file.save(temp_video_path)
        
        print(f"📹 Processing video: {file.filename}")
        
        # Get video info
        video_info = get_video_info(temp_video_path)
        
        # Extract frames
        frames = extract_frames_from_video(temp_video_path, max_frames=20)
        
        # Analyze each frame (you'll integrate with ML model later)
        frame_results = []
        
        for i, frame_path in enumerate(frames):
            # TODO: Replace with actual ML prediction
            # prediction = model.predict(frame_path)
            
            frame_results.append({
                'frame_number': i + 1,
                'prediction': 'Real',  # Placeholder
                'confidence': 85.5 + (i % 10)  # Placeholder
            })
        
        # Calculate overall result
        avg_confidence = sum([r['confidence'] for r in frame_results]) / len(frame_results)
        
        # Upload to Cloudinary (optional)
        cloudinary_url = None
        if 'cloudinary_config' in dir():
            cloudinary_url = upload_file_to_cloudinary(temp_video_path, folder='deepfake-videos')
        
        # Cleanup
        os.remove(temp_video_path)
        cleanup_frames()
        
        return jsonify({
            'success': True,
            'video_info': video_info,
            'frames_analyzed': len(frames),
            'frame_results': frame_results,
            'overall_prediction': 'Real' if avg_confidence > 50 else 'Fake',
            'overall_confidence': round(avg_confidence, 2),
            'video_url': cloudinary_url
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500
    @app.route('/api/analyze-url', methods=['POST'])
    def analyze_url():
        """Analyze image from URL"""
    
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = data['url']
    
    # Validate URL
    is_valid, message = validate_url(url)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    try:
        # Download image
        image_path, error = download_image_from_url(url)
        
        if error:
            return jsonify({'error': error}), 400
        
        print(f"🔍 Analyzing image from URL: {url}")
        
        # Analyze image (TODO: integrate with ML model)
        # prediction = model.predict(image_path)
        
        # Upload to Cloudinary (optional)
        cloudinary_url = None
        if 'cloudinary_config' in dir():
            cloudinary_url = upload_file_to_cloudinary(image_path, folder='deepfake-url-images')
        
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
        
        return jsonify({
            'success': True,
            'source_url': url,
            'prediction': 'Real',  # Placeholder
            'confidence': 87.5,  # Placeholder
            'analyzed_image_url': cloudinary_url
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500
    app = Flask(__name__)
    CORS(app)

# Add rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Use IP address as key
    default_limits=["100 per day", "20 per hour"],  # Default limits
    storage_uri="memory://"  # Store in memory
)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")  # Max 10 uploads per minute
def predict():
    # Your existing code...
    pass

@app.route('/api/analyze-video', methods=['POST'])
@limiter.limit("5 per minute")  # Videos take longer, so limit to 5
def analyze_video():
    # Your existing code...
    pass

@app.route('/api/analyze-url', methods=['POST'])
@limiter.limit("15 per minute")  # URLs are faster
def analyze_url():
    # Your existing code...
    pass

@app.route('/api/health', methods=['GET'])
@limiter.exempt  # No limit on health check
def health():
    return jsonify({'status': 'healthy'})
    @app.errorhandler(429)
    def ratelimit_handler(e):
       """Handle rate limit exceeded"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.',
        'retry_after': e.description
    }), 429
    @app.before_request
    def before_request():
       """Log request start time"""
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """Log request details after processing"""
    
    # Calculate response time
    if hasattr(request, 'start_time'):
        response_time = (time.time() - request.start_time) * 1000  # Convert to ms
    else:
        response_time = None
    
    # Log the request
    log_request(
        endpoint=request.path,
        method=request.method,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', 'Unknown'),
        status_code=response.status_code,
        response_time=response_time
    )
    
    return response  
    @app.route('/api/stats', methods=['GET'])
    @limiter.exempt
    def stats():
       """Get API statistics"""
    
    stats = get_request_stats()
    
    return jsonify({
        'success': True,
        'statistics': stats
    })