from redis.asyncio import Redis

from src.config.config import settings

redis = Redis.from_url(
    settings.redis_url,
    # automatically converts bytes into strings.
    decode_responses=True
)