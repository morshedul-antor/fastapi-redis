from typing import AsyncIterator
import aioredis


async def get_redis_pool() -> AsyncIterator[aioredis.Redis]:
    redis = aioredis.from_url(
        "redis://localhost:6379/0",
        decode_responses=True
    )
    try:
        yield redis
    finally:
        await redis.close()
