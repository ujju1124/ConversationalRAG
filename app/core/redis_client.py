"""Redis client for chat memory using Upstash."""
import redis
from app.core.config import settings

# Initialize Redis client for Upstash
redis_client = redis.Redis(
    host=settings.UPSTASH_REDIS_URL.replace("redis://", "").replace("rediss://", "").split(":")[0],
    port=int(settings.UPSTASH_REDIS_URL.split(":")[-1]) if ":" in settings.UPSTASH_REDIS_URL else 6379,
    password=settings.UPSTASH_REDIS_TOKEN,
    ssl=True,
    decode_responses=True
)


def get_redis_client():
    """Get Redis client instance."""
    return redis_client
