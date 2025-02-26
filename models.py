from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many relationship between students and courses
student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', secondary=student_course, backref=db.backref('students', lazy=True))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
