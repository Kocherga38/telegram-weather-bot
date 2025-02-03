import logging
import redis.asyncio as aioredis

from app.config.redis import redis_settings as settings

logger = logging.getLogger(__name__)


async def get_redis():
    return await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True
    )


async def save_city_in_redis(user_id: int, city: str) -> None:
    redis = await get_redis()
    await redis.set(f"user:{user_id}:city", city)
    await redis.sadd("users", user_id)

    logger.info(f"Saved in Redis.\nUser id: {user_id}\nCity: {city}")
    await redis.aclose()


async def get_city(user_id: int) -> str:
    redis = await get_redis()
    city = await redis.get(f"user:{user_id}:city")
    if city is None:
        logger.error(f"No city found for user {user_id}.")
    await redis.aclose()
    return city


async def get_all_users() -> list:
    redis = await get_redis()
    users = await redis.smembers("users")
    await redis.aclose()

    return [int(user_id) for user_id in users]
