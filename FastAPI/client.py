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
root.courses[101] = Course(101, "Computer Programming", 4)
root.courses[201] = Course(201, "Web Programming", 4)
root.courses[202] = Course(202, "Software Engineering Principles", 5)
root.courses[301] = Course(301, "Artificial Intelligent", 3)

root.courses[101].setGradeScheme(gradeScheme)
root.courses[201].setGradeScheme(gradeScheme)
root.courses[202].setGradeScheme(gradeScheme)
root.courses[301].setGradeScheme(gradeScheme)

root.courses[101].assignments = [Assignment("Assignment 1", 10, "2021-01-01"), Assignment("Assignment 2", 10, "2021-01-01"), Assignment("Assignment 3", 10, "2021-01-01"), Assignment("Assignment 4", 10, "2021-01-01")]

root.clients = BTrees.OOBTree.BTree()
#Lecturers
root.clients[9001] = Lecturer(9001, [], "Micheal Scott", "TheBestBoss", "1234", "../images/gojo.png")
root.clients[9001].setCourses([Course(101, "Computer Programming", 4), Course(201, "Web Programming", 4), Course(202, "Software Engineering Principles", 5), Course(301, "Artificial Intelligent", 3)])

#Students
root.clients[1100] = Student(1100, [], "Kasitphoom Thowongs", "student1101", "1234", "../images/micomet.jpg")
root.clients[1100].enrolls = [Enrollment(root.courses[101], 80, root.clients[1100]), Enrollment(root.courses[201], 87, root.clients[1100]), Enrollment(root.courses[202], 69, root.clients[1100]), Enrollment(root.courses[301], 80, root.clients[1100])]
root.clients[1101] = Student(1101, [], "Phupa Denphatcharangkul", "student1102", "1234")
root.clients[1101].enrolls = [Enrollment(root.courses[101], 80, root.clients[1101]), Enrollment(root.courses[201], 87, root.clients[1101]), Enrollment(root.courses[202], 69, root.clients[1101]), Enrollment(root.courses[301], 80, root.clients[1101])]
root.clients[1102] = Student(1102, [], "Pitiphong Khongkrapan","student1102", "1234")
root.clients[1102].enrolls = [Enrollment(root.courses[101], 80, root.clients[1102]), Enrollment(root.courses[201], 87, root.clients[1102]), Enrollment(root.courses[202], 69, root.clients[1102]), Enrollment(root.courses[301], 80, root.clients[1102])]

transaction.commit()
db.close()
