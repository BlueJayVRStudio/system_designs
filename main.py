from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
load_dotenv()
import os
import studio.video as video
import users.users as users
from collections import defaultdict

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

# Mount router with NO prefix
app.include_router(video.router, prefix="/studio")
app.include_router(users.router, prefix="/login")

@app.get('/')
def main_home(request: Request):
    if "user" in request.session:
        return request.session["user"]["name"]
    return "not logged in brother"

@app.get('/login/{name}')
def main_home(request: Request, name):
    request.session["user"] = {"name": name}