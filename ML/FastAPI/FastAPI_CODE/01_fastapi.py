# Python version required : 3.10 or newer
# pip install fastapi uvicorn
# python 01_fastapi.py
# uvicorn 01_fastapi:app --reload --port 8000
# # uvicorn 01_fastapi:app --reload

from fastapi import FastAPI

app = FastAPI() # app is the central object of a fastapi.

# route (also called as "endpoint" or "path operation")
@app.get("/")
def read_root():
    return {"message" : "Hello! This is my first API."}
# http://127.0.0.1:8000 --> process --> http://127.0.0.1:8000/

@app.get("/say_hello")
def say_hello_python():
    return {"message" : "Hello from UDS 2.0"}

@app.get("/say_hello/{name}")
def say_hello_python(name : str):
    return {"message" : f"Hello {name} from UDS 2.0"}


if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)