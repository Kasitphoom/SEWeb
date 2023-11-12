from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ZODB, ZODB.FileStorage
import BTrees.OOBTree
import transaction
from database import db  # Import the initialized database

storage = ZODB.FileStorage.FileStorage('C:/.Phong/.kmitl/.year2/html/pr/SEWeb/data_storage/mydata.fs')

db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# Check if 'users' exist in the root. If not, create it.
if not hasattr(root, 'users'):
    root.users = BTrees.OOBTree.BTree()


app = FastAPI()

class User(BaseModel):
    email: str
    password: str

# is this secure? nope :D
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users/all") #get service to retrieve all data
def A_get_all():
    users = root.users
    return {"users": users}

@app.post("/users/add")
async def add_user(user: User):
    users = root.users
    users[user.email] = { "email": user.email, "password": user.password}
    return {"users": users}
