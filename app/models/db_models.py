"""SQLAlchemy database models for documents and bookings."""
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.core.db import Base


class Document(Base):
    """Document metadata table."""
    __tablename__ = "documents"
    
    document_id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer, nullable=False)
    strategy = Column(String, nullable=False)


class Booking(Base):
    """Interview booking table."""
    __tablename__ = "bookings"
    
    booking_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
