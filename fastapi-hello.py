import uvicorn
from fastapi import FastAPI

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

if __name__ == "__main__":
    uvicorn.run("fastapi-hello:app", host="0.0.0.0", port=8000, reload=True)
