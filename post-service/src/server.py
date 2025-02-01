import asyncio

import uvicorn
from fastapi import FastAPI

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


@app.get("/posts")
@handle_exceptions
async def get_posts():
    return await asyncio.get_event_loop().run_in_executor(None, get_post_all_pipeline)


@app.get("/posts/{post_id}", response_model=SuccessResponse)
@handle_exceptions
async def get_post(post_id: str):
    return await asyncio.get_event_loop().run_in_executor(
        None, get_post_by_id_pipeline, post_id
    )


@app.post("/posts", response_model=SuccessResponse)
@handle_exceptions
async def create_post(post: Post):
    return await asyncio.get_event_loop().run_in_executor(
        None, create_post_pipeline, post
    )


@app.put("/posts/{post_id}", response_model=SuccessResponse)
@handle_exceptions
async def update_post(post_id: str, post: Post):
    return await asyncio.get_event_loop().run_in_executor(
        None, update_post_pipeline, post_id, post
    )


@app.delete("/posts/{post_id}", response_model=SuccessResponse)
@handle_exceptions
async def delete_post(post_id: str):
    return await asyncio.get_event_loop().run_in_executor(
        None, delete_post_pipeline, post_id
    )


@app.get("/posts/{post_id}/stats", response_model=SuccessResponse)
@handle_exceptions
async def get_post_stats(post_id: str):
    return await asyncio.get_event_loop().run_in_executor(
        None, get_post_stats_pipeline, post_id
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
