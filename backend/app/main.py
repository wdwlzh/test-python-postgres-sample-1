from fastapi import FastAPI

app = FastAPI(title="My FastAPI App", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
