from flask import Flask, render_template, request, redirect, url_for
from models import db, Student, Course

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create a custom CLI command to initialize the database
@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized.")

# Student CRUD

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form['name']
        new_student = Student(name=name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students'))
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/<int:id>/edit', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('edit_student.html', student=student)

@app.route('/students/<int:id>/delete', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

# Course CRUD
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        name = request.form['name']
        new_course = Course(name=name)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('courses'))
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
def edit_course(id):
    course = Course.query.get_or_404(id)
    if request.method == 'POST':
        course.name = request.form['name']
        db.session.commit()
        return redirect(url_for('courses'))
    return render_template('edit_course.html', course=course)

@app.route('/courses/<int:id>/delete', methods=['POST'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('courses'))

# Enrollment
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)
        student.courses.append(course)
        db.session.commit()
        return redirect(url_for('view_enrollments'))
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('enroll.html', students=students, courses=courses)

@app.route('/view_enrollments')
def view_enrollments():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('view_enrollments.html', students=students, courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
