from flask import Flask, jsonify, request
from flask_cors import CORS
from Parse import Parse
from database import Database
import os


app = Flask(__name__)
cors = CORS(app, origins = "*")


@app.route('/upload', methods = ["POST"] )
def receive_pdf():

    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # if file.filename == '':
    #     return jsonify({"error": "No file selected"}), 400

    
    # if file.filename.endswith('.pdf'):
    #     filename = file.filename
        

    #     filepath = os.getcwd()+"\\" + filename
    #     file.save(filepath)
        
    pdf = Parse()
    info = pdf.parsePDF(file)
    
    # if os.path.isfile(filepath):
    #     os.remove(filepath)
    

    
    db = Database()
    
    db.put_student_info(info)
    
    courses_taken = db.courses_taken(info)
    
    courses_not_taken = db.courses_not_taken(info)




    return jsonify(
    {
        "courses" : courses_taken,
        'not_taken' : courses_not_taken,
        'student_id' : info['id'],
        'dept' : info['dept']
    }) 
    
    return jsonify({"error": "Invalid file type"}), 400
    
    
    
    

    
if __name__ == "__main__":
    app.run(debug = True, port = 8080)