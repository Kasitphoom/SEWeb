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
root.courses[101] = Course(101, "Computer Programming", 4, banner="/images/maimai-festival.jpg")
root.courses[201] = Course(201, "Web Programming", 4)
root.courses[202] = Course(202, "Software Engineering Principles", 5)
root.courses[301] = Course(301, "Artificial Intelligent", 3)

root.courses[101].setGradeScheme(gradeScheme)
root.courses[201].setGradeScheme(gradeScheme)
root.courses[202].setGradeScheme(gradeScheme)
root.courses[301].setGradeScheme(gradeScheme)

root.courses[101].assignments = [Assignment("dff9328c-93ad-4b68-af6a-8934c809e5d0", "Assignment 1", 10, "2021-01-01"), Assignment("ed1c46f0-90d8-4ec9-907d-368b62446640", "Assignment 2", 10, "2021-01-01"), Assignment("e184b3dd-0174-4bfa-b18b-786e9204d3c8", "Assignment 3", 10, "2021-01-01"), Assignment("4add27a3-fbe3-415d-9730-5f26102dd600", "Assignment 4", 10, "2021-01-01")]
root.courses[201].assignments = [Assignment("6f323d65-cbaf-4cee-b341-983a223d31f0", "Write a website 1", 10, "2021-01-10"), Assignment("d504ce3c-7ea2-4e3b-a2b8-fe33668746b7", "Write a website 2", 10, "2021-01-10"), Assignment("f5d93289-40ad-47f3-82b8-1614abf9b76d", "Write a website 3", 10, "2021-01-10"), Assignment("08c99ebf-e186-4d1e-8bc7-0e62bbef4e6d", "Write a website 4", 10, "2021-01-10")]
root.courses[202].assignments = [Assignment("0b6d8814-ef19-454e-ad60-ad5a1b20676b", "Write a software 1", 10, "2021-01-10"), Assignment("9a07bbf1-291d-42b1-8277-87876755f56d", "Write a software 2", 10, "2021-01-10"), Assignment("d0bbaed4-2a22-42e3-8947-d309fd9236e9", "Write a software 3", 10, "2021-01-10"), Assignment("37e9c03c-b204-4447-83e9-e73e488dabb6", "Write a software 4", 10, "2021-01-10")]
root.courses[301].assignments = [Assignment("c2a7363c-2b0b-4cd9-8f66-effc04fc24df", "Write a AI 1", 10, "2021-01-10"), Assignment("cb3a49ab-4d2b-489b-9a92-2115744ec040", "Write a AI 2", 10, "2021-01-10"), Assignment("1d91c971-bffd-4829-bec2-25e768a68137", "Write a AI 3", 10, "2021-01-10"), Assignment("d4125ce2-e44c-4c90-898d-48f5f251f76c", "Write a AI 4", 10, "2021-01-10")]

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
