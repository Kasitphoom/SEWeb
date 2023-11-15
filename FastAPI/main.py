from fastapi import FastAPI, Request, Form, HTTPException, Body, Cookie, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from class_module import *
import ZODB, ZODB.FileStorage
import transaction

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
clients = root.clients

client = clients[9001]
print()

app = FastAPI()
templates = Jinja2Templates(directory="../html")
app.mount("/css", StaticFiles(directory="../css"), name="css")
app.mount("/images", StaticFiles(directory="../images"), name="images")
app.mount("/js", StaticFiles(directory="../js"), name="js")
app.mount("/Upload", StaticFiles(directory="Upload"), name="Upload")

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
            response = RedirectResponse(url="/classes/0/assignments", status_code=303)
            response.set_cookie(key="ID", value=ID)
            return response
        else:
            return {"message": "Login failed"}
    else: 
        return {"message": "No client found"}


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: int = 0):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.get("/classes/{course_index}/assignments", response_class=HTMLResponse)
async def get_classes(request: Request, course_index: int, ID: int = Cookie(None)):
    if ID == None:
        return RedirectResponse(url="/", status_code=303)
    client = clients[ID]
    client_type = "None"
    if type(client) == Lecturer:
        client_type = "Lecturer"
    elif type(client) == Student:
        client_type = "Student"

    return templates.TemplateResponse("classes.html", {"request": request, "client": client, "course_index": course_index, "client_type": client_type})
    
@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="ID")
    return response

@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, ID: int = Cookie(None)):
    client = clients[ID]
    return templates.TemplateResponse("profile.html", {"request": request, "client": client})

@app.post("/profile")
async def set_profile(request: Request, ID: int = Cookie(None), name: str = Form(...), user_name: str = Form(...), avatar: UploadFile = File(...)):
    UPLOAD_DIR = "Upload"
    client = clients[ID]
    client.setName(name)
    client.setUsername(user_name)
    data = await avatar.read()
    saveas = UPLOAD_DIR + "/" + avatar.filename
    with open(saveas, 'wb') as f:
        f.write(data)
    saveas = "/" + UPLOAD_DIR + "/" + avatar.filename
    client.setAvatar(saveas)
    return RedirectResponse(url="/profile", status_code=303)

@app.get("/classes/{course_index}/assignments/{assignment_name}", response_class=HTMLResponse)
async def get_assignment(request: Request, course_index: int, assignment_name: str, ID: int = Cookie(None)):
    client = clients[ID]
    client_type = "None"
    if type(client) == Lecturer:
        client_type = "Lecturer"
        for a in client.courses[course_index].assignments:
            if a.name == assignment_name:
                assignment = a
                break
    elif type(client) == Student:
        client_type = "Student"
        for a in client.enrolls[course_index].course.assignments:
            if a.name == assignment_name:
                assignment = a
                break
    return templates.TemplateResponse("assignment.html", {"request": request, "client": client, "course_index": course_index, "assignment_name": assignment_name, "client_type": client_type, "assignment": assignment, "ID": ID})

@app.post("/uploadFile/{course_index}/{ASS_ID}")
async def upload_file(request: Request, course_index: int, ASS_ID: str, assignmentFiles: List[UploadFile] = File(...), ID: int = Cookie(None)):
    # loop through request.form()
    UPLOAD_DIR = "Upload"
    summitfiles = []
    for file in assignmentFiles:
        data = await file.read()
        saveas = UPLOAD_DIR + "/" + file.filename
        with open(saveas, 'wb') as f:
            f.write(data)
        summitfiles.append(saveas)
        
    currentAss = None
    student = root.clients[ID]
    assignments = student.enrolls[course_index].course.assignments
    for assignment in assignments:
        if assignment.id == ASS_ID:
            currentAss = assignment
            currentAss.summitWork(ID, summitfiles)
            print(assignment.submitted_work, summitfiles)
    return RedirectResponse("/classes/{}/assignments/{}".format(course_index, currentAss.name), status_code=303)

@app.get("/unsubmit/{course_index}/{ASS_ID}")
async def upload_file(request: Request, course_index: int, ASS_ID: str, ID: int = Cookie(None)):
    currentAss = None
    student = root.clients[ID]
    assignments = student.enrolls[course_index].course.assignments
    for assignment in assignments:
        if assignment.id == ASS_ID:
            currentAss = assignment
            currentAss.unSummitWork(ID)
    return RedirectResponse("/classes/{}/assignments/{}".format(course_index, currentAss.name), status_code=303)

@app.get("/classes/{course_index}/addAssignment", response_class=HTMLResponse)
async def add_Assignment(request: Request, course_index: int, ID: int = Cookie(None)):
    client = clients[ID]
    client_type = "Lecturer"
    course = client.courses[course_index]
    assignments = course.assignments
    new_id = None

    while True:
        new_id = generate_uuid()
        if not any(new_id == assignment.id for assignment in assignments):
            break

    due_date = date.today()
    assignment_index = len(assignments)
    new_assignment = Assignment(new_id, "Assignment {}".format(assignment_index + 1), 10, due_date)
    course.addAssignment(new_assignment)
    assignment_name = new_assignment.name
    # for i in assignments:
    #     print(i)
        
    return templates.TemplateResponse("edit_assignment.html", {"request": request, "client": client, "course_index": course_index, "assignment_name": assignment_name, "client_type": client_type, "assignment": new_assignment, "ID": ID})

@app.get("/classes/{course_index}/editAssignment/{assignment_name}", response_class=HTMLResponse)
async def edit_Assignment(request: Request, course_index: int, assignment_name: str, ID: int = Cookie(None)):
    client = clients[ID]
    client_type = "Lecturer"
    for a in client.courses[course_index].assignments:
        if a.name == assignment_name:
            assignment = a
            break
    return templates.TemplateResponse("edit_assignment.html", {"request": request, "client": client, "course_index": course_index, "assignment_name": assignment_name, "client_type": client_type, "assignment": assignment, "ID": ID})

@app.get("/classes/{course_index}/rooms")
async def show_rooms(request: Request, course_index: int, ID: int = Cookie(None)):
    client = clients[ID]
    client_type = "None"
    rooms = None
    
    if type(client) == Lecturer:
        client_type = "Lecturer"
        course_id = client.courses[course_index].course_id
    elif type(client) == Student:
        client_type = "Student"
        course_id = client.enrolls[course_index].course.course_id
        
    course = root.courses[course_id]
    rooms = course.rooms
        
    return templates.TemplateResponse("rooms.html", {"request": request, "client": client, "course": course, "client_type": client_type, "rooms": rooms, "ID": ID})

@app.on_event("shutdown")
async def shutdown():
    transaction.commit()