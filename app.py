# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages

# In-memory "database" (use a file or real DB in production)
students = []

def save_students():
    with open('students.json', 'w') as f:
        json.dump(students, f, indent=2)

def load_students():
    global students
    try:
        with open('students.json', 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        pass  # Start with empty list

@app.before_first_request
def init_db():
    load_students()

@app.route('/')
def index():
    load_students()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name or not email:
            flash('Please fill in all fields.')
            return render_template('add_student.html')
        # Check for duplicate email
        existing = next((s for s in students if s['email'] == email), None)
        if existing:
            flash('Student with this email already exists.')
            return render_template('add_student.html')
        students.append({
            'id': len(students) + 1,
            'name': name,
            'email': email,
            'subjects': [],
            'scores': {}
        })
        save_students()
        flash('Student added successfully!')
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    global students
    load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        student['name'] = request.form['name']
        # Extend as needed for other fields
        save_students()
        flash('Student updated!')
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

# (Add more routes for tracking scores, attendance, etc.)

if __name__ == '__main__':
    app.run(debug=True)
