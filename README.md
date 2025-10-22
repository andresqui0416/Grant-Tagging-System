# Grant Tagging System

A React frontend and Python Flask backend system for categorizing and displaying grants with intelligent tagging.

## 🚀 Features

- **Grant Entry**: Add new grants with name and description (manual or JSON bulk upload)
- **Intelligent Tagging**: Automatically assign relevant tags from predefined list using hybrid approach
- **Grant Display**: View all grants with their assigned tags in a beautiful card layout
- **Advanced Filtering**: Filter grants by tags, search by text, and sort results
- **Real-time Updates**: Immediate display of newly added grants
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Project Structure

```
grant-tagging-system/
├── backend/
│   ├── app.py                    # Flask application with REST API
│   ├── tagging_service.py        # Intelligent tagging logic
│   ├── data/
│   │   └── grants.json           # JSON-based grant storage
│   ├── requirements.txt           # Python dependencies
│   └── env_example.txt           # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GrantEntry.js     # Grant input component
│   │   │   └── GrantDisplay.js   # Grant display component
│   │   ├── App.js               # Main React application
│   │   ├── App.css              # Tailwind CSS imports
│   │   └── index.js             # React entry point
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── tailwind.config.js       # Tailwind configuration
│   ├── postcss.config.js        # PostCSS configuration
│   └── package.json            # Node.js dependencies
├── test_grants.json            # Sample grant data for testing
└── README.md                   # This documentation
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- (Optional) OpenAI API key for enhanced tagging

### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up OpenAI API key for enhanced tagging:
   ```bash
   cp env_example.txt .env
   # Edit .env and add your OpenAI API key
   ```

5. Start the Flask server:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```
   
   Note: The project includes Tailwind CSS v3.4+ with standard PostCSS integration.

3. Start the React development server:
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/grants` | Retrieve all grants with tags |
| `POST` | `/api/grants` | Add new grants (single or bulk) |
| `GET` | `/api/tags` | Get all available tags |
| `POST` | `/api/grants/search` | Search grants by tags |
| `GET` | `/api/health` | Health check endpoint |

### Example API Usage

**Add a single grant:**
```bash
curl -X POST http://localhost:5000/api/grants \
  -H "Content-Type: application/json" \
  -d '{"grant_name": "Test Grant", "grant_description": "A test grant for demonstration"}'
```

**Add multiple grants:**
```bash
curl -X POST http://localhost:5000/api/grants \
  -H "Content-Type: application/json" \
  -d '[{"grant_name": "Grant 1", "grant_description": "..."}, {"grant_name": "Grant 2", "grant_description": "..."}]'
```

## 🧠 Tagging Algorithm

The system uses a sophisticated hybrid approach for accurate tag assignment:

### 1. String Matching
- Direct keyword matching against grant descriptions
- Comprehensive keyword mappings for semantic variations
- Special handling for compound terms (e.g., "farm-to-school", "local-food")

### 2. LLM Enhancement (Optional)
- OpenAI GPT-3.5-turbo for semantic understanding
- Context-aware tag assignment
- Handles complex relationships and implicit themes

### 3. Precision Filtering
- Only assigns tags from the predefined list (89 available tags)
- Prevents hallucinated or invalid tags
- Ensures consistency across the system

### Tag Categories
The system includes 89 predefined tags covering:
- **Agriculture**: agriculture, farming, soil, water, conservation
- **Education**: education, training, outreach, youth
- **Infrastructure**: infrastructure, equipment, capital, facilities
- **Program Types**: pilot, competitive, cost-share, reimbursement
- **Target Audiences**: farmer, youth, veteran, tribal, underserved
- **Geographic**: state-specific tags (wi, va, ri, nh, mn, me, ky, co)
- **Specialized**: equine, seafood, dairy, organic, disaster-relief

## 🎯 Tagging Performance

Based on testing with the provided grant data:

- **Precision**: High accuracy in tag assignment
- **Recall**: Captures most relevant tags for each grant
- **Coverage**: Successfully tags all major themes and concepts
- **Consistency**: Maintains consistent tagging across similar grants

### Example Tagging Results
- **Nutrient Management Grant**: `["soil", "education", "agriculture", "nutrient-management", "farmer", "planning"]`
- **Farm to School Program**: `["farm-to-school", "pilot", "procurement", "local-food", "school"]`
- **Drought Relief Fund**: `["water", "disaster-relief", "drought", "irrigation", "farmer"]`

## 🚀 Usage Guide

### Adding Grants
1. **Manual Entry**: Use the form to enter grant name and description
2. **JSON Upload**: Paste JSON data for bulk grant addition
3. **Sample Data**: Use the "Load Sample Data" button to test with example grants

### Viewing and Filtering Grants
1. **Browse All**: View all grants in a responsive card layout
2. **Tag Filtering**: Click tags to filter grants by specific categories
3. **Text Search**: Search grants by name or description
4. **Sorting**: Sort by name or number of tags
5. **Clear Filters**: Reset all filters to view all grants

### Advanced Features
- **Real-time Updates**: New grants appear immediately
- **Tag Counts**: See how many grants have each tag
- **Responsive Design**: Works on all screen sizes
- **Error Handling**: Graceful error messages and validation

## 🔧 Technical Implementation

### Backend Architecture
- **Flask**: Lightweight web framework for API
- **JSON Storage**: Simple file-based data persistence
- **CORS Support**: Cross-origin requests for frontend
- **Error Handling**: Comprehensive error responses

### Frontend Architecture
- **React Hooks**: Modern state management
- **Axios**: HTTP client for API communication
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Component-based**: Modular, reusable components

### Data Flow
1. User enters grant data (manual or JSON)
2. Frontend sends data to backend API
3. Backend processes grants through tagging service
4. Tags are assigned using hybrid algorithm
5. Grants are stored in JSON file
6. Frontend receives tagged grants and updates display

## 🧪 Testing

The system has been tested with the provided grant dataset:
- **8 grants** successfully processed
- **Accurate tagging** for all major themes
- **Proper handling** of optional fields (URLs, documents)
- **Responsive filtering** and search functionality

## 🚀 Future Enhancements

### Extension Options (if time permits)
1. **Enhanced Tagging**: Extract content from document/website URLs
2. **Smart Search**: Handle synonyms and related terms
3. **Dynamic Tags**: Automatically create new tags for emerging concepts
4. **Analytics**: Tag usage statistics and trends
5. **Export**: Download grants as CSV/JSON
6. **User Management**: Multi-user support with permissions

## 📝 Development Notes

### Design Decisions
- **Hybrid Tagging**: Combines rule-based and AI approaches for accuracy
- **JSON Storage**: Simple, portable data format
- **React Hooks**: Modern, functional component architecture
- **Tailwind CSS**: Utility-first styling for consistent, responsive design
- **Responsive Design**: Mobile-first approach with Tailwind's responsive utilities
- **Error Handling**: User-friendly error messages

### Performance Considerations
- **Efficient Filtering**: Client-side filtering for fast response
- **Lazy Loading**: Components load as needed
- **Optimized Queries**: Minimal API calls
- **Caching**: Browser caching for static assets

## 🤝 Contributing

This project was built as a technical assessment demonstrating:
- Full-stack development skills
- API design and implementation
- Frontend architecture and UX
- Intelligent data processing
- Problem-solving and creativity

## 📄 License

This project is part of a technical assessment for Lasso.
