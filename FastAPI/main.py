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
def index(request: Request, ID: int = Cookie(None), client_type: str = Cookie(None)):
    if ID == None or client_type == None:
        return templates.TemplateResponse("index.html", {"request": request, "client": None})
    client = clients[ID]
    print(client.avatar)
    first_course_id = None
    if client_type == "Lecturer":
        first_course_id = client.courses[0].course_id
    elif client_type == "Student":
        first_course_id = client.enrolls[0].course.course_id
    return templates.TemplateResponse("index.html", {"request": request, "client": client, "first_course_id": first_course_id})

@app.get("/users/all")
def get_all_users():
    return {"clients": list(clients.keys())}

@app.post("/login")
async def set_login(request: Request, response: Response, ID: int = Form(...), password: str = Form(...)):
    if ID in clients.keys():
        if clients[ID].login(ID, password):
            client = clients[ID]
            client_type = "None"
            if type(client) == Lecturer:
                client_type = "Lecturer"
                first_course_id = client.courses[0].course_id
            elif type(client) == Student:
                client_type = "Student"
                first_course_id = client.enrolls[0].course.course_id
            response = RedirectResponse(url="/classes/{}/assignments".format(first_course_id), status_code=303)
            response.set_cookie(key="ID", value=ID)
            response.set_cookie(key="client_type", value=client_type)
            return response
        else:
            return {"message": "Login failed"}
    else: 
        return {"message": "No client found"}


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: int = 0):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.get("/classes/{course_id}/assignments", response_class=HTMLResponse)
async def get_classes(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None)):
    if ID == None or client_type == None:
        return RedirectResponse(url="/", status_code=303)
    
    client = clients[ID]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type
    }
    
    return templates.TemplateResponse("classes.html", data)
    
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

@app.get("/classes/{course_id}/assignments/{assignment_id}", response_class=HTMLResponse)
async def get_assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None), client_type: str = Cookie(None)):
    
    if ID == None or client_type == None:
        return RedirectResponse(url="/", status_code=303)

    try:
        course = root.courses[course_id]
        assignment = root.assignments[assignment_id]
    except:
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        print("not in course")
        return RedirectResponse(url="/", status_code=303)
    
    client = clients[ID]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type, 
        "assignment": assignment, 
        "ID": ID
    }

    return templates.TemplateResponse("assignment.html", data)

@app.post("/uploadFile/{course_id}/{ASS_ID}")
async def upload_file(request: Request, course_id: int, ASS_ID: str, assignmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None)):
    
    try:
        course = root.courses[course_id]
        assignment = root.assignments[ASS_ID]
    except:
        print("Error")
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        print("Not in course")
        return RedirectResponse(url="/", status_code=303)
    
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    if assignmentFiles[0].filename != "":
        for file in assignmentFiles:
            data = await file.read()
            saveas = UPLOAD_DIR + "/" + file.filename
            with open(saveas, 'wb') as f:
                f.write(data)
            summitfiles.append(saveas)
        
    student = root.clients[ID]
    assignment = root.assignments[ASS_ID]
    assignment.summitWork(ID, summitfiles)
    print(assignment.submitted_work, summitfiles)
    return RedirectResponse("/classes/{}/assignments/{}".format(course_id, ASS_ID), status_code=303)

@app.get("/unsubmit/{course_id}/{ASS_ID}")
async def upload_file(request: Request, course_id: int, ASS_ID: str, ID: int = Cookie(None)):

    student = root.clients[ID]
    assignment = root.assignments[ASS_ID]
    assignment.unSummitWork(ID)
    
    return RedirectResponse("/classes/{}/assignments/{}".format(course_id, assignment.id), status_code=303)

