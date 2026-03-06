import uvicorn
from fastapi import FastAPI, HTTPException
from datetime import datetime

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

# Query params: /items/?skip=0&limit=5
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    items = list(db.values())
    return items[skip: skip + limit]


# =========================
# POST – Create Data
# =========================

from pydantic import BaseModel

class Item(BaseModel):
    id: int | None = None
    name: str
    price: float
    stock: int = 0
    category: str | None = None
    in_stock: bool = True
    description: str | None = None
    created_at: datetime = datetime.utcnow()

@app.post("/items/", status_code=201, summary="Create a new item")
def create_item(item: Item):
    global next_id
    db[next_id] = item
    item.id = next_id
    next_id += 1
    return {**item.model_dump()}


# =========================
# PUT – Replace Data (full replacement)
# =========================

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

if __name__ == "__main__":
    uvicorn.run("fastapi-httpmethods:app", host="0.0.0.0", port=8000, reload=True)