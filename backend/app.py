from cloudinary_config import upload_file_to_cloudinary
import os
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