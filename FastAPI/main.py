from fastapi import FastAPI, Request, Form, HTTPException, Body, Cookie
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from class_module import *
import ZODB, ZODB.FileStorage
import transaction

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
clients = root.clients

app = FastAPI()
templates = Jinja2Templates(directory="../html")
app.mount("/css", StaticFiles(directory="../css"), name="css")
app.mount("/images", StaticFiles(directory="../images"), name="images")
app.mount("/js", StaticFiles(directory="../js"), name="js")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, ID: int = Cookie(None)):
    if ID == None:
        return templates.TemplateResponse("index.html", {"request": request, "client": None})
    client = clients[ID]
    print(client.avatar)
    return templates.TemplateResponse("index.html", {"request": request, "client": client})

@app.get("/users/all")
def get_all_users():
    return {"clients": list(clients.keys())}

@app.post("/login")
async def set_login(request: Request, response: Response, ID: int = Form(...), password: str = Form(...)):
    if ID in clients.keys():
        if clients[ID].login(ID, password):
            response = RedirectResponse(url="/classes", status_code=303)
            response.set_cookie(key="ID", value=ID)
            return response
        else:
            return {"message": "Login failed"}
    else: 
        return {"message": "No client found"}


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: int = 0):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.get("/classes", response_class=HTMLResponse)
async def get_classes(request: Request, ID: int = Cookie(None)):
    client = clients[ID]
    course_index = 0
    return templates.TemplateResponse("classes.html", {"request": request, "client": client, "course_index": course_index})
