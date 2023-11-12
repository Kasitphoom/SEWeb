import persistent
import ZODB, ZODB.FileStorage, BTrees.OOBTree
import transaction

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

class Course(persistent.Persistent):
    def __init__(self, course_id, name , credit=3):
        self.credit = credit
        self.course_id = course_id
        self.name = name
        self.gradeScheme = [
            {"Grade": "A", "min":80, "max":100},
            {"Grade": "B", "min":70, "max":79},
            {"Grade": "C", "min":60, "max":69},
            {"Grade": "D", "min":50, "max":59},
            {"Grade": "F", "min":0, "max":49}
        ]

    def getCredit(self):
        return self.credit

    def setName(self, name):
        self.name = name

    def printDetail(self):
        print("ID:          {}, Course:         {}      ,Credit: {}".format(self.course_id, self.name, self.credit))

    def scoreGrading(self, score):
        for grade in self.gradeScheme:
            if score >= grade["min"] and score <= grade["max"]:
                return grade["Grade"]
        return None
    
    def setGradeScheme(self, gradeScheme):
        self.gradeScheme = gradeScheme

    def scoreGradingAsNum(self,score):
        grade = self.scoreGrading(score)
        switcher = {
            "A": 4,
            "B": 3,
            "C": 2,
            "D": 1,
            "F": 0
        }
        return switcher.get(grade, "Invalid grade")

class Student(persistent.Persistent):
    def __init__(self,enrolls, student_id, name, password):
        self.enrolls = enrolls
        self.id = student_id
        self.name = name
        self.password = password

    def enrollCourse(self, course):
        enrollment = Enrollment(self, course)
        self.enrolls.append(enrollment)
        return enrollment

    def getEnrollment(self, course):
        for enrollment in self.enrolls:
            if enrollment.getCourse() == course:
                return enrollment
        return None
    
    @classmethod
    def login(cls, student_id, password):
        storage = ZODB.FileStorage.FileStorage('mydata.fs')
        db = ZODB.DB(storage)
        connection = db.open()
        root = connection.root

        students = root.students
        for s in students:
            student = students[s]
            print("Input values: student_id =", student_id, "password =", password)
            print("Stored values: student.id =", student.id, "student.password =", student.password)
            if student.id == student_id and student.password == password:
                transaction.commit()
                db.close()
                print("LOGIN SUCCESSFUL")
                return True

        transaction.commit()
        db.close()
        print("LOGIN FAILED")
        return False
    
    @classmethod
    def get_all_students():
        storage = ZODB.FileStorage.FileStorage('mydata.fs')
        db = ZODB.DB(storage)
        connection = db.open()
        
        root = connection.root
        students = root.students
        all_students = {student.id: {"name": student.name, "password": student.password} for student in students.values()}
        transaction.commit()
        db.close()
        return all_students

    def getGPA(self):
        totalpoint = 0
        totalcredit = 0
        for enroll in self.enrolls:
            totalpoint += enroll.getCourse().scoreGradingAsNum(enroll.getScore()) * enroll.getCourse().getCredit()
            totalcredit += enroll.getCourse().getCredit()
        return totalpoint / totalcredit

    def __str__(self):
        courses = ""
        courses += "            Transcripts            \n"
        courses += "ID:     {} Name: {}\n".format(self.id, self.name)
        courses += "Course list\n"
        for enroll in self.enrolls:
            courses += "ID:         {}, Course: {}          , Credit: {} Score: {} Grade: {}\n".format(enroll.getCourse().course_id, enroll.getCourse().name, enroll.getCourse().credit, enroll.getScore(), enroll.getGrade())
        courses += "GPA: {:.3}\n".format(self.getGPA())
        courses += "==============================================="
        return courses

    def printTranscript(self):
        print(self.__str__())

    def setName(self, name):
        self.name = name

class Enrollment(persistent.Persistent):
    def __init__(self, course, score, student):
        self.course = course
        self.score = score
        self.student = student

    def getCourse(self):
        return self.course

    def getGrade(self):
        return self.course.scoreGrading(self.score)

    def printDetail(self):
        print(f"ID: {self.student.id} Course: {self.course.name} , Credit: {self.course.credit}")

    def getScore(self):
        return self.score
    
    def setScore(self, score):
        self.score = score


gradeScheme = [
    {"Grade": "A", "min":80, "max":100},
    {"Grade": "B", "min":70, "max":79}, 
    {"Grade": "C", "min":60, "max":69}, 
    {"Grade": "D", "min":50, "max":59}, 
    {"Grade": "F", "min":0, "max":49}
]


transaction.commit()
db.close()