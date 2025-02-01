import os
from typing import Optional

from dotenv import load_dotenv

from src.database.config_defs import DatabaseMainConfig
from src.database.database_pipeline import DatabasePipeline
from src.server_models import Post, SuccessResponse

load_dotenv()

print(f"Using config file: {os.getenv('DATABASE_CONFIG_FILE')}")

database_pipeline = DatabasePipeline.new_instance_from_config(
    DatabaseMainConfig.from_file(os.getenv("DATABASE_CONFIG_FILE"))
)


def get_sorted_posts_pipeline(
    sort_by: str = "created_at",
    order: str = "desc",
    author: Optional[str] = None
):
    posts = database_pipeline.get_post_all()

    if not posts:
        return SuccessResponse(data=[])

    if author:
        posts = [post for post in posts if getattr(post, "author", "").lower() == author.lower()]

    # Convert posts to dictionaries if they're not already
    posts_dict = [post.dict() if hasattr(post, 'dict') else post for post in posts]
    
    for post in posts_dict:
        if sort_by not in post:
            post[sort_by] = ""

    reverse = order == "desc"
    posts_dict.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)

    return SuccessResponse(data=posts_dict)

def get_post_by_id_pipeline(post_id: str):
    post = database_pipeline.get_post_by_id(post_id)
    return SuccessResponse(data=post)


def create_post_pipeline(post: Post):
    post = database_pipeline.create_post(post)
    return SuccessResponse(data=post)


def update_post_pipeline(post_id: str, post: Post):
    post = database_pipeline.update_post(post_id, post)
    return SuccessResponse(data=post)


def delete_post_pipeline(post_id: str):
    post = database_pipeline.delete_post(post_id)
    return SuccessResponse(data=post)


def get_post_stats_pipeline(post_id: str):
    post_stats = database_pipeline.get_post_stats(post_id)
    return SuccessResponse(data=post_stats)

def get_posts_by_author_pipeline(author: str):
    posts = database_pipeline.get_posts_by_author(author)
    return SuccessResponse(data=posts)
