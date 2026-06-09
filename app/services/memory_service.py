"""Service for managing chat history in Redis."""
from typing import List
import json
from app.core.redis_client import get_redis_client


def get_chat_history(session_id: str, max_messages: int = 6) -> List[dict]:
    """Retrieve chat history for a session from Redis."""
    redis_client = get_redis_client()
    key = f"chat:{session_id}"
    
    # Get the last N messages
    messages_json = redis_client.lrange(key, -max_messages, -1)
    
    messages = []
    for msg_json in messages_json:
        messages.append(json.loads(msg_json))
    
    return messages


def add_message_to_history(session_id: str, role: str, content: str) -> None:
    """Add a message to chat history in Redis."""
    redis_client = get_redis_client()
    key = f"chat:{session_id}"
    
    message = {
        "role": role,
        "content": content
    }
    
    # Append message to list
    redis_client.rpush(key, json.dumps(message))
    
    # Set expiration to 24 hours (86400 seconds)
    redis_client.expire(key, 86400)


def save_conversation_turn(session_id: str, user_message: str, assistant_response: str) -> None:
    """Save both user message and assistant response to Redis."""
    add_message_to_history(session_id, "user", user_message)
    add_message_to_history(session_id, "assistant", assistant_response)
