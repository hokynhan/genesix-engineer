import uvicorn
from fastapi import FastAPI
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


app = FastAPI(
    title="Assignment 06/03/2026 FastAPI",
    description="All Five Endpoints at a Glance",
    version="1.0.0",
)

@app.get("/")
def read_root():
    """Welcome message."""
    return {"message": "Welcome to Assignment 06/03/2026 FastAPI!", "docs": "/docs"}


# =========================
# ASYNC – For I/O-bound operations
# =========================
import asyncio
import json
from fastapi import Query, HTTPException
import aiofiles
import os

# Path to the articles.json file
ARTICLES_FILE = os.path.join(os.path.dirname(__file__), "articles.json")

async def load_articles():
    try:
        async with aiofiles.open(ARTICLES_FILE, mode='r') as file:
            content = await file.read()
            articles = json.loads(content)
            return articles
    except Exception:
        return []

async def save_articles(articles: list[dict]):
    async with aiofiles.open(ARTICLES_FILE, mode='w') as file:
        await file.write(json.dumps(articles, indent=2))


# =========================
# GET – Read Data
# =========================
class ItemGetRequest(BaseModel):
    skip: Optional[int] = None
    limit: Optional[int] = None

class ArticleGetResponse(BaseModel):
    code: str
    title: str
    author: str
    published_date: date
    version: str
    created_at: datetime

class ArticleGetListResponse(BaseModel):
    itemList: list[ArticleGetResponse]

@app.get("/articles/",
         response_model=ArticleGetListResponse,
         summary="List all articles",
         )

# async def list_articles(
#     ):
#     articles = await load_articles()
#     return {"itemList": articles}

async def list_articles(
    skip: int = Query(default=0, description="Number of items to skip"),
    limit: int = Query(default=10, description="Maximum number of items to return")
    ):
    articles = await load_articles()
    return {"itemList": articles[skip: skip + limit]}



if __name__ == "__main__":
    uvicorn.run("fastapi-test:app", host="0.0.0.0", port=8000, reload=True)