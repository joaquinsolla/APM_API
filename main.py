import json
import os
from typing import Union
from fastapi import FastAPI

app = FastAPI()


# DEFAULT
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


# CREATE NEW USER DATA FILE
# RETURNS: NEW USER DATA IF OK
@app.put("/new_user/{user_id}/{user_name}")
def create_user_data(user_id: str, user_name: str):
    try:
        new_file_path = os.path.join("data/users/", f"{user_id}.json")
        new_data = {
            "id": user_id,
            "name": user_name,
            "favorites": []
        }

        if not os.path.exists(new_file_path):
            with open(new_file_path, "w") as file:
                json.dump(new_data, file)
            return new_data
        else:
            return {}

    except Exception:
        return {}