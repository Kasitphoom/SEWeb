from fastapi import FastAPI, Request, Form, HTTPException, Body
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from class_module import *
import json

app = FastAPI()
templates = Jinja2Templates(directory="../html")
app.mount("/css", StaticFiles(directory="../css"), name="css")
app.mount("/images", StaticFiles(directory="../images"), name="images")
app.mount("/js", StaticFiles(directory="../js"), name="js")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users/all")
def get_all_users():
    users = Student.get_all_students()
    return {"users": users}

@app.post("/login")
def getform(request: Request, email: str = Form(...), password: str = Form(...)):
    student = Student.login(student_id, password)
    print(student)
    if student:
        # Successful login
        print("Successful login")
        data = {"student_id": student_id, "password": password}
        return  templates.TemplateResponse("index.html", {"request": request, "data":data})
    else:
        # Invalid login
        print("Failed to login")
        return {"Error": "Invalid login"}

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: int = 0):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})
