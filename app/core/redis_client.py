"""Redis client for chat memory using Upstash."""
import redis
from app.core.config import settings

# Parse the Redis URL
redis_url = settings.UPSTASH_REDIS_URL

# Initialize Redis client
# For Upstash (rediss://), pass password token
# For local Redis (redis://), omit password if token is None
redis_kwargs = {
    "url": redis_url,
    "decode_responses": True
}

# Only add password if token is provided (for Upstash)
if settings.UPSTASH_REDIS_TOKEN:
    redis_kwargs["password"] = settings.UPSTASH_REDIS_TOKEN

redis_client = redis.from_url(**redis_kwargs)


def get_redis_client():
    """Get Redis client instance."""
    return redis_client
