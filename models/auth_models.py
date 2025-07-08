from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)  # index for performance
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)  # store hashed password
    created_at = Column(DateTime, default=datetime.utcnow)
    email_verified = Column(Boolean, default=False)
    version = Column(Integer, default=1)