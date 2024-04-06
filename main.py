import json
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"APM": "API"}


# GET ALL PARKING SLOTS
# RETURNS: { "plazas:" List [ slots {} ] }
@app.get("/plazas")
def get_all_slots():
    try:
        with open("data/parking_formatted.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception:
        return {}


# GET ALL FAVORITE PARKING SLOTS OF USER ID
# RETURNS: List [ slots {} ]
@app.get("/plazas/{user_id}")
def get_user_favorites(user_id: str):
    try:
        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

        with open("data/parking_formatted.json", "r", encoding="utf-8") as file:
            slots_data = json.load(file)

        fav_ids = user_data["favorites"]
        fav_slots = [plaza for plaza in slots_data["plazas"] if plaza["id"] in fav_ids]

        return fav_slots
    except Exception:
        return {}





@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}