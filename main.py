import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# DEFAULT
@app.get("/")
def read_root():
    return {"APM": "API"}


# GET ALL PARKING SLOTS
# RETURNS: { "plazas:" List [ slots {} ] }
@app.get("/get/plazas")
def get_all_slots():
    try:
        with open("data/parking_formatted.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception:
        return {}


# GET ALL FAVORITE PARKING SLOTS OF USER ID
# RETURNS: List [ slots {} ]
@app.get("/get/plazas/{user_id}")
def get_user_favorites(user_id: str):
    try:
        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

        with open("data/parking_formatted.json", "r", encoding="utf-8") as file:
            slots_data = json.load(file)

        fav_ids = user_data["favorites"]
        fav_slots = [plaza for plaza in slots_data["plazas"] if plaza["id"] in fav_ids]

        return {"plazas": fav_slots}
    except Exception:
        return {}


# CREATE NEW USER DATA FILE
# RETURNS: NEW USER DATA IF OK
@app.put("/put/new_user/{user_id}/{user_email}/{password}")
def create_user_data(user_id: str, user_email: str, password: str):
    try:
        new_file_path = os.path.join("data/users/", f"{user_id}.json")
        new_data = {
            "id": user_id,
            "email": user_email,
            "favorites": [],
            "password": password
        }

        if not os.path.exists(new_file_path):
            with open(new_file_path, "w") as file:
                json.dump(new_data, file)
            return new_data
        else:
            return {}

    except Exception:
        return {}


# ADD SLOT TO USER FAVORITES
# RETURNS: NEW USER DATA
@app.put("/put/user/{user_id}/add_favorite/{slot_id}")
def add_user_favorite(user_id: str, slot_id: int):
    try:

        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

        if slot_id not in user_data["favorites"]:
            user_data["favorites"].append(slot_id)

            with open(f"data/users/{user_id}.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file)

            return user_data

        else:
            return {"id": "", "email": "", "favorites": [], "password": ""}

    except Exception:
        return {}


# REMOVE SLOT FROM USER FAVORITES
# RETURNS: NEW USER DATA
@app.put("/put/user/{user_id}/remove_favorite/{slot_id}")
def remove_user_favorite(user_id: str, slot_id: int):
    try:

        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

        if slot_id in user_data["favorites"]:
            user_data["favorites"].remove(slot_id)

            with open(f"data/users/{user_id}.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file)

            return user_data

        else:
            return {"id": "", "email": "", "favorites": [], "password": ""}

    except Exception:
        return {}


# EDIT USER ACCOUNT INFO
# RETURNS: NEW USER DATA
@app.put("/put/user/{user_id}/edit_info/{new_email}")
def edit_user_info(user_id: str, new_email: str):
    try:

        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

        user_data["email"] = new_email

        with open(f"data/users/{user_id}.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file)

        return user_data

    except Exception:
        return {}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/post/login")
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    print("LOGIN")
    print(f"Recibido username: {username}, password: {password}")

    try:
        with open(f"data/users/{username}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)

            # Verificar si la contraseña coincide
            if user_data.get("password") == password:
                return {"message": "Login exitoso"}
            else:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")