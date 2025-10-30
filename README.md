# Grant Tagging System

A React frontend and Python Flask backend system for categorizing and displaying grants with intelligent tagging and MySQL database integration.

## Features

- **Grant Entry**: Add new grants with name and description (manual or JSON bulk upload)
- **Intelligent Tagging**: Automatically assign relevant tags from predefined list using hybrid approach
- **Grant Display**: View all grants with their assigned tags in a beautiful card layout
- **Advanced Filtering**: Filter grants by tags, search by text, and sort results
- **Real-time Updates**: Immediate display of newly added grants
- **Responsive Design**: Works on desktop and mobile devices
- **MySQL Database**: Robust data persistence with SQLAlchemy ORM
- **Production Ready**: Deployed on Vercel with cloud database

## Project Structure

```
grant-tagging-system/
├── backend/
│   ├── app.py                    # Flask application with REST API
│   ├── database.py              # Database configuration
│   ├── models.py                # SQLAlchemy database models
│   ├── database_service.py     # Database operations service
│   ├── tagging_service.py       # Intelligent tagging logic
│   ├── setup_database.py       # Database setup and reset functionality
│   ├── seed_from_json.py       # Database seeding from JSON data
│   ├── data/
│   │   └── grants.json          # Sample grant data
│   ├── requirements.txt         # Python dependencies
│   ├── env_example.txt         # Environment variables template
│   └── vercel.json             # Vercel deployment configuration
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GrantEntry.js    # Grant input component
│   │   │   └── GrantDisplay.js  # Grant display component
│   │   ├── App.js              # Main React application
│   │   ├── App.css             # Tailwind CSS imports
│   │   └── index.js            # React entry point
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── tailwind.config.js     # Tailwind configuration
│   ├── postcss.config.js      # PostCSS configuration
│   └── package.json           # Node.js dependencies
└── README.md                  # This documentation
```

## Setup Instructions

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- MySQL database (local or cloud)
- (Optional) OpenAI API key for enhanced tagging

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Option 1: Use the setup script
   python setup_env.py
   
   # Option 2: Manual setup
   cp env_example.txt .env
   # Edit .env with your database credentials
   ```

5. **Set up the database:**
   ```bash
   # Create database and tables
   python setup_database.py
   
   # Or reset existing database
   python setup_database.py --reset
   ```

6. **Seed with sample data:**
   ```bash
   python seed_from_json.py
   ```

7. **Start the Flask server:**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000`

## Database Configuration

### Environment Variables (.env)

```bash
# Database Configuration
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=grant_tagging_db

# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key

# Environment
ENVIRONMENT=development
```

### Database Management

**Reset Database:**
```bash
python setup_database.py --reset
```

**Seed with JSON Data:**
```bash
python seed_from_json.py
```

**Check Database Status:**
```bash
python -c "
from database import create_database_engine, DB_CONFIG
from models import Grant, Tag
from sqlalchemy.orm import sessionmaker
engine = create_database_engine()
Session = sessionmaker(bind=engine)
session = Session()
print(f'Grants: {session.query(Grant).count()}')
print(f'Tags: {session.query(Tag).count()}')
session.close()
"
```

**Setup Environment File:**
```bash
# Create .env file with examples
python setup_env.py
```

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

## Tagging Algorithm

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
- Only assigns tags from the predefined list
- Prevents hallucinated or invalid tags
- Ensures consistency across the system

## Usage Guide

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

## Deployment

### Vercel Deployment

**Backend Deployment:**
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

**Frontend Deployment:**
1. Build the React app: `npm run build`
2. Deploy to Vercel or any static hosting service
3. Update API URLs for production

### Environment Variables for Production

```bash
# Database Configuration
DB_HOST=your_production_database_host
DB_PORT=3306
DB_USER=your_production_username
DB_PASSWORD=your_production_password
DB_NAME=grant_tagging_db


# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# Environment
ENVIRONMENT=production
```

## Technical Implementation

### Backend Architecture
- **Flask**: Lightweight web framework for API
- **SQLAlchemy**: Python ORM for database operations
- **MySQL**: Robust relational database
- **CORS Support**: Cross-origin requests for frontend
- **Error Handling**: Comprehensive error responses

### Frontend Architecture
- **React Hooks**: Modern state management
- **Axios**: HTTP client for API communication
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Component-based**: Modular, reusable components

### Database Schema
- **Grants Table**: `id`, `grant_name`, `grant_description`, `created_at`, `updated_at`
- **Tags Table**: `id`, `name`, `description`, `created_at`
- **Grant-Tags Association**: Many-to-many relationship table

### Data Flow
1. User enters grant data (manual or JSON)
2. Frontend sends data to backend API
3. Backend processes grants through tagging service
4. Tags are assigned using hybrid algorithm
5. Grants are stored in MySQL database
6. Frontend receives tagged grants and updates display

## Testing

The system has been tested with:
- **MySQL database integration**
- **JSON data seeding** from existing grant files
- **Responsive filtering** and search functionality
- **Production deployment** on Vercel
- **Cross-origin requests** between frontend and backend

## Future Enhancements

### Extension Options
1. **Enhanced Tagging**: Extract content from document/website URLs
2. **Smart Search**: Handle synonyms and related terms
3. **Dynamic Tags**: Automatically create new tags for emerging concepts
4. **Analytics**: Tag usage statistics and trends
5. **Export**: Download grants as CSV/JSON
6. **User Management**: Multi-user support with permissions
7. **Caching**: Redis for improved performance
8. **API Rate Limiting**: Protect against abuse

## Development Notes

### Design Decisions
- **Hybrid Tagging**: Combines rule-based and AI approaches for accuracy
- **MySQL Database**: Robust, scalable data persistence
- **React Hooks**: Modern, functional component architecture
- **Tailwind CSS**: Utility-first styling for consistent, responsive design
- **Production Ready**: Vercel deployment with cloud database

### Performance Considerations
- **Efficient Filtering**: Client-side filtering for fast response
- **Database Indexing**: Optimized queries for large datasets
- **Connection Pooling**: Efficient database connections
- **Caching**: Browser caching for static assets

## Contributing

This project was built as a technical assessment demonstrating:
- Full-stack development skills
- Database design and ORM usage
- API design and implementation
- Frontend architecture and UX
- Intelligent data processing
- Production deployment

## 📄 License

This project is part of a technical assessment for Lasso.
