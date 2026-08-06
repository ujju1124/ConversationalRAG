"""Tests for booking detection and extraction."""
import pytest
from unittest.mock import Mock, patch
from app.services.booking_service import (
    detect_booking_intent,
    extract_booking_info,
    process_booking
)
from app.models.schemas import BookingData


def test_detect_booking_intent_positive():
    """Test that booking keywords are detected."""
    assert detect_booking_intent("I want to book an interview") == True
    assert detect_booking_intent("Can I schedule a meeting?") == True
    assert detect_booking_intent("What appointment slots are available?") == True


def test_detect_booking_intent_negative():
    """Test that non-booking messages are not detected."""
    assert detect_booking_intent("What is machine learning?") == False
    assert detect_booking_intent("Tell me about AI") == False


def test_extract_booking_with_all_fields(mock_groq):
    """Test booking extraction when all fields are present."""
    # Mock Groq to return booking data
    mock_groq.chat.completions.create.return_value.choices[0].message.content = '''{
        "name": "John Doe",
        "email": "john@example.com",
        "date": "2024-03-15",
        "time": "2:00 PM"
    }'''
    
    conversation = [
        {"role": "user", "content": "I want to book an interview"},
        {"role": "assistant", "content": "Sure, what's your name?"},
        {"role": "user", "content": "John Doe, john@example.com, March 15th at 2 PM"}
    ]
    
    result = extract_booking_info(conversation)
    
    assert result is not None
    assert result.name == "John Doe"
    assert result.email == "john@example.com"
    assert result.date == "2024-03-15"
    assert result.time == "2:00 PM"


def test_extract_booking_with_partial_fields(mock_groq):
    """Test booking extraction with only some fields present."""
    mock_groq.chat.completions.create.return_value.choices[0].message.content = '''{
        "name": "Jane Smith",
        "email": null,
        "date": "2024-03-20",
        "time": null
    }'''
    
    conversation = [
        {"role": "user", "content": "I'm Jane Smith and I want to book for March 20th"}
    ]
    
    result = extract_booking_info(conversation)
    
    assert result is not None
    assert result.name == "Jane Smith"
    assert result.email is None
    assert result.date == "2024-03-20"


def test_extract_booking_all_null_returns_none(mock_groq):
    """Test that all null fields returns None."""
    mock_groq.chat.completions.create.return_value.choices[0].message.content = '''{
        "name": null,
        "email": null,
        "date": null,
        "time": null
    }'''
    
    conversation = [{"role": "user", "content": "What's the weather?"}]
    
    result = extract_booking_info(conversation)
    
    assert result is None


def test_booking_without_keywords_returns_none():
    """Test that process_booking returns None when no booking keywords detected."""
    from unittest.mock import Mock as MockDB
    
    db = MockDB()
    result = process_booking(
        db=db,
        session_id="test",
        user_message="What is AI?",
        chat_history=[]
    )
    
    assert result is None


def test_email_validation():
    """Test that invalid emails are rejected by Pydantic."""
    # Valid email should work
    booking = BookingData(email="valid@example.com")
    assert booking.email == "valid@example.com"
    
    # Invalid email should raise validation error
    with pytest.raises(Exception):  # Pydantic ValidationError
        BookingData(email="invalid-email")
