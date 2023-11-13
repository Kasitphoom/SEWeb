import persistent

class Client(persistent.Persistent):
    def __init__(self, ID, name, user_name, password, avatar=None):
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
    def __init__(self, ID, courses, name, user_name, password, avatar=None):
        super().__init__(ID ,name, user_name, password, avatar)
        self.courses = courses

    def setCourses(self, courses):
        self.courses = courses

    def addCourse(self, course):
        self.courses.append(course)
    

class Student(Client):
    def __init__(self, ID, enrolls, name, user_name, password, avatar=None):
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


gradeScheme = [
    {"Grade": "A", "min":80, "max":100},
    {"Grade": "B", "min":70, "max":79}, 
    {"Grade": "C", "min":60, "max":69}, 
    {"Grade": "D", "min":50, "max":59}, 
    {"Grade": "F", "min":0, "max":49}
]
