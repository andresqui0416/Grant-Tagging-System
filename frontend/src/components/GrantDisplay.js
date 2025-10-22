import React, { useState, useEffect } from 'react';

const GrantDisplay = ({ grants, availableTags, onSearch, onClearSearch, loading }) => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [filteredGrants, setFilteredGrants] = useState(grants);

  // Update filtered grants when grants or filters change
  useEffect(() => {
    let filtered = [...grants];

    // Filter by selected tags
    if (selectedTags.length > 0) {
      filtered = filtered.filter(grant => 
        selectedTags.some(tag => grant.tags && grant.tags.includes(tag))
      );
    }

    // Filter by search term
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(grant => 
        grant.grant_name.toLowerCase().includes(term) ||
        grant.grant_description.toLowerCase().includes(term)
      );
    }

    // Sort grants
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.grant_name.localeCompare(b.grant_name);
        case 'tags':
          return (b.tags?.length || 0) - (a.tags?.length || 0);
        default:
          return 0;
      }
    });

    setFilteredGrants(filtered);
  }, [grants, selectedTags, searchTerm, sortBy]);

  const handleTagToggle = (tag) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const handleSearch = () => {
    if (selectedTags.length > 0) {
      onSearch(selectedTags);
    }
  };

  const handleClearFilters = () => {
    setSelectedTags([]);
    setSearchTerm('');
    onClearSearch();
  };

  const getTagCounts = () => {
    const counts = {};
    grants.forEach(grant => {
      if (grant.tags) {
        grant.tags.forEach(tag => {
          counts[tag] = (counts[tag] || 0) + 1;
        });
      }
    });
    return counts;
  };

  const tagCounts = getTagCounts();
  const sortedTags = availableTags
    .filter(tag => tagCounts[tag] > 0)
    .sort((a, b) => (tagCounts[b] || 0) - (tagCounts[a] || 0));

  return (
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Grant Database</h2>
        <p className="text-gray-600">Browse and filter grants by tags or search terms</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search grants by name or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Filter by Tags</h3>
            <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto p-3 border border-gray-200 rounded-lg bg-gray-50">
              {sortedTags.slice(0, 20).map(tag => (
                <button
                  key={tag}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-all duration-200 ${
                    selectedTags.includes(tag)
                      ? 'bg-primary-500 text-white'
                      : 'bg-white text-gray-600 border border-gray-300 hover:bg-gray-100'
                  }`}
                  onClick={() => handleTagToggle(tag)}
                >
                  {tag} ({tagCounts[tag] || 0})
                </button>
              ))}
              {sortedTags.length > 20 && (
                <span className="text-gray-500 text-sm italic px-3 py-1 self-center">
                  +{sortedTags.length - 20} more tags available
                </span>
              )}
            </div>
          </div>

          <div className="flex flex-col">
            <label htmlFor="sort-select" className="text-sm font-medium text-gray-700 mb-2">Sort by:</label>
            <select
              id="sort-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white"
            >
              <option value="name">Name (A-Z)</option>
              <option value="tags">Most Tagged</option>
            </select>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <button 
            onClick={handleSearch} 
            className="bg-gradient-to-r from-primary-500 to-primary-600 text-white px-6 py-2 rounded-md font-medium hover:from-primary-600 hover:to-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200"
            disabled={selectedTags.length === 0}
          >
            Search by Tags
          </button>
          <button 
            onClick={handleClearFilters} 
            className="bg-gray-100 text-gray-700 border border-gray-300 px-6 py-2 rounded-md font-medium hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200"
          >
            Clear All Filters
          </button>
        </div>
      </div>

      <div className="bg-primary-50 p-4 rounded-lg border border-primary-200 mb-6">
        <p className="text-gray-700 font-medium">
          Showing {filteredGrants.length} of {grants.length} grants
          {selectedTags.length > 0 && ` (filtered by ${selectedTags.length} tag${selectedTags.length > 1 ? 's' : ''})`}
        </p>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-12 text-gray-600">
          <div className="w-10 h-10 border-4 border-gray-200 border-t-primary-500 rounded-full animate-spin mb-4"></div>
          <p>Loading grants...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredGrants.length === 0 ? (
            <div className="col-span-full text-center py-12 text-gray-600">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No grants found</h3>
              <p>Try adjusting your search criteria or add some grants first.</p>
            </div>
          ) : (
            filteredGrants.map((grant, index) => (
              <div key={grant.id || index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3 leading-tight">{grant.grant_name}</h3>
                  {grant.tags && grant.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {grant.tags.map(tag => (
                        <span key={tag} className="bg-primary-500 text-white px-2 py-1 rounded text-xs font-medium">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                
                <div className="mb-4">
                  <p className="text-gray-600 leading-relaxed">{grant.grant_description}</p>
                </div>

                {(grant.website_urls || grant.document_urls) && (
                  <div className="border-t border-gray-200 pt-4">
                    {grant.website_urls && grant.website_urls.length > 0 && (
                      <div className="mb-3">
                        <strong className="block text-sm font-medium text-gray-900 mb-2">Websites:</strong>
                        <ul className="space-y-1">
                          {grant.website_urls.map((url, idx) => (
                            <li key={idx}>
                              <a 
                                href={url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-primary-600 hover:text-primary-800 text-sm break-all"
                              >
                                {url}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {grant.document_urls && grant.document_urls.length > 0 && (
                      <div>
                        <strong className="block text-sm font-medium text-gray-900 mb-2">Documents:</strong>
                        <ul className="space-y-1">
                          {grant.document_urls.map((url, idx) => (
                            <li key={idx}>
                              <a 
                                href={url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-primary-600 hover:text-primary-800 text-sm break-all"
                              >
                                {url}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default GrantDisplay;
