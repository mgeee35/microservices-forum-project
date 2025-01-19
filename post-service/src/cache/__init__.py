import os

from .redis_cache import RedisCache

cache = RedisCache(
    host="redis" if os.getenv("DOCKER_ENV") == "true" else "localhost", port=6379
)
