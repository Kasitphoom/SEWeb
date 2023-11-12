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

root.students = BTrees.OOBTree.BTree()
root.students[1100] = Student([], 1100, "Mr. Tonkla Pokaew", 1234)
root.students[1100].enrolls = [Enrollment(root.courses[101], 80, root.students[1100]), Enrollment(root.courses[201], 87, root.students[1100]), Enrollment(root.courses[202], 69, root.students[1100]), Enrollment(root.courses[301], 80, root.students[1100])]

# create test case as above
root.students[1101] = Student([], 1101, "Mr. John Doe", 1234)
root.students[1101].enrolls = [Enrollment(root.courses[101], 80, root.students[1101]), Enrollment(root.courses[201], 87, root.students[1101]), Enrollment(root.courses[202], 69, root.students[1101]), Enrollment(root.courses[301], 80, root.students[1101])]

root.students[1102] = Student([], 1102, "Mr. Mohamed ibn Ibrahim", 1234)
root.students[1102].enrolls = [Enrollment(root.courses[101], 80, root.students[1102]), Enrollment(root.courses[201], 87, root.students[1102]), Enrollment(root.courses[202], 69, root.students[1102]), Enrollment(root.courses[301], 80, root.students[1102])]

transaction.commit()
db.close()