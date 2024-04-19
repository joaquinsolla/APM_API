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

# GET USER DATA
@app.get("/get/{user_id}")
def get_user_data(user_id: str):
    try:
        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)
            print(user_data)

        return user_data
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


class PasswordChangeRequest(BaseModel):
    username: str
    email: str
    password: str

# CHANGE USER PASSWORD
@app.put("/put/user/change_password")
def change_password(request: PasswordChangeRequest):
    try:
        user_file_path = f"data/users/{request.username}.json"
        if os.path.exists(user_file_path):
            with open(user_file_path, "r", encoding="utf-8") as file:
                user_data = json.load(file)
            
                if user_data["email"] == request.email:
                    user_data["password"] = request.password
                    with open(user_file_path, "w", encoding="utf-8") as file:
                        json.dump(user_data, file)
                    return {"message": "Password successfully changed"}
                else:
                    raise HTTPException(status_code=400, detail="Email does not match")
        else:
            raise HTTPException(status_code=401, detail="User not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/post/login")
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

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
    

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
# CREATE NEW USER DATA FILE
# RETURNS: NEW USER DATA IF OK
@app.post("/post/register")
def register(register_request: RegisterRequest):
    username = register_request.username
    user_email = register_request.email
    password = register_request.password
    try:
        users_dir = "data/users/"
        new_file_path = os.path.join(users_dir, f"{username}.json")
        
        # Verificar si el usuario ya existe
        for filename in os.listdir(users_dir):
            with open(os.path.join(users_dir, filename), "r") as file:
                existing_user = json.load(file)
                if existing_user["email"] == user_email:
                    print(f"Email in use: {existing_user}")
                    raise HTTPException(status_code=401, detail="Email in use")

        new_data = {
            "id": username,
            "email": user_email,
            "favorites": [],
            "password": password
        }

        if not os.path.exists(new_file_path):
            with open(new_file_path, "w") as file:
                json.dump(new_data, file)
            print(f"New user data created: {new_data}")
            return {"message": "Register success"}
        else:
            print(f"User data already exists: {new_data}")
            raise HTTPException(status_code=400, detail="Username exists")

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=404, detail="Error")

# DELETE USER DATA FILE
@app.delete("/delete/user/{username}")
def delete_user(username: str):
    try:
        user_file_path = f"data/users/{username}.json"
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
            return {"message": "User successfully deleted"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))