from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict

from fastapi import APIRouter, HTTPException
from tinydb import TinyDB, Query

from models.auth_models import User
from database import Session
import os

router = APIRouter()

# @router.get("/users/{user_id}")
# def get_user(user_id: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@router.get("/users/{user_id}")
def get_user(user_id: str):
    db = Session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        return user
    finally:
        db.close()

# @router.post("/users")
# def create_user(user: User):
#     if db.search(UserQuery.id == user.id):
#         raise HTTPException(status_code=400, detail="User already exists")
#     db.insert(user.dict())
#     return {"msg": "User created"}

# @router.put("/users/{user_id}")
# def update_user(user_id: str, updated: User):
#     user = db.search(UserQuery.id == user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     current = user[0]
#     if updated.version != current["version"]:
#         raise HTTPException(status_code=409, detail="Version mismatch")

#     updated.version += 1
#     db.update(updated.dict(), UserQuery.id == user_id)
#     return {"msg": "User updated"}

# @router.patch("/users/{user_id}")
# def patch_user(user_id: str, fields: dict):
#     user = db.get(UserQuery.id == user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Check version match if provided
#     if "version" in fields and fields["version"] != user["version"]:
#         raise HTTPException(status_code=409, detail="Version mismatch")

#     # Remove version field from the patch (we control it)
#     fields.pop("version", None)

#     # Apply changes and increment version
#     updated_user = {**user, **fields, "version": user["version"] + 1}
#     db.update(updated_user, UserQuery.id == user_id)
#     return updated_user

# @router.delete("/users/{user_id}")
# def delete_user(user_id: str):
#     user = db.get(UserQuery.id == user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.remove(UserQuery.id == user_id)
#     return {"detail": "User deleted"}