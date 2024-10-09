import sqlite3

from readData import Docs

class Database:
    
    def __init__(self):
        
        self.connect = sqlite3.connect("database.db")
        self.cursor = self.connect.cursor()
        
    
    
    def init_student_table(self):
        cursor = self.cursor
        
        cursor.execute("""
                    create table if not exists Student
                    (student_id TEXT PRIMARY KEY,
                    dept TEXT)""")
        self.connect.commit()
        
        
    
    def init_semester_table(self):
        cursor = self.cursor
        
        cursor.execute("""
                    create table if not exists Semester
                    (semester_id INTEGER PRIMARY KEY,
                    semester TEXT UNIQUE)""")
        self.connect.commit()
        
    
    def init_course_table(self):
        cursor = self.cursor
        
        cursor.execute("""
                    create table if not exists Course
                    (course_id INTEGER PRIMARY KEY,
                    course_name TEXT UNIQUE,
                    course_code TEXT UNIQUE,
                    category TEXT,
                    description TEXT,
                    prerequisite TEXT,
                    lab TEXT,
                    dept TEXT)""")
        self.connect.commit()
        
    
    def init_student_semester_table(self):
        
        cursor = self.cursor
        
        cursor.execute("""
                    create table if not exists Student_Semester
                    (
                    student_id text,
                    semester_id INTEGER,
                    PRIMARY KEY (student_ID, semester_id),
                    FOREIGN KEY (student_id) REFERENCES Student(student_id),
                    FOREIGN KEY (semester_id) REFERENCES Semester(semester_id))""")
        self.connect.commit()
        
    
    def init_student_course_table(self):
        cursor = self.cursor
        
        
        
        cursor.execute("""
                    create table if not exists Student_Course
                    (
                    student_id TEXT,
                    semester_id INTEGER,
                    course_id INTEGER,
                    PRIMARY KEY (student_id, semester_id, course_id),
                    FOREIGN KEY (student_id) REFERENCES Student(student_id),
                    FOREIGN KEY (semester_id) REFERENCES Semester(semester_id),
                    FOREIGN KEY (course_id) REFERENCES Course(course_id)    
                        )""")
        self.connect.commit()
        
        
    
    def init_course_table_items(self):
        
        d = Docs()
        
        courses = d.get_courses()
        
        
        cursor = self.cursor
        
        for code, name in courses:
            
            cursor.execute("""
                        insert or ignore into Course(course_name, course_code) values (?,?)
                        """, (name, code))
        
        self.connect.commit()
    
    
    
    def put_student_info(self, info):
        
        """
        SAMEPLE INFO::::
        info = {
        "id" : "22299513",
        "dept" : "CSE",
        "Courses" : {
            
            "FALL2022" : ["CSE110", "ENG101", "MAT110"],
            "SPRING2023" : ["PHY111", "CSE111", "CSE260", "CSE230"],
            "FALL2023" : ["CSE220", "BUS102", "STA201", "MAT120"]
        }
}"""    

        cursor = self.cursor
        
        
        #Inserting ID and DEPT
        cursor.execute("""
                    insert or ignore into Student values (?,?)""", (info['id'], info['dept']))
        
        
        #INSERTING SEMESTER FIRST
        
        for semester, courses in info['courses'].items():
            
            #Checking if semester already exists, if not then insert, if yes then ignore
            cursor.execute("insert or ignore into Semester(semester) values(:sem)", {"sem" : semester})
            
            #Establishing Student_Semester Relation
            
            cursor.execute("""
                        insert or ignore into Student_Semester(student_id, semester_id) values 
                        (:student_id, (select semester_id from Semester where semester = :sem))""",
                        {"student_id" : info["id"], "sem" : semester})
            
            
            
            #ESTABLISHING STUDENT COURSE RELATION
            
            for course in courses:
                
                #checking if course exists
                cursor.execute("insert or ignore into Course(course_code) values(:course)", {'course' : course})        
        
                
                cursor.execute("""
                            insert or ignore into Student_Course(student_id, semester_id, course_id) values ( :student_id, 
                                (select semester_id from Semester where semester = :sem),
                                (select course_id from Course where course_code = :course
                                    ))""", {"student_id" : info['id'], "sem" : semester, "course" : course})
        
        
        self.connect.commit()
    
    def courses_taken(self, info):
        
        """Returns the all of the courses the student has taken in a dictionary
        groued by semester"""
        
        
        cursor = self.cursor
        
        cursor.execute("""
                    select Semester.semester, Course.course_code
                    FROM Student
                    JOIN Student_Course ON Student.student_id = Student_Course.student_id
                    JOIN Semester ON Student_Course.semester_id = Semester.semester_id
                    JOIN Course ON Student_Course.course_id = Course.course_id
                    WHERE Student.student_id =:id""", {"id" : info["id"]})
        
        
        taken = cursor.fetchall()
        
        all_courses = {}
        
        for sem, code in taken:
            
            if sem in all_courses:
                all_courses[sem].append(code)
                
            else:
                all_courses[sem] = [code]
        
        return all_courses
        

    
    
    def courses_not_taken(self, info):
        
        """Returns all of the courses the student has not taken in a dictionary
        grouped by category // but first just send it via a list"""
        
        cursor = self.cursor
        
        cursor.execute("""
                    select Course.course_code
                    FROM Course
                    WHERE NOT EXISTS (
                        select *
                        FROM Student_Course
                        WHERE Student_Course.course_id = Course.course_id
                        AND Student_Course.student_id =:id
                        )""", {"id" : info["id"]})
        
        
        not_taken = cursor.fetchall()
        
        return not_taken
        


            
            
        
        
    
        
# db = Database()
# db.init_student_table()
# db.init_course_table()
# db.init_semester_table()
# db.init_student_course_table()
# db.init_student_semester_table()
# db.init_course_table_items()
