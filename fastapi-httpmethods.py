import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime
from pydantic import BaseModel

v1 = APIRouter(prefix="/v1", tags=["v1"])

app = FastAPI(
    title="My First FastAPI",
    description="A beginner tutorial covering core FastAPI concepts.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    """Welcome message."""
    return {"message": "Welcome to FastAPI!", "docs": "/docs"}

@app.get("/greet/{name}")
def greet(name: str, loud: bool = False):
    """
    Path param:  /greet/Alice
    Query param: /greet/Alice?loud=true
    """
    msg = f"Hello, {name.upper()}!" if loud else f"Hello, {name}!"
    return {"message": msg}

db: dict[int, dict] = {
    1: {
        "id": 1, "name": "Laptop", "price": 999.99, "stock": 10,
        "category": "electronics", "in_stock": True,
        "description": "A powerful laptop", "created_at": datetime.utcnow(),
    },
    2: {
        "id": 2, "name": "Mouse", "price": 29.99, "stock": 0,
        "category": "accessories", "in_stock": False,
        "description": None, "created_at": datetime.utcnow(),
    },
}

next_id = 3

# =========================
# GET – Read Data
# =========================

@app.get("/items/")  # list all
def list_items():
    return list(db.values())

@app.get("/items/{item_id}")  # get one
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return db[item_id]

# # Query params: /items/?skip=0&limit=5
# @app.get("/items/")
# def list_items(skip: int = 0, limit: int = 10):
#     items = list(db.values())
#     return items[skip: skip + limit]

class ItemResponse(BaseModel):
    id:         int
    name:       str
    price:      float
    stock:      int
    category:   Optional[str]
    in_stock:   bool
    description: Optional[str]
    created_at: datetime

class ItemListResponse(BaseModel):
    itemList: list[ItemResponse]

@app.get("/items/",
         response_model=ItemListResponse,
         summary="List all items",
         )
def list_items(skip: int = 0, limit: int = 10):
    items = list(db.values())
    return {"itemList": items[skip: skip + limit]}

# =========================
# POST – Create Data
# =========================

from pydantic import BaseModel, Field

class Item(BaseModel):
    id: int | None = None
    name: str
    price: float
    stock: int = 0
    category: str | None = None
    in_stock: bool = True
    description: str | None = None
    created_at: datetime = datetime.utcnow()

@v1.post("/items/", status_code=201, summary="Create a new item")
def create_item(item: Item):
    global next_id
    db[next_id] = item
    item.id = next_id
    next_id += 1
    return {**item.model_dump()}

class ItemRequest(BaseModel):
    id:         Optional[int] = Field(None, examples=[123])
    name:       str = Field(..., min_length=1, max_length=100,
                            description="Product name",
                            examples=["Laptop"])
    price:      float = Field(..., gt=0,
                              description="Price must be > 0",
                              examples=[999.99])
    stock:      int = Field(default=0, ge=0,
                            description="Stock quantity")
    category:   Optional[str] = Field(None, examples=["electronics"])
    in_stock:   bool = Field(default=True)
    description: Optional[str] = Field(None, max_length=300)


@app.post("/items/",response_model=ItemResponse, status_code=201, summary="Create a new item")
def create_item(item: ItemRequest):
    global next_id
    record = {**item.model_dump(), "created_at": datetime.utcnow()}
    
    if not record['id']:
        record['id'] = next_id
        next_id += 1
    
    db[next_id] = record

    return record


# =========================
# PUT – Replace Data (full replacement)
# =========================

class Item(BaseModel):
    id: int | None = None
    name: str
    price: float
    stock: int = 0
    category: str | None = None
    in_stock: bool = True
    description: str | None = None
    created_at: datetime = datetime.utcnow()

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    item.id = item_id
    db[item_id] = item
    return {**item.model_dump()}

# =========================
# PATCH – Partially Update Data
# =========================

from typing import Optional

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

@app.patch("/items/{item_id}")
def patch_item(item_id: int, updates: ItemUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    existing = db[item_id]
    patch_data = updates.model_dump(exclude_unset=True)  # only fields the client sent
    updated = {**existing, **patch_data}

    db[item_id] = updated
    return updated

# =========================
# DELETE - Remove Data
# =========================

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Hard delete — permanently removes the item
    """
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    db.pop(item_id)
    return {"message": f"Item {item_id} deleted"}


@app.delete("/items/{item_id}/soft")
def soft_delete_item(item_id: int):
    """
    Soft delete — marks item as out-of-stock instead of removing it.
    Useful when you want to preserve data history.
    """
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    db[item_id]["in_stock"] = False
    db[item_id]["stock"] = 0
    return {"message": f"Item {item_id} deactivated"}

# =========================
# ASYNC – For I/O-bound operations
# =========================
import asyncio
import httpx
from fastapi import Query

# Async -- best for DB calls, HTTP requests, file I/O
@app.get("/async-example", summary="Async endpoint example")
async def async_endpoint():
    await asyncio.sleep(1)
    return {"type": "async", "note": "Awaited a 1-second I/O operation"}

# Calling an external API asynchronously
@app.get("/timezone", summary="Get timezones matching a specific offset (async)")
async def get_timezone(
    offset: Optional[str] = Query(
        default="",
        description="UTC offset in military style, e.g. +0700, -0500, +0000"
    ),
):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                f"https://aisenseapi.com/services/v1/timezones/{offset}",
                timeout=5
            )
            res.raise_for_status()
            data = res.json()
            return data
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Timezone service error: {str(e)}")

app.include_router(v1)

if __name__ == "__main__":
    uvicorn.run("fastapi-httpmethods:app", host="0.0.0.0", port=8000, reload=True)