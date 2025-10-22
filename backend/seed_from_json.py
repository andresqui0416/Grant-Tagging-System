#!/usr/bin/env python3
"""
Simple database seeding script using existing grants.json data
"""

import json
import os
from database import DB_CONFIG, create_database_engine
from models import Grant, Tag
from sqlalchemy.orm import sessionmaker

def load_grants_from_json():
    """Load grants data from grants.json file"""
    json_file = os.path.join(os.path.dirname(__file__), 'data', 'grants.json')
    
    try:
        with open(json_file, 'r') as f:
            grants_data = json.load(f)
        print(f"📄 Loaded {len(grants_data)} grants from grants.json")
        return grants_data
    except FileNotFoundError:
        print(f"❌ File not found: {json_file}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return []

def create_tags_from_grants(session, grants_data):
    """Create tags from all unique tags in grants data"""
    print("📝 Creating tags from grants data...")
    
    # Collect all unique tags
    all_tags = set()
    for grant in grants_data:
        if 'tags' in grant:
            all_tags.update(grant['tags'])
    
    created_tags = []
    for tag_name in sorted(all_tags):
        # Check if tag already exists
        existing_tag = session.query(Tag).filter_by(name=tag_name).first()
        if not existing_tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            created_tags.append(tag)
            print(f"  ✅ Created tag: {tag_name}")
        else:
            created_tags.append(existing_tag)
            print(f"  ℹ️  Tag already exists: {tag_name}")
    
    session.commit()
    print(f"📊 Total tags: {len(created_tags)}")
    return created_tags

def create_grants_from_json(session, grants_data):
    """Create grants from JSON data"""
    print("📝 Creating grants from JSON data...")
    
    created_grants = []
    for grant_data in grants_data:
        # Check if grant already exists
        existing_grant = session.query(Grant).filter_by(grant_name=grant_data['grant_name']).first()
        if not existing_grant:
            # Create grant
            grant = Grant(
                grant_name=grant_data['grant_name'],
                grant_description=grant_data['grant_description']
            )
            session.add(grant)
            session.flush()  # Get the ID
            
            # Assign tags
            assigned_tags = []
            if 'tags' in grant_data:
                for tag_name in grant_data['tags']:
                    tag = session.query(Tag).filter_by(name=tag_name).first()
                    if tag:
                        grant.tags.append(tag)
                        assigned_tags.append(tag_name)
            
            print(f"  ✅ Created grant: {grant_data['grant_name']}")
            if assigned_tags:
                print(f"     📋 Tags: {', '.join(assigned_tags[:5])}{'...' if len(assigned_tags) > 5 else ''}")
            
            created_grants.append(grant)
        else:
            print(f"  ℹ️  Grant already exists: {grant_data['grant_name']}")
            created_grants.append(existing_grant)
    
    session.commit()
    print(f"📊 Total grants: {len(created_grants)}")
    return created_grants

def main():
    """Main seeding function"""
    print("🌱 Grant Tagging System Database Seeding (from JSON)")
    print("=" * 60)
    
    try:
        # Use the existing database engine creation function (handles proxy automatically)
        engine = create_database_engine()
        if engine is None:
            print("❌ Failed to create database engine")
            return
        
        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print(f"📊 Database: {DB_CONFIG['database']}")
        print(f"🏠 Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        print()
        
        # Load grants data from JSON
        grants_data = load_grants_from_json()
        if not grants_data:
            print("❌ No grants data found")
            return
        
        # Create tags from grants data
        tags = create_tags_from_grants(session, grants_data)
        print()
        
        # Create grants from JSON data
        grants = create_grants_from_json(session, grants_data)
        print()
        
        # Display summary
        print("📈 Seeding Summary:")
        print(f"  🏷️  Tags created: {len(tags)}")
        print(f"  📄 Grants created: {len(grants)}")
        print()
        
        # Show some examples
        print("🔍 Sample Data Preview:")
        recent_grants = session.query(Grant).limit(3).all()
        for grant in recent_grants:
            print(f"  📄 {grant.grant_name}")
            grant_tag_names = [tag.name for tag in grant.tags]
            if grant_tag_names:
                print(f"     🏷️  Tags: {', '.join(grant_tag_names[:5])}{'...' if len(grant_tag_names) > 5 else ''}")
            else:
                print(f"     🏷️  Tags: None")
            print()
        
        print("✅ Database seeding completed successfully!")
        print()
        print("🚀 Next steps:")
        print("  1. Run the Flask application: python app.py")
        print("  2. Open the frontend to view and manage grants")
        print("  3. Test the tagging and filtering functionality")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
