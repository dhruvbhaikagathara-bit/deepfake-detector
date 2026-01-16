import { useState } from 'react';
import axios from 'axios'; 

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    console.log("File selected:", e.target.files[0]);
  };

  const handleUpload = async () => {
  // Step 1: Check if file is selected
  if (!selectedFile) {
    alert("Please select a file first!");
    return;
  }

  // Step 2: Create FormData (special format for sending files)
  const formData = new FormData();
  formData.append('file', selectedFile);

  // Step 3: Send to backend
  try {
    console.log("Sending file to backend...");
    
    const response = await axios.post(
      'http://localhost:5000/api/predict',  // Backend URL
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    );

    // Step 4: Show the result
    console.log("Success! Backend returned:", response.data);
    alert("Result: " + JSON.stringify(response.data));

  } catch (error) {
    // Step 5: Handle errors
    console.error("Error uploading file:", error);
    
    if (error.response) {
      // Backend responded with error
      alert("Backend error: " + error.response.data.message);
    } else if (error.request) {
      // Backend didn't respond
      alert("Cannot reach backend. Is it running on localhost:5000?");
    } else {
      // Something else went wrong
      alert("Error: " + error.message);
    }
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
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Analyze File
          </button>
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