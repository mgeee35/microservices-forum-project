from typing import List

from src.database.database_protocol import DatabaseProtocol
from src.server_models import Post, PostStats

from .config_defs import DatabaseMainConfig, DatabaseTag


class DatabasePipeline(DatabaseProtocol):
    def __init__(self, database: DatabaseProtocol, config: DatabaseMainConfig):
        self.database = database
        self.config = config

    @staticmethod
    def new_instance_from_config(config: DatabaseMainConfig) -> DatabaseProtocol:
        """Create a new instance of the database pipeline from a config"""
        from src.database.mongodb import MongoDB

        if config.database.database_tag == DatabaseTag.MONGODB:
            return MongoDB(config)
        else:
            raise ValueError(f"Invalid database tag: {config.database.database_tag}")

    def create_post(self, post: Post) -> Post:
        """Create a post in the database"""
        return self.database.create_post(post)

    def get_post(self, post_id: str) -> Post:
        """Get a post from the database"""
        return self.database.get_post(post_id)

    def get_post_all(self) -> List[Post]:
        """Get all posts from the database"""
        return self.database.get_post_all()

    def update_post(self, post_id: str, post: Post) -> Post:
        """Update a post in the database"""
        return self.database.update_post(post_id, post)

    def delete_post(self, post_id: str) -> None:
        """Delete a post from the database"""
        return self.database.delete_post(post_id)

    def get_post_by_id(self, post_id: str) -> Post:
        """Get a post by id from the database"""
        return self.database.get_post_by_id(post_id)

    def get_post_by_user_id(self, user_id: str) -> List[Post]:
        """Get all posts by user id from the database"""
        return self.database.get_post_by_user_id(user_id)

    def get_post_stats(self, post_id: str) -> PostStats:
        """Get post stats from the database"""
        return self.database.get_post_stats(post_id)
