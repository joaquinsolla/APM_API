import json
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/plazas")
def read_item():
    with open("data/parking_formatted.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}