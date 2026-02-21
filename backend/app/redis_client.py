"""Redis connection and utilities"""
import redis
import json
from app.config import settings
from typing import Any, Optional


# Create Redis client
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def get_redis():
    """Get Redis client"""
    return redis_client


def cache_get(key: str) -> Optional[Any]:
    """Get cached value"""
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None


def cache_set(key: str, value: Any, ttl: int = 3600):
    """Set cached value"""
    redis_client.setex(key, ttl, json.dumps(value))


def cache_delete(key: str):
    """Delete cached value"""
    redis_client.delete(key)


def cache_clear_pattern(pattern: str):
    """Clear all keys matching pattern"""
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
