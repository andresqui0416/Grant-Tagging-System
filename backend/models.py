from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for many-to-many relationship between grants and tags
grant_tags = Table(
    'grant_tags',
    Base.metadata,
    Column('grant_id', Integer, ForeignKey('grants.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Grant(Base):
    __tablename__ = 'grants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    grant_name = Column(String(255), nullable=False)
    grant_description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-many relationship with tags
    tags = relationship("Tag", secondary=grant_tags, back_populates="grants")
    
    def to_dict(self):
        """Convert grant to dictionary"""
        return {
            'id': self.id,
            'grant_name': self.grant_name,
            'grant_description': self.grant_description,
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with grants
    grants = relationship("Grant", secondary=grant_tags, back_populates="tags")
    
    def to_dict(self):
        """Convert tag to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
