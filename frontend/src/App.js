import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GrantEntry from './components/GrantEntry';
import GrantDisplay from './components/GrantDisplay';
import './App.css';

// API base URL - use Vercel backend for production
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://grant-tagging-system-backend.vercel.app'
  : '';

function App() {
  const [activeTab, setActiveTab] = useState('entry');
  const [grants, setGrants] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load grants and tags on component mount
  useEffect(() => {
    loadGrants();
    loadTags();
  }, []);

  const loadGrants = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/grants`);
      if (response.data.success) {
        setGrants(response.data.grants);
      } else {
        setError('Failed to load grants');
      }
    } catch (err) {
      setError('Error loading grants: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadTags = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/tags`);
      if (response.data.success) {
        setTags(response.data.tags);
      }
    } catch (err) {
      console.error('Error loading tags:', err);
    }
  };

  const handleGrantsAdded = (newGrants) => {
    setGrants(prevGrants => [...prevGrants, ...newGrants]);
  };

  const handleGrantSearch = async (searchTags) => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/api/grants/search`, { tags: searchTags });
      if (response.data.success) {
        setGrants(response.data.grants);
      } else {
        setError('Search failed');
      }
    } catch (err) {
      setError('Search error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClearSearch = () => {
    loadGrants();
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-gradient-to-br from-primary-500 to-primary-700 text-white py-8 px-4 text-center shadow-lg">
        <h1 className="text-4xl font-bold mb-2">Grant Tagging System</h1>
        <p className="text-lg opacity-90">Intelligent categorization and display of grants</p>
      </header>

      <nav className="flex bg-white border-b border-gray-200 shadow-sm">
        <button 
          className={`flex-1 py-4 px-8 text-base font-medium cursor-pointer transition-all duration-300 border-b-3 ${
            activeTab === 'entry' 
              ? 'text-primary-600 border-primary-600 bg-primary-50' 
              : 'text-gray-600 border-transparent hover:bg-gray-50 hover:text-gray-900'
          }`}
          onClick={() => setActiveTab('entry')}
        >
          Add Grants
        </button>
        <button 
          className={`flex-1 py-4 px-8 text-base font-medium cursor-pointer transition-all duration-300 border-b-3 ${
            activeTab === 'display' 
              ? 'text-primary-600 border-primary-600 bg-primary-50' 
              : 'text-gray-600 border-transparent hover:bg-gray-50 hover:text-gray-900'
          }`}
          onClick={() => setActiveTab('display')}
        >
          View Grants ({grants.length})
        </button>
      </nav>

      <main className="flex-1 p-8 max-w-7xl mx-auto w-full">
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-4 border border-red-200 flex justify-between items-center">
            <span>{error}</span>
            <button 
              onClick={() => setError(null)}
              className="text-red-700 hover:text-red-900 text-xl ml-4"
            >
              ×
            </button>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center py-12 text-gray-600">
            <div className="w-10 h-10 border-4 border-gray-200 border-t-primary-500 rounded-full animate-spin mb-4"></div>
            <p>Loading...</p>
          </div>
        )}

        {activeTab === 'entry' && (
          <GrantEntry 
            onGrantsAdded={handleGrantsAdded}
            availableTags={tags}
          />
        )}

        {activeTab === 'display' && (
          <GrantDisplay 
            grants={grants}
            availableTags={tags}
            onSearch={handleGrantSearch}
            onClearSearch={handleClearSearch}
            loading={loading}
          />
        )}
      </main>

      <footer className="bg-gray-800 text-white text-center py-4 mt-auto">
        <p className="text-sm opacity-80">Grant Tagging System - Built with React & Flask</p>
      </footer>
    </div>
  );
}

export default App;
