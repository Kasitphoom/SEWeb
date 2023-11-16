import ZODB, ZODB.FileStorage, BTrees.OOBTree
import transaction
from class_module import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

gradeScheme = [
    {"Grade": "A", "min":80, "max":100},
    {"Grade": "B", "min":70, "max":79}, 
    {"Grade": "C", "min":60, "max":69}, 
    {"Grade": "D", "min":50, "max":59}, 
    {"Grade": "F", "min":0, "max":49}
]

root.courses = BTrees.OOBTree.BTree()
root.courses[101] = Course(101, "Computer Programming", 4, banner="/images/Python-banner.png")
root.courses[201] = Course(201, "Web Programming", 4)
root.courses[202] = Course(202, "Software Engineering Principles", 5)
root.courses[301] = Course(301, "Artificial Intelligent", 3)

root.courses[101].setGradeScheme(gradeScheme)
root.courses[201].setGradeScheme(gradeScheme)
root.courses[202].setGradeScheme(gradeScheme)
root.courses[301].setGradeScheme(gradeScheme)

root.assignments = BTrees.OOBTree.BTree()
root.assignments["dff9328c-93ad-4b68-af6a-8934c809e5d0"] = Assignment("dff9328c-93ad-4b68-af6a-8934c809e5d0", "Assignment 1", 10, "2021-01-01")
root.assignments["ed1c46f0-90d8-4ec9-907d-368b62446640"] = Assignment("ed1c46f0-90d8-4ec9-907d-368b62446640", "Assignment 2", 10, "2021-01-01")
root.assignments["e184b3dd-0174-4bfa-b18b-786e9204d3c8"] = Assignment("e184b3dd-0174-4bfa-b18b-786e9204d3c8", "Assignment 3", 10, "2021-01-01")
root.assignments["6f323d65-cbaf-4cee-b341-983a223d31f0"] = Assignment("6f323d65-cbaf-4cee-b341-983a223d31f0", "Write a website 1", 10, "2021-01-10")
root.assignments["d504ce3c-7ea2-4e3b-a2b8-fe33668746b7"] = Assignment("d504ce3c-7ea2-4e3b-a2b8-fe33668746b7", "Write a website 2", 10, "2021-01-10")
root.assignments["0b6d8814-ef19-454e-ad60-ad5a1b20676b"] = Assignment("0b6d8814-ef19-454e-ad60-ad5a1b20676b", "Write a software 1", 10, "2021-01-10")
root.assignments["9a07bbf1-291d-42b1-8277-87876755f56d"] = Assignment("9a07bbf1-291d-42b1-8277-87876755f56d", "Write a software 2", 10, "2021-01-10")
root.assignments["c2a7363c-2b0b-4cd9-8f66-effc04fc24df"] = Assignment("c2a7363c-2b0b-4cd9-8f66-effc04fc24df", "Write a AI 1", 10, "2021-01-10")
root.assignments["cb3a49ab-4d2b-489b-9a92-2115744ec040"] = Assignment("cb3a49ab-4d2b-489b-9a92-2115744ec040", "Write a AI 2", 10, "2021-01-10")

root.courses[101].assignments = [root.assignments["dff9328c-93ad-4b68-af6a-8934c809e5d0"], root.assignments["ed1c46f0-90d8-4ec9-907d-368b62446640"], root.assignments["e184b3dd-0174-4bfa-b18b-786e9204d3c8"]]
root.courses[201].assignments = [root.assignments["6f323d65-cbaf-4cee-b341-983a223d31f0"], root.assignments["d504ce3c-7ea2-4e3b-a2b8-fe33668746b7"]]
root.courses[202].assignments = [root.assignments["0b6d8814-ef19-454e-ad60-ad5a1b20676b"], root.assignments["9a07bbf1-291d-42b1-8277-87876755f56d"]]
root.courses[301].assignments = [root.assignments["c2a7363c-2b0b-4cd9-8f66-effc04fc24df"], root.assignments["cb3a49ab-4d2b-489b-9a92-2115744ec040"]]

root.clients = BTrees.OOBTree.BTree()
#Lecturers
root.clients[9001] = Lecturer(9001, [], "Micheal Scott", "TheBestBoss", "1234", "/images/gojo.png")
root.clients[9001].setCourses([root.courses[101], root.courses[201], root.courses[202], root.courses[301]])

#Students
root.clients[1100] = Student(1100, [], "Kasitphoom Thowongs", "student1101", "1234", "/images/micomet.jpg")
root.clients[1100].enrolls = [Enrollment(root.courses[101], 80, root.clients[1100]), Enrollment(root.courses[201], 87, root.clients[1100]), Enrollment(root.courses[202], 69, root.clients[1100]), Enrollment(root.courses[301], 80, root.clients[1100])]
root.clients[1101] = Student(1101, [], "Phupa Denphatcharangkul", "student1102", "1234")
root.clients[1101].enrolls = [Enrollment(root.courses[101], 80, root.clients[1101]), Enrollment(root.courses[201], 87, root.clients[1101]), Enrollment(root.courses[202], 69, root.clients[1101]), Enrollment(root.courses[301], 80, root.clients[1101])]
root.clients[1102] = Student(1102, [], "Pitiphong Khongkrapan","student1102", "1234")
root.clients[1102].enrolls = [Enrollment(root.courses[101], 80, root.clients[1102]), Enrollment(root.courses[201], 87, root.clients[1102]), Enrollment(root.courses[202], 69, root.clients[1102]), Enrollment(root.courses[301], 80, root.clients[1102])]

root.rooms = BTrees.OOBTree.BTree()

transaction.commit()
db.close()
