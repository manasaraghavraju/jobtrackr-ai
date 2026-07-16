import json
import logging
import os
from typing import Any, Optional

import redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


def get_cached_json(key: str) -> Optional[Any]:
    """Return decoded cached JSON, or None on a miss/failure."""
    try:
        cached_value = redis_client.get(key)

        if cached_value is None:
            logger.info({
                "message": "Redis cache miss",
                "cacheKey": key,
            })
            return None

        logger.info({
            "message": "Redis cache hit",
            "cacheKey": key,
        })

        return json.loads(cached_value)

    except (RedisError, json.JSONDecodeError):
        logger.exception("Unable to read from Redis")
        return None


def set_cached_json(
    key: str,
    value: Any,
    ttl_seconds: int = CACHE_TTL_SECONDS,
) -> None:
    """Store JSON with an expiration time. Cache failures do not break the API."""
    try:
        redis_client.set(
            name=key,
            value=json.dumps(value),
            ex=ttl_seconds,
        )

        logger.info({
            "message": "Redis value cached",
            "cacheKey": key,
            "ttlSeconds": ttl_seconds,
        })

    except RedisError:
        logger.exception("Unable to write to Redis")


def delete_cached_value(key: str) -> None:
    """Invalidate one cache key."""
    try:
        redis_client.delete(key)

        logger.info({
            "message": "Redis cache invalidated",
            "cacheKey": key,
        })

    except RedisError:
        logger.exception("Unable to invalidate Redis cache")