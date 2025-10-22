from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from database_service import DatabaseService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize database service
try:
    db_service = DatabaseService()
    logger.info("Database service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database service: {e}")
    db_service = None

@app.route('/api/grants', methods=['GET'])
def get_grants():
    """Get all grants"""
    try:
        if not db_service:
            return jsonify({
                'success': False,
                'error': 'Database service not available'
            }), 500
            
        result = db_service.get_all_grants()
        if result['success']:
            return jsonify({
                'success': True,
                'grants': result['grants'],
                'count': len(result['grants'])
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in get_grants: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grants', methods=['POST'])
def add_grants():
    """Add new grants with automatic tagging"""
    try:
        if not db_service:
            return jsonify({
                'success': False,
                'error': 'Database service not available'
            }), 500
            
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Handle both single grant and array of grants
        grants_to_add = data if isinstance(data, list) else [data]
        
        # Validate grants
        validated_grants = []
        for grant in grants_to_add:
            if grant.get('grant_name') and grant.get('grant_description'):
                validated_grants.append({
                    'grant_name': grant['grant_name'],
                    'grant_description': grant['grant_description']
                })
        
        if not validated_grants:
            return jsonify({
                'success': False,
                'error': 'No valid grants provided'
            }), 400
        
        # Add grants to database
        result = db_service.add_grants(validated_grants)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'grants_added': result['grants_added'],
                'count': len(result['grants_added'])
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in add_grants: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Get all available tags"""
    try:
        if not db_service:
            return jsonify({
                'success': False,
                'error': 'Database service not available'
            }), 500
            
        result = db_service.get_all_tags()
        if result['success']:
            return jsonify({
                'success': True,
                'tags': result['tags'],
                'count': len(result['tags'])
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in get_tags: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grants/search', methods=['POST'])
def search_grants():
    """Search grants by tags"""
    try:
        if not db_service:
            return jsonify({
                'success': False,
                'error': 'Database service not available'
            }), 500
            
        data = request.get_json()
        search_tags = data.get('tags', []) if data else []
        
        result = db_service.search_grants_by_tags(search_tags)
        
        if result['success']:
            return jsonify({
                'success': True,
                'grants': result['grants'],
                'count': len(result['grants']),
                'search_tags': search_tags
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in search_grants: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grants/<int:grant_id>', methods=['GET'])
def get_grant(grant_id):
    """Get a specific grant by ID"""
    try:
        if not db_service:
            return jsonify({
                'success': False,
                'error': 'Database service not available'
            }), 500
            
        result = db_service.get_grant_by_id(grant_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_grant: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grants/<int:grant_id>', methods=['DELETE'])
def delete_grant(grant_id):
    """Delete a grant by ID"""
    try:
        if not db_service:
            return jsonify({
                'success': False,
                'error': 'Database service not available'
            }), 500
            
        result = db_service.delete_grant(grant_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in delete_grant: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        db_status = "connected" if db_service else "disconnected"
        return jsonify({
            'success': True,
            'message': 'Grant Tagging API is running',
            'version': '1.0.0',
            'database': db_status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    environment = os.getenv('ENVIRONMENT')
    if environment == 'development':
        print("Starting Grant Tagging API...")
        print("Available endpoints:")
        print("  GET    /api/grants - Get all grants")
        print("  POST   /api/grants - Add new grants")
        print("  GET    /api/grants/<id> - Get specific grant")
        print("  DELETE /api/grants/<id> - Delete grant")
        print("  GET    /api/tags - Get available tags")
        print("  POST   /api/grants/search - Search grants by tags")
        print("  GET    /api/health - Health check")
        app.run(debug=True, host='0.0.0.0', port=5000)
    elif environment == 'vercel_production':
        print("Starting Grant Tagging API in vercel production mode...")
    else:
        print("Starting Grant Tagging API in development mode...")
        app.run(debug=True, host='0.0.0.0', port=5000)