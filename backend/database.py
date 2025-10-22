import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'grant_tagging_db'),
    'use_proxy': os.getenv('USE_PROXY', 'FALSE').upper() == 'TRUE',
    'proxy_host': os.getenv('DB_PROXY_HOST', ''),
    'proxy_port': int(os.getenv('DB_PROXY_PORT', 0)),
    'proxy_user': os.getenv('DB_PROXY_USER', ''),
    'proxy_password': os.getenv('DB_PROXY_PASSWORD', '')
}

print(f"Database configuration loaded: {DB_CONFIG}")

def get_database_url():
    """Generate database URL for SQLAlchemy"""
    return f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

def setup_proxy():
    """Set up SOCKS proxy if configured and enabled"""
    # Check if proxy is enabled
    if not DB_CONFIG['use_proxy']:
        print("ℹ️  Proxy disabled (USE_PROXY=FALSE)")
        return True
    
    # Check if proxy configuration is provided
    if not DB_CONFIG['proxy_host'] or not DB_CONFIG['proxy_port']:
        print("⚠️  USE_PROXY=TRUE but proxy configuration is missing")
        print("   Please set DB_PROXY_HOST, DB_PROXY_PORT, DB_PROXY_USER, DB_PROXY_PASSWORD")
        return False
    
    try:
        import socks
        import socket
        
        # Set up SOCKS proxy
        socks.set_default_proxy(socks.SOCKS5, DB_CONFIG['proxy_host'], DB_CONFIG['proxy_port'], 
                              username=DB_CONFIG['proxy_user'], password=DB_CONFIG['proxy_password'])
        socket.socket = socks.socksocket
        
        print(f"✅ Using SOCKS proxy: {DB_CONFIG['proxy_host']}:{DB_CONFIG['proxy_port']}")
        return True
        
    except ImportError:
        print("⚠️  PySocks not installed. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySocks"])
        print("✅ PySocks installed. Please restart the application.")
        return False
    except Exception as e:
        print(f"❌ Error setting up proxy: {e}")
        print("⚠️  Continuing without proxy...")
        return False

def create_database_engine():
    """Create database engine with optional proxy support"""
    database_url = get_database_url()
    
    # Set up proxy if configured
    if not setup_proxy():
        return None
    
    return create_engine(database_url, echo=False)

def get_db_session():
    """Get database session"""
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_server_engine():
    """Create database engine for server connection (without database name)"""
    # For creating the database, we need to connect without specifying the database name
    server_url = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
    
    # Set up proxy if configured
    if not setup_proxy():
        return None
    
    return create_engine(server_url, echo=False)

def init_database(app):
    """Initialize database with Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Set up proxy if configured
    setup_proxy()
    
    db = SQLAlchemy(app)
    return db
