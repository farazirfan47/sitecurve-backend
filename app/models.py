from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)   
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    landscapes = relationship("Landscape", back_populates="owner")

class Landscape(Base):
    __tablename__ = "landscapes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    keyword_s3 = Column(String, unique=True, nullable=True)
    first_loaded = Column(Boolean, default=False)
    # public, private, paid visibility options, default is public and should be a enum
    visibility = Column(Enum('public', 'private', 'paid', name='visibility_types'), default='public')

    owner = relationship("User", back_populates="landscapes")