import asyncio
from typing import Optional

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.decorators import handle_exceptions
from src.main import *
from src.server_models import Post, SuccessResponse

app = FastAPI(
    title="Post Service",
    description="API for managing posts",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/post/list")
@handle_exceptions
async def get_posts(
    sort_by: Optional[str] = Query("created_at", enum=["created_at", "updated_at", "title", "author"]),
    order: Optional[str] = Query("desc", enum=["asc", "desc"]),
    author: Optional[str] = Query(None)
):
    return await asyncio.get_event_loop().run_in_executor(
        None, get_sorted_posts_pipeline, sort_by, order, author
    )

@app.post("/post/create", response_model=SuccessResponse)
@handle_exceptions
async def create_post(post: Post):
    return await asyncio.get_event_loop().run_in_executor(
        None, create_post_pipeline, post
    )


@app.put("/post/update/{post_id}", response_model=SuccessResponse)
@handle_exceptions
async def update_post(post_id: str, post: Post):
    return await asyncio.get_event_loop().run_in_executor(
        None, update_post_pipeline, post_id, post
    )


@app.delete("/post/delete/{post_id}", response_model=SuccessResponse)
@handle_exceptions
async def delete_post(post_id: str):
    return await asyncio.get_event_loop().run_in_executor(
        None, delete_post_pipeline, post_id
    )


@app.get("/post/stats/{post_id}", response_model=SuccessResponse)
@handle_exceptions
async def get_post_stats(post_id: str):
    return await asyncio.get_event_loop().run_in_executor(
        None, get_post_stats_pipeline, post_id
    )


@app.get("/post/get/{author}", response_model=SuccessResponse)
@handle_exceptions
async def get_posts_by_author(author: str):
    return await asyncio.get_event_loop().run_in_executor(
        None, get_posts_by_author_pipeline, author
    )


if __name__ == "__main__":
    if os.getenv("DOCKER_ENV") == "true":
        uvicorn.run(
            "src.server:app", host="0.0.0.0", port=8000, reload=False, workers=4
        )
    else:
        uvicorn.run(
            "src.server:app", host="localhost", port=8000, reload=True, workers=1
        )
