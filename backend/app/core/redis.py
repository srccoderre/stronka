"""Redis configuration and client."""
from typing import Optional
from redis import asyncio as aioredis
from app.core.config import settings


class RedisClient:
    """Redis client wrapper."""
    
    _client: Optional[aioredis.Redis] = None
    
    @classmethod
    async def get_client(cls) -> aioredis.Redis:
        """
        Get Redis client instance.
        
        Returns:
            Redis client
        """
        if cls._client is None:
            cls._client = await aioredis.from_url(
                str(settings.REDIS_URL),
                encoding="utf-8",
                decode_responses=True,
                max_connections=10,
            )
        return cls._client
    
    @classmethod
    async def close(cls) -> None:
        """Close Redis connection."""
        if cls._client:
            await cls._client.close()
            cls._client = None


async def get_redis() -> aioredis.Redis:
    """
    Dependency for getting Redis client.
    
    Returns:
        Redis client
    """
    return await RedisClient.get_client()
