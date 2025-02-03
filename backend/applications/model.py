from applications.database import db
from datetime import datetime
from flask_security import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def verify_password(self, password):
        """Verify the password against the hashed password in the database."""
        if not isinstance(password, str):
            raise ValueError("Password must be a string")
        return check_password_hash(self.password, password)

    def set_password(self, password):
        """Hash and set the password for the user."""
        if not isinstance(password, str):
            raise ValueError("Password must be a string")
        self.password = generate_password_hash(password)

    def has_role(self, role_name):
        """Check if the user has a specific role."""
        return any(role.name == role_name for role in self.roles)


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permissions = db.Column(db.String(255), nullable=True)  # Example: "read,write,delete"

    def get_permissions(self):
        """Return a list of permissions associated with the role."""
        return self.permissions.split(',') if self.permissions else []


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete")


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    difficulty_level = db.Column(db.String(50), nullable=True)  # Easy, Medium, Hard
    time_limit = db.Column(db.Integer, nullable=True)  # In minutes
    total_marks = db.Column(db.Integer, nullable=True)  # Total quiz marks
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete")
    date = db.Column(db.Date, nullable=True)  # Date of the quiz
    duration = db.Column(db.Time, nullable=True)

    def calculate_total_marks(self):
        """Calculate total marks based on questions."""
        return sum(question.marks for question in self.questions)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(10), nullable=False)  # A, B, C, or D
    explanation = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, nullable=True)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer)
    total_time_taken = db.Column(db.Integer)  # Time taken in minutes
    user = db.relationship('User', backref='scores')

    def percentage_score(self):
        """Calculate the percentage score for the quiz."""
        quiz = Quiz.query.get(self.quiz_id)
        if quiz and quiz.total_marks:
            return (self.total_scored / quiz.total_marks) * 100
        return 0



