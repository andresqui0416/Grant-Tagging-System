from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
from database import create_database_engine
from models import Grant, Tag, Base
from tagging_service import GrantTaggingService
import logging

class DatabaseService:
    def __init__(self):
        self.engine = create_database_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.tagging_service = GrantTaggingService()
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        # Initialize default tags
        self._initialize_default_tags()
    
    def _initialize_default_tags(self):
        """Initialize default tags if they don't exist"""
        session = self.Session()
        try:
            # Check if tags already exist
            if session.query(Tag).count() == 0:
                default_tags = self.tagging_service.available_tags
                for tag_name in default_tags:
                    tag = Tag(name=tag_name)
                    session.add(tag)
                session.commit()
                logging.info(f"Initialized {len(default_tags)} default tags")
        except Exception as e:
            logging.error(f"Error initializing default tags: {e}")
            session.rollback()
        finally:
            session.close()
    
    def add_grants(self, grants_data):
        """Add new grants to the database"""
        session = self.Session()
        try:
            added_grants = []
            
            for grant_data in grants_data:
                # Create grant
                grant = Grant(
                    grant_name=grant_data['grant_name'],
                    grant_description=grant_data['grant_description']
                )
                session.add(grant)
                session.flush()  # Get the ID
                
                # Get assigned tags
                assigned_tags = self.tagging_service.assign_tags(
                    grant_data['grant_name'], 
                    grant_data['grant_description']
                )
                
                # Find and assign tags
                for tag_name in assigned_tags:
                    tag = session.query(Tag).filter(Tag.name == tag_name).first()
                    if tag:
                        grant.tags.append(tag)
                
                added_grants.append(grant.to_dict())
            
            session.commit()
            return {
                'success': True,
                'grants_added': added_grants,
                'message': f'Successfully added {len(added_grants)} grant(s)'
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding grants: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def get_all_grants(self):
        """Get all grants from the database"""
        session = self.Session()
        try:
            grants = session.query(Grant).all()
            return {
                'success': True,
                'grants': [grant.to_dict() for grant in grants]
            }
        except Exception as e:
            logging.error(f"Error getting grants: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def get_all_tags(self):
        """Get all available tags"""
        session = self.Session()
        try:
            tags = session.query(Tag).all()
            return {
                'success': True,
                'tags': [tag.name for tag in tags]
            }
        except Exception as e:
            logging.error(f"Error getting tags: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def search_grants_by_tags(self, search_tags):
        """Search grants by tags"""
        session = self.Session()
        try:
            if not search_tags:
                return self.get_all_grants()
            
            # Build query to find grants that have any of the specified tags
            grants = session.query(Grant).join(Grant.tags).filter(
                Tag.name.in_(search_tags)
            ).distinct().all()
            
            return {
                'success': True,
                'grants': [grant.to_dict() for grant in grants]
            }
        except Exception as e:
            logging.error(f"Error searching grants: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def get_grant_by_id(self, grant_id):
        """Get a specific grant by ID"""
        session = self.Session()
        try:
            grant = session.query(Grant).filter(Grant.id == grant_id).first()
            if grant:
                return {
                    'success': True,
                    'grant': grant.to_dict()
                }
            else:
                return {
                    'success': False,
                    'error': 'Grant not found'
                }
        except Exception as e:
            logging.error(f"Error getting grant: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def delete_grant(self, grant_id):
        """Delete a grant by ID"""
        session = self.Session()
        try:
            grant = session.query(Grant).filter(Grant.id == grant_id).first()
            if grant:
                session.delete(grant)
                session.commit()
                return {
                    'success': True,
                    'message': 'Grant deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Grant not found'
                }
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting grant: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()

