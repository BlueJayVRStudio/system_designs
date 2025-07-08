from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
# from starlette.status import HTTP_302_FOUND, HTTP_200_OK
from dotenv import load_dotenv
load_dotenv()
import os
import studio.video as video
import users.users as users
from collections import defaultdict

templates = Jinja2Templates(directory="./templates")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

# Mount router with NO prefix
app.include_router(video.router, prefix="/studio")
app.include_router(users.router, prefix="/login")

@app.get('/')
def main_home(request: Request):
    if "user_id" in request.session:
        return templates.TemplateResponse("landing.html", {"request": request})
    return RedirectResponse(url="/login", status_code=302)

# definitely not going to be in production
@app.get('/set_name/{name}')
def main_home(request: Request, name):
    request.session["user_id"] = {"name": name}