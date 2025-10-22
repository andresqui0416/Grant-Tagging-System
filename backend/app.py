from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from tagging_service import GrantTaggingService

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize tagging service
tagging_service = GrantTaggingService()

# Data file path
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'grants.json')

def load_grants():
    """Load grants from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading grants: {e}")
        return []

def save_grants(grants):
    """Save grants to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(grants, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving grants: {e}")
        return False

@app.route('/api/grants', methods=['GET'])
def get_grants():
    """Get all grants"""
    try:
        grants = load_grants()
        return jsonify({
            'success': True,
            'grants': grants,
            'count': len(grants)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grants', methods=['POST'])
def add_grants():
    """Add new grants with automatic tagging"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Handle both single grant and array of grants
        grants_to_add = data if isinstance(data, list) else [data]
        
        # Load existing grants
        existing_grants = load_grants()
        
        # Process each grant
        processed_grants = []
        for grant in grants_to_add:
            # Validate required fields
            if not grant.get('grant_name') or not grant.get('grant_description'):
                continue
            
            # Assign tags using the tagging service
            tags = tagging_service.assign_tags(
                grant['grant_name'], 
                grant['grant_description']
            )
            
            # Create processed grant object
            processed_grant = {
                'grant_name': grant['grant_name'],
                'grant_description': grant['grant_description'],
                'tags': tags,
                'id': len(existing_grants) + len(processed_grants) + 1  # Simple ID generation
            }
            
            # Add optional fields if present
            if 'website_urls' in grant:
                processed_grant['website_urls'] = grant['website_urls']
            if 'document_urls' in grant:
                processed_grant['document_urls'] = grant['document_urls']
            
            processed_grants.append(processed_grant)
        
        # Add processed grants to existing grants
        all_grants = existing_grants + processed_grants
        
        # Save to file
        if save_grants(all_grants):
            return jsonify({
                'success': True,
                'message': f'Successfully added {len(processed_grants)} grants',
                'grants_added': processed_grants,
                'total_grants': len(all_grants)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save grants'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Get all available tags"""
    try:
        tags = tagging_service.get_available_tags()
        return jsonify({
            'success': True,
            'tags': tags,
            'count': len(tags)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grants/search', methods=['POST'])
def search_grants():
    """Search grants by tags"""
    try:
        data = request.get_json()
        search_tags = data.get('tags', []) if data else []
        
        grants = load_grants()
        
        if not search_tags:
            # Return all grants if no tags specified
            filtered_grants = grants
        else:
            # Filter grants that have any of the specified tags
            filtered_grants = [
                grant for grant in grants 
                if any(tag in grant.get('tags', []) for tag in search_tags)
            ]
        
        return jsonify({
            'success': True,
            'grants': filtered_grants,
            'count': len(filtered_grants),
            'search_tags': search_tags
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Grant Tagging API is running',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    environment = os.getenv('ENVIRONMENT')
    if environment == 'development':
        print("Starting Grant Tagging API...")
        print("Available endpoints:")
        print("  GET  /api/grants - Get all grants")
        print("  POST /api/grants - Add new grants")
        print("  GET  /api/tags - Get available tags")
        print("  POST /api/grants/search - Search grants by tags")
        print("  GET  /api/health - Health check")
        app.run(debug=True, host='0.0.0.0', port=5000)
    elif environment == 'vercel_production':
        print("Starting Grant Tagging API in vercel production mode...")
    else:
        print("Starting Grant Tagging API in development mode...")
        app.run(debug=True, host='0.0.0.0', port=5000)
