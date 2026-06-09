"""Service for booking intent detection and extraction."""
import json
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.db_models import Booking
from app.models.schemas import BookingData
from app.services.llm_service import call_groq_api


# Keywords for booking intent detection
BOOKING_KEYWORDS = ["book", "schedule", "interview", "appointment", "available", "meeting", "slot"]


def detect_booking_intent(user_message: str) -> bool:
    """Check if user message contains booking-related keywords."""
    message_lower = user_message.lower()
    return any(keyword in message_lower for keyword in BOOKING_KEYWORDS)


def extract_booking_info(conversation_messages: List[dict]) -> Optional[BookingData]:
    """Extract booking information using Groq API."""
    
    # Build conversation context (last 4 messages + current)
    conversation_text = ""
    for msg in conversation_messages[-5:]:  # Last 5 messages including current
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            conversation_text += f"User: {content}\n"
        elif role == "assistant":
            conversation_text += f"Assistant: {content}\n"
    
    # Extraction prompt
    extraction_prompt = f"""Extract the following fields from this conversation if present: name, email, date, time. Return as JSON only, no explanation. If a field is missing return null for that field.

Conversation:
{conversation_text}

Return only valid JSON in this exact format:
{{"name": "value or null", "email": "value or null", "date": "value or null", "time": "value or null"}}"""
    
    try:
        # Call Groq API for extraction
        response = call_groq_api(extraction_prompt)
        
        # Parse JSON response
        # Clean response to extract JSON
        response_clean = response.strip()
        if "```json" in response_clean:
            response_clean = response_clean.split("```json")[1].split("```")[0].strip()
        elif "```" in response_clean:
            response_clean = response_clean.split("```")[1].split("```")[0].strip()
        
        booking_data = json.loads(response_clean)
        
        # Create BookingData object
        return BookingData(
            name=booking_data.get("name"),
            email=booking_data.get("email"),
            date=booking_data.get("date"),
            time=booking_data.get("time")
        )
    except Exception as e:
        # If extraction fails, return None
        print(f"Booking extraction error: {e}")
        return None


def save_booking(db: Session, session_id: str, booking_data: BookingData) -> str:
    """Save booking to SQLite database."""
    booking_id = str(uuid.uuid4())
    
    booking = Booking(
        booking_id=booking_id,
        session_id=session_id,
        name=booking_data.name,
        email=booking_data.email,
        date=booking_data.date,
        time=booking_data.time
    )
    
    db.add(booking)
    db.commit()
    
    return booking_id


def process_booking(db: Session, session_id: str, user_message: str, 
                   chat_history: List[dict]) -> Optional[BookingData]:
    """Process booking intent: detect, extract, and save."""
    
    # Check for booking intent
    if not detect_booking_intent(user_message):
        return None
    
    # Build conversation including current message
    conversation = chat_history + [{"role": "user", "content": user_message}]
    
    # Extract booking information
    booking_data = extract_booking_info(conversation)
    
    if booking_data:
        # Save to database
        save_booking(db, session_id, booking_data)
        return booking_data
    
    return None
