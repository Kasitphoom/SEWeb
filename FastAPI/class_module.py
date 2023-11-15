import persistent
import os
import uuid
from datetime import date

def generate_uuid():
    return str(uuid.uuid4())

class Client(persistent.Persistent):
    def __init__(self, ID, name, user_name, password, avatar):
        self.ID = ID
        self.name = name
        self.user_name = user_name
        self.password = password
        self.avatar = avatar

    def login(self, ID, password):
        print(self.password)
        if self.ID == ID and self.password == password:
            return True
        return False
    
    def setUsername(self, user_name):
        self.user_name = user_name

    def setName(self, name):
        self.name = name

    def setAvatar(self, avatar):
        self.avatar = avatar

class Lecturer(Client):
    def __init__(self, ID, courses, name, user_name, password, avatar="../images/user-default-avatar.svg"):
        super().__init__(ID ,name, user_name, password, avatar)
        self.courses = courses

    def setCourses(self, courses):
        self.courses = courses

    def addCourse(self, course):
        self.courses.append(course)
    

class Student(Client):
    def __init__(self, ID, enrolls, name, user_name, password, avatar="../images/user-default-avatar.svg"):
        super().__init__(ID, name, user_name, password, avatar)
        self.enrolls = enrolls

    def enrollCourse(self, course):
        enrollment = Enrollment(self, course)
        self.enrolls.append(enrollment)
        return enrollment

    def getEnrollment(self, course):
        for enrollment in self.enrolls:
            if enrollment.getCourse() == course:
                return enrollment
        return None

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
        courses += "ID:     {} Name: {}\n".format(self.ID, self.name)
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

class Course(persistent.Persistent):
    def __init__(self, course_id, name , credit=3, assignments=[], rooms = []):
        self.credit = credit
        self.course_id = course_id
        self.name = name
        self.assignments = assignments
        self.rooms = rooms
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
        print("ID:{}, Course:{},Credit: {}".format(self.course_id, self.name, self.credit))

    def scoreGrading(self, score):
        for grade in self.gradeScheme:
            if score >= grade["min"] and score <= grade["max"]:
                return grade["Grade"]
        return None
    
    def setGradeScheme(self, gradeScheme):
        self.gradeScheme = gradeScheme
        
    def addRoom(self, roomID):
        self.rooms.append(roomID)
        
    def removeRoom(self, roomID):
        self.rooms.remove(roomID)

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
    
    def addAssignment(self, assignment):
        self.assignments.append(assignment)
        self._p_changed = True

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

class Assignment(persistent.Persistent):
    def __init__(self, ID, name, max_score, due_date, attachment=[] , submitted_work={}, description="No Description"):
        self.id = ID
        self.name = name
        self.max_score = max_score
        self.due_date = due_date
        self.attachment = attachment
        self.submitted_work = submitted_work
        self.description = description

    def summitWork(self, studentId, work):
        self.submitted_work[studentId] = {"work": work, "score": 0}
        self._p_changed = True

    def unSummitWork(self, student):
        #delete the submitted work from upload folder
        for work in self.submitted_work[student]["work"]:
            os.remove(work)
        # print(self.submitted_work)
        self.submitted_work.pop(student)
        self._p_changed = True

    def grading(self, student, score):
        #check whether student has submitted work
        if student not in self.submitted_work.keys():
            return False
        self.submitted_work[student]["score"] = score
        self._p_changed = True
        return True

    def setName(self, name):
        self.name = name

    def setDueDate(self, due_date):
        if len(due_date.split("-")) != 3 and len(due_date) != 10 and len(due_date.split("-")[0]) != 4:
            self.due_date = date.today()
        else:
            self.due_date = due_date
        

    def setDescription(self, description):
        self.description = description

    def getDesciption(self):
        return self.description

    def setAttachment(self, attachment):
        self.attachment = attachment

    def removeAttachment(self):
        if len(self.attachment) > 0:
            for file in self.attachment:
                os.remove(file)
        self.attachment = []
        self._p_changed = True

    def getWorkScore(self, student):
        return self.submitted_work[student]["score"]
    
    def checkSubmitted(self, student):
        if student in self.submitted_work:
            return "Summited"
        return "Not Summited"
    
    def haveAttachment(self):
        return len(self.attachment) > 0
    
class Room(persistent.Persistent):
    def __init__(self, ID, title):
        self.id = ID
        self.title = title
    
    def setTitle(self, title):
        self.title = title
    
    def delete(self):
        del self
        self._p_changed = True

gradeScheme = [
    {"Grade": "A", "min":80, "max":100},
    {"Grade": "B", "min":70, "max":79}, 
    {"Grade": "C", "min":60, "max":69}, 
    {"Grade": "D", "min":50, "max":59}, 
    {"Grade": "F", "min":0, "max":49}
]
