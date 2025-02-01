import os

from dotenv import load_dotenv
from pymongo import ASCENDING, DESCENDING

from src.database.config_defs import DatabaseMainConfig
from src.database.database_pipeline import DatabasePipeline
from src.server_models import Post, SuccessResponse

load_dotenv()

print(f"Using config file: {os.getenv('DATABASE_CONFIG_FILE')}")

database_pipeline = DatabasePipeline.new_instance_from_config(
    DatabaseMainConfig.from_file(os.getenv("DATABASE_CONFIG_FILE"))
)


def get_sorted_posts_pipeline(sort_by: str = "created_at", order: str = "desc", page: int = 1, page_size: int = 10):

    posts = database_pipeline.get_post_all()

    # Return an empty list if there are no posts available
    if not posts:
        return SuccessResponse(data=[])

    # Ensure every post includes the sort field; assign a default empty string if missing
    for post in posts:
        post.setdefault(sort_by, "")

    # Determine sorting order and sort the posts accordingly
    reverse_order = (order.lower() == "desc")
    posts.sort(key=lambda post: post.get(sort_by, ""), reverse=reverse_order)

    # Calculate pagination boundaries and slice the list
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_posts = posts[start_index:end_index]
    return SuccessResponse(data=paginated_posts)

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
