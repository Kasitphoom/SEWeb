import persistent

class Client(persistent.Persistent):
    def __init__(self, ID, name, user_name, password, avatar):
        self.ID = ID
        self.name = name
        self.user_name = user_name
        self.password = password
        self.avatar = avatar

    def setAvatar(self, avatar):
        self.avatar = avatar

    def login(self, ID, password):
        print(self.password)
        if self.ID == ID and self.password == password:
            return True
        return False
    
    def setUsername(self, user_name):
        self.user_name = user_name

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
    def __init__(self, course_id, name , credit=3, assignments=[]):
        self.credit = credit
        self.course_id = course_id
        self.name = name
        self.assignments = assignments
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
    def __init__(self, name, max_score, due_date, attachment=[] , submitted_work=[],description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."):
        self.name = name
        self.max_score = max_score
        self.due_date = due_date
        self.attachment = attachment
        self.submitted_work = submitted_work
        self.description = description




gradeScheme = [
    {"Grade": "A", "min":80, "max":100},
    {"Grade": "B", "min":70, "max":79}, 
    {"Grade": "C", "min":60, "max":69}, 
    {"Grade": "D", "min":50, "max":59}, 
    {"Grade": "F", "min":0, "max":49}
]
