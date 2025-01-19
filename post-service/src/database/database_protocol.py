from typing import List, Protocol

from src.server_models import Post, PostStats


class DatabaseProtocol(Protocol):

    def create_post(self, post: Post) -> Post:
        pass

    def get_post(self, post_id: str) -> Post:
        pass

    def get_post_all(self) -> List[Post]:
        pass

    def update_post(self, post_id: str, post: Post) -> Post:
        pass

    def delete_post(self, post_id: str) -> None:
        pass

    def get_post_by_id(self, post_id: str) -> Post:
        pass

    def get_post_by_user_id(self, user_id: str) -> List[Post]:
        pass

    def get_post_stats(self, post_id: str) -> PostStats:
        pass
