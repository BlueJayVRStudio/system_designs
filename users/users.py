from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Dict

from fastapi import APIRouter, HTTPException
from tinydb import TinyDB, Query

from fastapi.templating import Jinja2Templates

from starlette.requests import Request
from starlette.status import HTTP_303_SEE_OTHER

from models.auth_models import User
from database import Session
import os

from datetime import datetime

templates = Jinja2Templates(directory="./users")

import bcrypt
def hash_password(plain: str | None) -> str | None:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8") if plain else None
def verify_password(to_check, in_store):
    return bcrypt.checkpw(to_check.encode(), in_store.encode())

router = APIRouter()

@router.get("/")
def show_login_form(request: Request):
    error = request.query_params.get("error")
    logout = request.query_params.get("logout")
    session_invalid = request.query_params.get("session_invalid")
    return templates.TemplateResponse("login_form.html", {
        "request": request,
        "error": error,
        "logout": logout,
        "session_invalid": session_invalid
    })

@router.post("/")
def login(
    request: Request,
    user_id: str = Form(...),
    password: str = Form(None),
):
    db = Session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or not verify_password(password, user.password):
            # Redirect with an error query param
            return RedirectResponse(url="/login?error=1", status_code=HTTP_303_SEE_OTHER)

        request.session["user_id"] = user.user_id
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    finally:
        db.close()

@router.post("/logout")
def logout(request: Request):
    request.session.pop("user_id")
    return RedirectResponse(url="/login?logout=1", status_code=HTTP_303_SEE_OTHER)

@router.get("/users/search/{user_id}")
def get_user(user_id: str, request: Request):
    # print(request.session["user"]) # it works
    db = Session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        return user
    finally:
        db.close()

@router.get("/users/create", response_class=HTMLResponse)
def show_create_user_form(request: Request):
    return templates.TemplateResponse("create_form.html", {"request": request})

@router.post("/users/create")
def create_user(
    user_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(None),
):
    db = Session()
    try:
        if db.query(User).filter(User.user_id == user_id).first():
            raise HTTPException(status_code=400, detail="User ID already exists")

        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = hash_password(password)

        new_user = User(
            user_id=user_id,
            name=name,
            email=email,
            password=hashed_password,
            created_at=datetime.utcnow(),
            email_verified=False,
            version=1,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "User created", "user_id": new_user.user_id}
    finally:
        db.close()

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