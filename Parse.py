import re
import pypdf
import sqlite3

class Parse:
    
    def parsePDF(self, file):
        
        pdf = pypdf.PdfReader(file)


        page = pdf.get_page(0)
        page_text = page.extract_text()

        course_re = r"[A-Z]{3}[0-9]{3}"
        id_re = r"[0-9]{8}"
        semester_re = r"\b[A-Z]+ [0-9]{4}\b"
        
        dict = {}

        courses = []
        id = ""
        current_sem = ""
        
        
        for text in page_text.split("\n"):
            # print(text)
            id_match = re.search(id_re, text) 
            
            course = re.search(course_re, text)
            
            semester_match = re.search(semester_re, text)
            
            if semester_match:
                current_sem = semester_match.group()
            
            if current_sem and current_sem not in dict:
                dict[current_sem] = []
            

            if course:
                
                courses.append(course.group())
                dict[current_sem].append(course.group())
            

            if id_match:

                id = id_match.group()    
            

            

        self.info = {}
        self.info["courses"] = dict
        self.info["id"] = id
        self.info["dept"] = "CSE"
        
        


        return self.info
    
    def putCourse(self):
        #connect to database
        connect = sqlite3.connect('student.db')
        
        #connect  to cursor that is the anchor to do anything
        cursor = connect.cursor()
        
        #create a table
        cursor.execute("""
                       CREATE TABLE Students (
                           id text,
                           course blob)""")
        
        
        connect.commit()
        
        #close connection
        connect.close()

# connect = sqlite3.connect('student.db')

# cursor = connect.cursor()
        
# #create a table
# dict = {'FALL2020' : ['CSE110', 'CSE230']}

# cursor.execute("INSERT INTO Students VALUES ('22299513', dict)")
# # print(cursor.fetchall())
# connect.commit()

# #close connection
# connect.close()