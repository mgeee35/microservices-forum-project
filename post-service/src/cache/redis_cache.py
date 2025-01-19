import json
from datetime import datetime
from typing import Any, Optional

import redis

from src.server_models import Post, PostStats


class RedisCache:
    def __init__(self, host="localhost", port=6379, db=0, decode_responses=True):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=decode_responses
        )
        self.default_expiry = 3600  # 1 hour default cache expiry

    def _serialize_datetime(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    def _serialize_post(self, post: Post) -> str:
        return json.dumps(post.model_dump(), default=self._serialize_datetime)

    def _deserialize_post(self, post_data: str) -> Post:
        return Post(**json.loads(post_data))

    def _serialize_post_stats(self, stats: PostStats) -> str:
        return json.dumps(stats.model_dump(), default=self._serialize_datetime)

    def _deserialize_post_stats(self, stats_data: str) -> PostStats:
        return PostStats(**json.loads(stats_data))

    def get_post(self, post_id: str) -> Optional[Post]:
        """Retrieve a post from cache"""
        cached_post = self.redis_client.get(f"post:{post_id}")
        if cached_post:
            return self._deserialize_post(cached_post)
        return None

    def set_post(self, post: Post, expiry: int = None) -> None:
        """Store a post in cache"""
        if expiry is None:
            expiry = self.default_expiry
        self.redis_client.setex(f"post:{post.id}", expiry, self._serialize_post(post))

    def delete_post(self, post_id: str) -> None:
        """Remove a post from cache"""
        self.redis_client.delete(f"post:{post_id}")

    def get_post_stats(self, post_id: str) -> Optional[PostStats]:
        """Retrieve post stats from cache"""
        cached_stats = self.redis_client.get(f"stats:{post_id}")
        if cached_stats:
            return self._deserialize_post_stats(cached_stats)
        return None

    def set_post_stats(
        self, post_id: str, stats: PostStats, expiry: int = None
    ) -> None:
        """Store post stats in cache"""
        if expiry is None:
            expiry = self.default_expiry
        self.redis_client.setex(
            f"stats:{post_id}", expiry, self._serialize_post_stats(stats)
        )

    def delete_post_stats(self, post_id: str) -> None:
        """Remove post stats from cache"""
        self.redis_client.delete(f"stats:{post_id}")

    def clear_cache(self) -> None:
        """Clear all cache entries"""
        self.redis_client.flushdb()

    def get_all_posts(self) -> list[Post]:
        """Retrieve all cached posts"""
        posts = []
        for key in self.redis_client.keys("post:*"):
            post_data = self.redis_client.get(key)
            if post_data:
                posts.append(self._deserialize_post(post_data))
        return posts
