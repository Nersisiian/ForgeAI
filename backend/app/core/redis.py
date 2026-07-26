import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(str(settings.REDIS_URL), decode_responses=True)