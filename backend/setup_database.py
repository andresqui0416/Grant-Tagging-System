#!/usr/bin/env python3
"""
Database setup script for Grant Tagging System
Run this script to create the database and tables
"""

import os
import sys
from sqlalchemy import create_engine, text
from database import get_database_url, DB_CONFIG, create_database_engine, create_server_engine
from models import Base

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Use the existing server engine creation function (handles proxy automatically)
        engine = create_server_engine()
        if engine is None:
            print("❌ Failed to create server engine")
            return False
        
        with engine.connect() as conn:
            # Create database if it doesn't exist
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}"))
            conn.commit()
            print(f"✅ Database '{DB_CONFIG['database']}' created/verified")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    print("🗑️  Resetting database...")
    try:
        # First, we need to connect to the database to drop tables
        # Use the existing database engine creation function (handles proxy automatically)
        engine = create_database_engine()
        if engine is None:
            print("❌ Failed to create database engine")
            return False
        
        print(f"  🔗 Connected to database: {DB_CONFIG['database']}")
        
        # Drop all tables
        print("  🗑️  Dropping all tables...")
        Base.metadata.drop_all(engine)
        print("  ✅ All tables dropped")
        
        # Force commit the drop operation
        engine.dispose()
        
        # Recreate connection and tables
        print("  🔄 Reconnecting to database...")
        engine = create_database_engine()
        if engine is None:
            print("❌ Failed to reconnect to database")
            return False
        
        # Recreate all tables
        print("  🔨 Recreating all tables...")
        Base.metadata.create_all(engine)
        print("  ✅ All tables recreated")
        
        # Verify tables are empty
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Check if tables are actually empty
        from models import Grant, Tag
        grant_count = session.query(Grant).count()
        tag_count = session.query(Tag).count()
        
        print(f"  📊 Verification: {grant_count} grants, {tag_count} tags")
        
        session.close()
        engine.dispose()
        
        print("🎉 Database reset completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_tables():
    """Create all tables"""
    try:
        # Use the existing database engine creation function (handles proxy automatically)
        engine = create_database_engine()
        if engine is None:
            print("❌ Failed to create database engine")
            return False
        
        # Create all tables
        Base.metadata.create_all(engine)
        print("✅ All tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main setup function"""
    import sys
    
    # Check if reset flag is provided
    reset_flag = len(sys.argv) > 1 and sys.argv[1] == '--reset'
    
    if reset_flag:
        print("🔄 Resetting Grant Tagging System Database...")
        print("⚠️  This will delete ALL existing data!")
    else:
        print("🚀 Setting up Grant Tagging System Database...")
    
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"User: {DB_CONFIG['user']}")
    
    if DB_CONFIG['use_proxy']:
        if DB_CONFIG['proxy_host'] and DB_CONFIG['proxy_port']:
            print(f"Proxy: {DB_CONFIG['proxy_host']}:{DB_CONFIG['proxy_port']}")
            print(f"Proxy User: {DB_CONFIG['proxy_user']}")
        else:
            print("⚠️  USE_PROXY=TRUE but proxy configuration is missing")
    else:
        print("No proxy configured (USE_PROXY=FALSE)")
    print()
    
    # Create database
    if not create_database():
        print("❌ Failed to create database")
        sys.exit(1)
    
    # Reset tables if requested
    if reset_flag:
        if not reset_database():
            print("❌ Failed to reset database")
            sys.exit(1)
    else:
        # Create tables
        if not create_tables():
            print("❌ Failed to create tables")
            sys.exit(1)
    
    print()
    if reset_flag:
        print("🎉 Database reset completed successfully!")
    else:
        print("🎉 Database setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Run the seed script: python seed_from_json.py")
    print("2. Run the Flask application: python app.py")

if __name__ == "__main__":
    main()
