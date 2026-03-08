import uvicorn
from fastapi import FastAPI
from datetime import datetime
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

@app.get("/sum/",summary="Sum two numbers")
def sum_two_numbers(num1: int, num2: int):
    return {"sum is": num1 + num2}

@app.get("/factorial/{number}",summary="Compute n!")
def get_factorial(number: int):
    def compute_factorial(n):
        if n == 0:
            return 1
        else:
            return n * compute_factorial(n - 1)
    return {"factorial is": compute_factorial(number)}


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
    published_date: datetime
    version: float
    created_at: datetime

class ArticleGetListResponse(BaseModel):
    itemList: list[ArticleGetResponse]

@app.get("/articles/",
         response_model=ArticleGetListResponse,
         summary="List all articles",
         )
async def list_articles(
    skip: int = Query(default=0, description="Number of items to skip"),
    limit: int = Query(default=10, description="Maximum number of items to return")
    ):
    articles = await load_articles()
    return {"itemList": articles[skip: skip + limit]}

# =========================
# PATCH – Partially Update Data
# =========================

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    version: Optional[float] = None


@app.patch("/articles/{code}",
            # response_model=ArticlePostResponse,
            summary="Edit by code",
         )

async def patch_item(
    article_code: str = Query(
        default="",
        description="Code format, e.g. ART-001, ART-002, etc.",
    ),
    updates: ItemUpdate = None):

    articles = await load_articles()

    # locate the item and its index
    codes = [article["code"] for article in articles]
    if article_code not in codes:
        raise HTTPException(status_code=404, detail=f"Item {article_code} not found")

    idx = codes.index(article_code)
    existing_article = articles[idx]

    # merge only provided fields
    patch_data = updates.model_dump(exclude_unset=True)
    updated_article = {**existing_article, **patch_data}

    # replace in list and persist back to file
    articles[idx] = updated_article
    await save_articles(articles)

    return updated_article

# =========================
# POST – Create Data
# =========================

from typing import Optional
from pydantic import Field

class ArticlePostResponse(BaseModel):
    code: str
    title: str
    author: str
    published_date: datetime
    version: float
    created_at: datetime=datetime.utcnow()

class ArticlePostRequest(BaseModel):
    code:       str = Field(..., min_length=7, max_length=20,
                            description="code format API-xxx",
                            examples=["API-001"])
    title:      str = Field(..., max_length=200, 
                            description="Title of the article",
                            examples=["Understanding Pydantic"])
    author:     str = Field(..., max_length=100,
                            description="Author's name",
                            examples=["Alice Johnson"])
    published_date: Optional[datetime] = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$",
                                description="Published date in YYYY-MM-DD format",
                                examples=["2024-03-15"])
    version:    float = Field(default=1.0, ge=1.0,
                            description="Version of the article")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp, auto-set by server")

@app.post("/articles/",response_model=ArticlePostResponse, status_code=201, summary="Create a new article")
def create_article(article: ArticlePostRequest):
    articles = load_articles()

    if article.code in [existing["code"] for existing in articles]:
        raise HTTPException(status_code=400, detail=f"Article with code {article.code} already exists")

    new_article = article.model_dump()
    new_article["created_at"] = datetime.utcnow().isoformat()
    articles.append(new_article)
    save_articles(articles)

    return new_article

# @app.post("/articles/",
#           summary="Create a new article",
#           )
# async def create_article(article: ArticlePostRequest):
#     articles = await load_articles()

#     if article.code in [existing["code"] for existing in articles]:
#         raise HTTPException(status_code=400, detail=f"Article with code {article.code} already exists")

#     articles.append(article.dict())
#     await save_articles(articles)

#     return article

if __name__ == "__main__":
    uvicorn.run("fastapi-assignment260307:app", host="0.0.0.0", port=8000, reload=True)