from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any
from bson.objectid import ObjectId

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str = Field(default="")
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    author: str = Field(default="")

class PostStats(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    likes: int = Field(default=0)
    comments: int = Field(default=0)
    views: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

class SuccessResponse(BaseModel):
    success: bool = Field(default=True)
    reasonPhrase: str = Field(default="")
    statusCode: int = Field(default=200)
    data: Any = Field(default=None)

