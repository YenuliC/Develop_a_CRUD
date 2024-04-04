# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Database simulation
users_db: Dict[int, Dict[str, str]] = {}

class User(BaseModel):
    first_name: str
    last_name: str
    email: str

@app.post("/users/", response_model=User)
def create_user(user: User):
    user_id = len(users_db) + 1
    users_db[user_id] = user.dict()
    return user

@app.get("/users/", response_model=List[User])
def read_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db.pop(user_id)