@app.get("/classes/{course_id}/addAssignment", response_class=HTMLResponse)
async def add_Assignment(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None)):
    client = clients[ID]
    course = root.courses[course_id]
    assignments = course.assignments
    new_id = None

    while True:
        new_id = generate_uuid()
        if not any(new_id == assignment.id for assignment in assignments):
            break

    due_date = str(date.today())
    assignment_index = len(assignments)
    new_assignment = Assignment(new_id, "Assignment {}".format(assignment_index + 1), 10, due_date)
    root.assignments[new_assignment.id] = new_assignment
    course.addAssignment(root.assignments[new_assignment.id])
    # for i in assignments:
    #     print(i)
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "assignment": new_assignment, 
        "client_type": client_type, 
        "ID": ID
    }
        
    return templates.TemplateResponse("edit_assignment.html", data)

@app.get("/classes/{course_id}/editAssignment/{assignment_id}", response_class=HTMLResponse)
async def edit_Assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None), client_type: str = Cookie(None)):
    client = clients[ID]
    assignment = root.assignments[assignment_id]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course,
        "client_type": client_type, 
        "assignment": assignment, 
        "ID": ID
    }
    
    return templates.TemplateResponse("edit_assignment.html", data)

@app.get("/classes/{course_id}/removeAssignment/{assignment_id}")
async def remove_assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None)):
    client = clients[ID]
    course = root.courses[course_id]
    try:
        assignment = root.assignments[assignment_id]
    except KeyError:
        IncorrectAssignments = course.assignments
        for i in IncorrectAssignments:
            if i.id == assignment_id:
                IncorrectAssignments.p
        return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)
    
    if course.removeAssignment(assignment):
        root.assignments.pop(assignment_id)
        root._p_changed = True
    
    return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)

@app.post("/classes/{course_id}/editAssignment/{assignment_id}")
async def save_Edit_Assignment(request: Request, course_id: int, assignment_id: str, name: str = Form(...), due_date: str = Form(...), description: str = Form(...), attachmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None), client_type: str = Cookie(None)):
    client = clients[ID]
    assignment = root.assignments[assignment_id]
    assignment.setName(name)
    assignment.setDueDate(due_date)
    assignment.setDescription(description)
    # set attachment
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    print(assignment.attachment)
    if attachmentFiles != None :
        try:
            for file in attachmentFiles:
                data = await file.read()
                saveas = UPLOAD_DIR + "/" + file.filename
                with open(saveas, 'wb') as f:
                    f.write(data)
                summitfiles.append(saveas)
            
            assignment.setAttachment(summitfiles)
        except:
            pass
        
    return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)


@app.get("/classes/{course_id}/editAssignment/{assignment_id}/removeAttachment")
async def remove_attachment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None)):
    
    client = root.clients[ID]
    assignment = root.assignments[assignment_id]
    assignment.removeAttachment()

    return RedirectResponse("/classes/{}/editAssignment/{}".format(course_id, assignment_id), status_code=303)


@app.get("/classes/{course_id}/rooms")
async def show_rooms(request: Request, course_id: int, ID: int = Cookie(None)):
    client = clients[ID]
    client_type = "None"
    rooms = None
    
    if type(client) == Lecturer:
        client_type = "Lecturer"
    elif type(client) == Student:
        client_type = "Student"
        
    course = root.courses[course_id]
    rooms = course.rooms
        
    return templates.TemplateResponse("rooms.html", {"request": request, "client": client, "course": course, "client_type": client_type, "rooms": rooms, "ID": ID})

@app.get("/classes/{course_id}/grade/{ass_id}")
async def gradeAssignment(request: Request, course_id: int, ass_id: str, ID: int = Cookie(None), client_type: str = Cookie(None)):
    
    client = root.clients[ID]
    course = root.courses[course_id]
    assignment = root.assignments[ass_id]
    submitted_work = assignment.submitted_work
    
    data = {
        "request": request,
        "client": client,
        "course": course,
        "client_type": client_type,
        "assignment": assignment,
        "submitted_work": submitted_work,
        "root": root
    }
    
    print(submitted_work)
    
    return templates.TemplateResponse("gradeall.html", data)

