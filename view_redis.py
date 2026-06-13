"""Script to view chat history stored in Redis."""
import redis
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def view_redis_data():
    """Display chat history from Redis."""
    
    # Connect to Redis
    redis_url = os.getenv('UPSTASH_REDIS_URL')
    redis_token = os.getenv('UPSTASH_REDIS_TOKEN')
    
    client = redis.from_url(
        url=redis_url,
        password=redis_token,
        decode_responses=True
    )
    
    print("=" * 80)
    print("💬 REDIS CHAT HISTORY")
    print("=" * 80)
    
    # Get all keys
    keys = client.keys('chat:*')
    
    if keys:
        print(f"\nFound {len(keys)} session(s):\n")
        
        for key in keys:
            session_id = key.replace('chat:', '')
            print(f"\n📝 Session: {session_id}")
            print("-" * 80)
            
            # Get all messages for this session
            messages = client.lrange(key, 0, -1)
            
            print(f"  Messages: {len(messages)}\n")
            
            for i, msg_json in enumerate(messages, 1):
                msg = json.loads(msg_json)
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                
                emoji = "👤" if role == "user" else "🤖"
                print(f"  {i}. {emoji} {role.upper()}:")
                print(f"     {content}\n")
            
            print("-" * 80)
    else:
        print("\n  No chat sessions found.\n")
    
    client.close()
    print("\n✅ Redis check complete!\n")

if __name__ == "__main__":
    view_redis_data()
