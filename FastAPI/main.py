from fastapi import FastAPI, Request, Form, HTTPException, Body
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
templates = Jinja2Templates(directory="../html")
app.mount("/css", StaticFiles(directory="../css"), name="css")
app.mount("/images", StaticFiles(directory="../images"), name="images")
app.mount("/js", StaticFiles(directory="../js"), name="js")

class User(BaseModel):
    email: str
    password: str

# Load data from the text file
def load_data():
    try:
        with open("userdata.txt", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data

# Save data to the text file
def save_data(data):
    with open("userdata.txt", "w") as file:
        json.dump(data, file)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users/all")
def get_all_users():
    users = load_data()
    return {"users": users}

@app.post("/users/add")
async def add_user(user: User):
    users = load_data()
    users[user.email] = {"email": user.email, "password": user.password}
    save_data(users)
    return {"users": users}

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, user: User):
    users = load_data()

    if user.email in users and users[user.email]["password"] == user.password:
        # Successful login, you can perform further actions here
        return templates.TemplateResponse("login.html", {"request": request, "user": user})
    else:
        # Incorrect login, redirect to login page with an error message
        return RedirectResponse("/login?error=1")

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: int = 0):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

