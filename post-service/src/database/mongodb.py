from typing import List, Optional

import pymongo
from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

from src.database.config_defs import DatabaseMainConfig
from src.database.database_protocol import DatabaseProtocol
from src.server_models import Post, PostStats


class MongoDB(DatabaseProtocol):
    def __init__(self, config: DatabaseMainConfig):
        self.client = MongoClient(config.mongo.database_url)
        self.db = self.client[config.mongo.database_name]
        self.posts_collection = self.db[config.mongo.posts_collection_name]
        self.stats_collection = self.db[config.mongo.stats_collection_name]

    def create_post(self, post: Post) -> Post:
        """Create a post in the database"""
        post_dict = post.model_dump()
        result = self.posts_collection.insert_one(post_dict)
        post_dict["_id"] = str(result.inserted_id)
        return Post(**post_dict)

    def get_post(self, post_id: str) -> Post:
        """Get a post from the database"""
        try:
            print(f"Fetching post with id: {post_id}")
            post_dict = self.posts_collection.find_one({"id": post_id})
            if post_dict:
                post_dict["_id"] = str(post_dict["_id"])
                return Post(**post_dict)
        except Exception as e:
            print(f"Error fetching post: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error fetching post: {str(e)}"
            )
        return None

    def get_post_all(self) -> List[Post]:
        """Get all posts from the database"""
        posts = []
        for post in self.posts_collection.find():
            post["_id"] = str(post["_id"])
            posts.append(Post(**post))
        return posts

    def update_post(self, post_id: str, post: Post) -> Post:
        """Update a post in the database"""
        post_dict = post.model_dump()
        self.posts_collection.update_one(
            {"_id": ObjectId(post_id)}, {"$set": post_dict}
        )
        return self.get_post(post_id)

    def delete_post(self, post_id: str) -> None:
        """Delete a post from the database"""
        self.posts_collection.delete_one({"_id": ObjectId(post_id)})

    def get_post_by_id(self, post_id: str) -> Post:
        """Get a post by id from the database"""
        return self.get_post(post_id)

    def get_post_by_user_id(self, user_id: str) -> List[Post]:
        posts = []
        for post in self.posts_collection.find({"user_id": user_id}):
            post["_id"] = str(post["_id"])
            posts.append(Post(**post))
        return posts

    def find_posts(self, user_id: Optional[str] = None, username: Optional[str] = None) -> List[Post]:

        query = {}

        # Add user_id filter if provided
        if user_id:
            query["user_id"] = user_id

        # Add username filter if provided
        if username:
            query["username"] = {"$regex": f"^{username}", "$options": "i"}  # Case-insensitive, partial match

        # Fetch posts from MongoDB
        posts = []
        for post in self.posts_collection.find(query):
            post["_id"] = str(post["_id"])  # Convert ObjectId to string
            posts.append(Post(**post))

        return posts

    def get_post_stats(self, post_id: str) -> PostStats:
        """Get post stats from the database"""
        stats = self.stats_collection.find_one({"post_id": post_id})
        if stats:
            stats["_id"] = str(stats["_id"])
            return PostStats(**stats)
        return None
    
    def get_posts_by_author(self, author: str) -> List[Post]:
        """Get all posts by author from the database"""
        posts = []
        for post in self.posts_collection.find({"author": author}):
            post["_id"] = str(post["_id"])
            posts.append(Post(**post))
        return posts
