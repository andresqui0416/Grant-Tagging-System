import React, { useState } from 'react';
import axios from 'axios';

// API base URL - use Vercel backend for production
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://grant-tagging-system-backend.vercel.app'
  : '';

const GrantEntry = ({ onGrantsAdded, availableTags }) => {
  const [formData, setFormData] = useState({
    grant_name: '',
    grant_description: ''
  });
  const [jsonInput, setJsonInput] = useState('');
  const [useJsonInput, setUseJsonInput] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleJsonInputChange = (e) => {
    setJsonInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      let grantsToSubmit = [];

      if (useJsonInput) {
        // Parse JSON input
        try {
          const parsed = JSON.parse(jsonInput);
          grantsToSubmit = Array.isArray(parsed) ? parsed : [parsed];
        } catch (parseError) {
          setMessage('Invalid JSON format. Please check your input.');
          setLoading(false);
          return;
        }
      } else {
        // Use form data
        if (!formData.grant_name.trim() || !formData.grant_description.trim()) {
          setMessage('Please fill in both grant name and description.');
          setLoading(false);
          return;
        }
        grantsToSubmit = [formData];
      }

      // Submit to backend
      const response = await axios.post(`${API_BASE_URL}/api/grants`, grantsToSubmit);
      
      if (response.data.success) {
        setMessage(`Successfully added ${response.data.grants_added.length} grant(s) with automatic tagging!`);
        
        // Reset form
        setFormData({ grant_name: '', grant_description: '' });
        setJsonInput('');
        
        // Notify parent component
        onGrantsAdded(response.data.grants_added);
      } else {
        setMessage('Error: ' + (response.data.error || 'Failed to add grants'));
      }
    } catch (error) {
      setMessage('Error: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const loadSampleData = () => {
    const sampleData = [
      {
        "grant_name": "Sustainable Agriculture Research Grant",
        "grant_description": "Funding for projects that promote organic farming practices and soil conservation."
      },
      {
        "grant_name": "STEM Education Initiative",
        "grant_description": "Support for programs that encourage high school students to pursue careers in science, technology, engineering, and mathematics."
      }
    ];
    setJsonInput(JSON.stringify(sampleData, null, 2));
    setUseJsonInput(true);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Add New Grants</h2>
        <p className="text-gray-600">Enter grant information manually or upload JSON data. The system will automatically assign relevant tags.</p>
      </div>

      <div className="flex gap-8 mb-8 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="inputMethod"
            checked={!useJsonInput}
            onChange={() => setUseJsonInput(false)}
            className="text-primary-600 focus:ring-primary-500"
          />
          <span className="font-medium text-gray-700">Manual Entry</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="inputMethod"
            checked={useJsonInput}
            onChange={() => setUseJsonInput(true)}
            className="text-primary-600 focus:ring-primary-500"
          />
          <span className="font-medium text-gray-700">JSON Input</span>
        </label>
      </div>

      {!useJsonInput ? (
        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="mb-6">
            <label htmlFor="grant_name" className="block mb-2 font-medium text-gray-700">Grant Name *</label>
            <input
              type="text"
              id="grant_name"
              name="grant_name"
              value={formData.grant_name}
              onChange={handleInputChange}
              placeholder="Enter grant name"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>

          <div className="mb-6">
            <label htmlFor="grant_description" className="block mb-2 font-medium text-gray-700">Grant Description *</label>
            <textarea
              id="grant_description"
              name="grant_description"
              value={formData.grant_description}
              onChange={handleInputChange}
              placeholder="Enter detailed grant description"
              rows="4"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-vertical min-h-[100px]"
            />
          </div>

          <button 
            type="submit" 
            className="w-full bg-gradient-to-r from-primary-500 to-primary-600 text-white py-3 px-6 rounded-md font-medium hover:from-primary-600 hover:to-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200"
            disabled={loading}
          >
            {loading ? 'Adding Grant...' : 'Add Grant'}
          </button>
        </form>
      ) : (
        <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-gray-900">JSON Input</h3>
            <button 
              type="button" 
              onClick={loadSampleData} 
              className="bg-gray-100 text-primary-600 border border-primary-600 px-4 py-2 rounded-md hover:bg-primary-600 hover:text-white transition-colors duration-200 text-sm font-medium"
            >
              Load Sample Data
            </button>
          </div>
          
          <textarea
            value={jsonInput}
            onChange={handleJsonInputChange}
            placeholder="Paste your JSON data here..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 font-mono text-sm resize-vertical min-h-[200px]"
            rows="10"
          />
          
          <button 
            onClick={handleSubmit} 
            className="w-full bg-gradient-to-r from-primary-500 to-primary-600 text-white py-3 px-6 rounded-md font-medium hover:from-primary-600 hover:to-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200 mt-4"
            disabled={loading || !jsonInput.trim()}
          >
            {loading ? 'Processing...' : 'Process JSON Data'}
          </button>
        </div>
      )}

      {message && (
        <div className={`p-4 rounded-lg mb-4 font-medium ${
          message.includes('Error') 
            ? 'bg-red-50 text-red-700 border border-red-200' 
            : 'bg-green-50 text-green-700 border border-green-200'
        }`}>
          {message}
        </div>
      )}

      <div className="bg-primary-50 p-6 rounded-lg border border-primary-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Automatic Tagging</h3>
        <p className="text-gray-600 mb-4">The system will automatically assign relevant tags from our predefined list:</p>
        <div className="flex flex-wrap gap-2">
          {availableTags.slice(0, 10).map(tag => (
            <span key={tag} className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-medium">
              {tag}
            </span>
          ))}
          {availableTags.length > 10 && (
            <span className="bg-gray-500 text-white px-3 py-1 rounded-full text-sm font-medium">
              +{availableTags.length - 10} more
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default GrantEntry;
