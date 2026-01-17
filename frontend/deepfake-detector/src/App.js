import { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
     setError(null); 
     console.log("File selected:", e.target.files[0]);
  };

  const handleUpload = async () => {
    setUploadProgress(0);
    setIsLoading(true);
     setError(null); 
    
    if (!selectedFile) {
      setError("Please select a file first!"); 
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      console.log("Sending file to backend...");
      
      const response = await axios.post(
        'http://localhost:5000/api/predict',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            const percent = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percent);
            console.log("Upload progress:", percent + "%");
          }
        }
      );

      console.log("Success! Backend returned:", response.data);
      alert("Result: " + JSON.stringify(response.data));
      
      setUploadProgress(100);
      setTimeout(() => setUploadProgress(0), 2000);

    } catch (error) {
      console.error("Error uploading file:", error);
      setUploadProgress(0);
      
      if (error.response) {
      // Backend responded with an error (4xx, 5xx)
      const message = error.response.data?.message || error.response.data?.error || 'Server error occurred';
      setError(`Backend Error: ${message}`);
    } else if (error.request) {
      // Request was made but no response received
      setError('Cannot reach the server. Is the backend running on localhost:5000?');
    } else {
      // Something else went wrong
      setError(`Error: ${error.message}`);
    }
  } finally {
    setIsLoading(false);
  }
};

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
        <h1 className="text-3xl font-bold">Deepfake Detector</h1>
        <p className="text-blue-100">Upload an image or video to analyze</p>
      </header>

      {/* Upload Area */}
      <div className="max-w-2xl mx-auto p-8">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center bg-white">
          <input 
            type="file" 
            accept="image/*,video/*"
            onChange={handleFileChange}
            className="mb-4"
          />
          
          {selectedFile && (
            <p className="text-gray-700 mb-4">Selected: {selectedFile.name}</p>
          )}
          
          <button 
            onClick={handleUpload}
            disabled={isLoading}
            className={`px-6 py-2 rounded-lg transition-colors text-white font-medium ${
              isLoading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {isLoading ? 'Analyzing...' : 'Analyze File'}
          </button>

          {/* Progress bar */}
          {uploadProgress > 0 && uploadProgress < 100 && (
            <div className="mt-4">
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  className="bg-blue-500 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <p className="text-sm text-gray-600 mt-2 text-center">
                Uploading: {uploadProgress}%
              </p>
            </div>
          )}

          {/* Loading spinner */}
          {isLoading && (
            <div className="flex flex-col items-center mt-6">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
              <p className="text-gray-600 mt-3 font-medium">Analyzing your file...</p>
            </div>
          )}
          {error && (
  <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded">
    <div className="flex items-start">
      <div className="flex-shrink-0">
        <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="ml-3">
        <h3 className="text-sm font-medium text-red-800">Error</h3>
        <p className="text-sm text-red-700 mt-1">{error}</p>
      </div>
      <button 
        onClick={() => setError(null)}
        className="ml-auto flex-shrink-0 text-red-400 hover:text-red-600"
      >
        <span className="text-xl">&times;</span>
      </button>
    </div>
  </div>
)}

        </div>

        {/* Results Section */}
        <div className="mt-8 p-6 bg-white rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Results</h2>
          <p className="text-gray-500">Upload a file to see results here</p>
        </div>
      </div>
    </div>
  );
}

export default App;