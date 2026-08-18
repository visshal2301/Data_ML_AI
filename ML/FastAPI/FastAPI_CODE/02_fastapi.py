# python file_name.py
# uvicorn file_name:app --reload --port 8000
# # uvicorn file_name:app --reload
# http://localhost:8000/docs

from fastapi import FastAPI, HTTPException

app = FastAPI()

FAKE_ITEMS_DB = {
    1: {"name": "keyboard", "price": 49.99},
    2: {"name": "monitor", "price": 199.99},
    10: {"name": "keyboard_expensive", "price": 499.99},
    4: {"name": "keyrings", "price": 0.99}
}

@app.get("/")
def read_root():
    return {"message" : "Hello! This is my Second API Tutorial."}

@app.get("/allitems")
def read_root():
    return FAKE_ITEMS_DB

# PATH PARAMETER
@app.get("/items/{item_id}")
def read_root(item_id):
    item_id = int(item_id)
    if item_id not in FAKE_ITEMS_DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return FAKE_ITEMS_DB[item_id]

# PATH PARAMETER, with automatic type conversion + Validation
@app.get("/itemsv2/{item_id}")
def read_root(item_id : int):
    if item_id not in FAKE_ITEMS_DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return FAKE_ITEMS_DB[item_id]

# Query Parameters
@app.get("/search")
def search_items(q : str, limit : int):
    if q is None and limit is None:
        raise HTTPException(status_code=404, detail="Need to pass Query parameters")
    else :
        matches = [item for item in FAKE_ITEMS_DB.values() if q.lower() in item["name"]]
        return {"query" : q, "limit" : limit, "results" : matches[:limit]}


# Query Parameters, optional with defaults
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
def create_item(item : dict):
    new_id = max(FAKE_ITEMS_DB.keys()) + 1
    FAKE_ITEMS_DB[new_id] = item
    return {"id" : new_id, **item}
# curl -X POST "http://localhost:8000/items" -H "Content-Type: application/json" -d "{\"name\" : \"microphone\", \"price\" : 390.10}"







if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)