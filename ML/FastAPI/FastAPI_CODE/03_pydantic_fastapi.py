# python file_name.py
# uvicorn file_name:app --reload --port 8000
# # uvicorn 03_pydantic_fastapi:app --reload
# http://localhost:8000/docs


### Validation Requests Bodies with Pydantic

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

FAKE_ITEMS_DB = {
    1: {"name": "keyboard", "price": 49.99},
    2: {"name": "monitor", "price": 199.99},
    10: {"name": "keyboard_expensive", "price": 499.99},
    4: {"name": "keyrings", "price": 0.99}
}

class Item(BaseModel):
    name : str = "None"
    price : float = 0

@app.get("/searchv2")
def search_items(q : str | None = None, limit : int = 10):
    # q = 'a'
    if q is None :
         return {"query" : None, "limit" : limit, "results" : list(FAKE_ITEMS_DB.values())[:limit]}
    else :
        matches = [item for item in FAKE_ITEMS_DB.values() if q.lower() in item["name"]]
        return {"query" : q, "limit" : limit, "results" : matches[:limit]}
    
# Post endpoint : Add data in FAKE_ITEMS_DB
@app.post("/items", status_code=201)
def create_item(item : Item):
    new_id = max(FAKE_ITEMS_DB.keys()) + 1
    input_ = {"name" : item.name, "price" : item.price}
    FAKE_ITEMS_DB[new_id] = input_
    return {"id" : new_id, **input_}
# curl -X POST "http://localhost:8000/items" -H "Content-Type: application/json" -d "{\"name\" : \"microphone\", \"price\" : 390.10}"


if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)