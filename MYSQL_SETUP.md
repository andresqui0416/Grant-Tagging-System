# MySQL Setup Guide for Grant Tagging System

This guide will help you set up MySQL database for the Grant Tagging System backend.

## Prerequisites

1. **MySQL Server** - Install MySQL 8.0 or later
2. **Python 3.8+** - Already installed
3. **Virtual Environment** - Already set up

## Step 1: Install MySQL Server

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### macOS (with Homebrew):
```bash
brew install mysql
brew services start mysql
```

### Windows:
Download and install from [MySQL Official Website](https://dev.mysql.com/downloads/mysql/)

## Step 2: Create Database and User

Connect to MySQL as root:
```bash
sudo mysql -u root -p
```

Create database and user:
```sql
CREATE DATABASE grant_tagging_db;
CREATE USER 'grant_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON grant_tagging_db.* TO 'grant_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Step 3: Configure Environment Variables

Create a `.env` file in the backend directory:
```bash
cd backend
nano .env
```

Add the following content:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=grant_user
DB_PASSWORD=your_secure_password
DB_NAME=grant_tagging_db

# OpenAI API Key (optional - for enhanced tagging)
OPENAI_API_KEY=your_openai_api_key_here

# Environment
ENVIRONMENT=development
```

## Step 4: Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

## Step 5: Set Up Database Tables

Run the database setup script:
```bash
python setup_database.py
python seed_from_json.py
```

This will:
- Create the database (if it doesn't exist)
- Create all necessary tables
- Initialize default tags

## Step 6: Test the Setup

Start the Flask application:
```bash
python app.py
```

Test the health endpoint:
```bash
curl http://localhost:5000/api/health
```

You should see:
```json
{
  "success": true,
  "message": "Grant Tagging API is running",
  "version": "1.0.0",
  "database": "connected"
}
```

## Database Schema

The system creates the following tables:

### `grants` table:
- `id` (Primary Key, Auto Increment)
- `grant_name` (VARCHAR 255)
- `grant_description` (TEXT)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

### `tags` table:
- `id` (Primary Key, Auto Increment)
- `name` (VARCHAR 100, Unique)
- `description` (TEXT)
- `created_at` (DATETIME)

### `grant_tags` table (Many-to-Many):
- `grant_id` (Foreign Key to grants.id)
- `tag_id` (Foreign Key to tags.id)

## API Endpoints

The following endpoints are available:

- `GET /api/grants` - Get all grants
- `POST /api/grants` - Add new grants
- `GET /api/grants/<id>` - Get specific grant
- `DELETE /api/grants/<id>` - Delete grant
- `GET /api/tags` - Get all available tags
- `POST /api/grants/search` - Search grants by tags
- `GET /api/health` - Health check

## Troubleshooting

### Connection Issues:
1. Check MySQL service is running: `sudo systemctl status mysql`
2. Verify database credentials in `.env` file
3. Test connection: `mysql -u grant_user -p grant_tagging_db`

### Permission Issues:
```sql
GRANT ALL PRIVILEGES ON grant_tagging_db.* TO 'grant_user'@'localhost';
FLUSH PRIVILEGES;
```

### Port Issues:
- Default MySQL port is 3306
- Check if port is available: `netstat -tlnp | grep 3306`

## Production Deployment

For production deployment (Vercel), you'll need to:

1. **Use a cloud MySQL service** (like PlanetScale, AWS RDS, or Google Cloud SQL)
2. **Update environment variables** in your deployment platform
3. **Ensure SSL connections** are enabled
4. **Set up connection pooling** for better performance

### Example Production Environment Variables:
```env
DB_HOST=your-cloud-mysql-host.com
DB_PORT=3306
DB_USER=your_production_user
DB_PASSWORD=your_secure_production_password
DB_NAME=grant_tagging_db
ENVIRONMENT=production
```

## Migration from JSON to MySQL

If you have existing data in JSON format, you can migrate it:

1. Export existing grants from JSON file
2. Use the `/api/grants` POST endpoint to add them to MySQL
3. The system will automatically assign tags

## Next Steps

1. Test the frontend connection to the new MySQL backend
2. Deploy to production with cloud MySQL
3. Set up database backups
4. Monitor database performance