@app.get("/delete/submission/{course_id}/{ass_id}/{student_id}")
async def removeSubmission(request: Request, course_id: int, student_id: int, ass_id: str, ID: int = Cookie(None), client_type: str = Cookie(None)):
    if client_type != "Lecturer":
        return {"Message": "NO PERMISSION"}
    assignment = root.assignments[ass_id]
    assignment.unSummitWork(student_id)
    return RedirectResponse(url = "/classes/{}/grade/{}".format(course_id, ass_id), status_code=303)

@app.get("/classes/{course_id}/grade/{ass_id}/{student_id}")
async def grade_Student(request: Request, course_id: int, ass_id: str, student_id: int, ID: int = Cookie(None), client_type: str = Cookie(None)):
    client = root.clients[ID]
    course = root.courses[course_id]
    assignment = root.assignments[ass_id]
    submitted_work = assignment.submitted_work
    student = root.clients[student_id]

    data = {
        "request": request,
        "client": client,
        "course": course,
        "student": student,
        "client_type": client_type,
        "assignment": assignment,
        "submitted_work": submitted_work,
        "root": root
    }

    return templates.TemplateResponse("gradeIndividual.html", data)

@app.post("/grading/{course_id}/{ass_id}/{student_id}")
async def grading_Student(request: Request, course_id: int, ass_id: str, student_id: int, score: int = Form(None) ,ID: int = Cookie(None), client_type: str = Cookie(None)):
    if score == None:
        pass
    else:
        assignment = root.assignments[ass_id]
        if score > assignment.max_score:
            score = assignment.max_score
        assignment.grading(student_id, score)

    return RedirectResponse("/classes/{}/grade/{}".format(course_id, ass_id), status_code=303)


@app.get("/room/edit/page/{room_id}")
async def show_rooms(request: Request, room_id: str, ID: int = Cookie(None)):
    client = clients[ID]
    client_type = "Lecturer"
    rooms = None
    
    if type(client) != Lecturer:
        return {"message": "You are not allowed to edit room"}
    
    room = root.rooms[room_id]
        
    return templates.TemplateResponse("editroom.html", {"request": request, "client": client, "client_type": client_type, "room": room, "ID": ID, "type": "edit"})

@app.post("/room/edit/{room_id}")
async def show_rooms(request: Request, room_id: str, title: str = Form(...), ID: int = Cookie(None)):
    
    room = root.rooms[room_id]
    client = clients[ID]
    course_id = client.courses[0].course_id
    
    room.setTitle(title)
        
    return RedirectResponse("/classes/{}/rooms".format(course_id), status_code=303)

@app.get("/room/delete/{course_id}/{room_id}")
async def deleteRoom(request: Request, room_id: str, course_id: int, ID: int = Cookie(None)):
    client = clients[ID]
    
    if type(client) != Lecturer:
        return {"message": "You are not allowed to edit room"}
    
    room = root.rooms[room_id]
    course = root.courses[course_id]
    
    course.removeRoom(room)
    room.delete()
    del root.rooms[room_id]
    
    root._p_changed = True
    
    return RedirectResponse("/classes/{}/rooms".format(course_id), status_code=303)

@app.get("/room/add/page/{course_id}")
async def show_rooms(request: Request, course_id: int, ID: int = Cookie(None)):
    
    room_id = generate_uuid()
    client_type = "Lecturer"
    course = root.courses[course_id]
        
    return templates.TemplateResponse("editroom.html", {"request": request, "client": client, "client_type": client_type, "room": None, "course_id": course_id, "course": course, "room_id": room_id, "ID": ID, "type": "add"})

@app.post("/room/add/{course_id}/{room_id}")
async def show_rooms(request: Request, course_id: int, room_id: str, title: str = Form(...), ID: int = Cookie(None)):
    
    root.rooms[room_id] = Room(room_id, title)
    root.courses[course_id].addRoom(root.rooms[room_id])
        
    return RedirectResponse("/classes/{}/rooms".format(course_id), status_code=303)

@app.on_event("shutdown")
async def shutdown():
    transaction.commit()