from flask import Flask, jsonify
from flask_cors import CORS
from applications.model import User, Role
from applications.database import db
from applications.config import Config
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from applications.user_datastore import user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize Flask-RESTful API
    api = Api(app, prefix='/api/v1')
    app.security = Security(app, user_datastore)

    with app.app_context():
        # Create database tables
        db.create_all()

        # Create default roles
        try:
            admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
            user_role = user_datastore.find_or_create_role(name='user', description='Quiz User')

            # Create default admin user
            if not user_datastore.find_user(email="admin@quizmaster.com"):
                admin_password_hash = generate_password_hash("admin123")
                user_datastore.create_user(
                    email="admin@quizmaster.com",
                    username="admin",
                    password=admin_password_hash,
                    roles=[admin_role]
                )
            db.session.commit()
        except Exception as e:
            print(f"Error during default admin and role creation: {e}")

    # Add global error handling
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "An unexpected error occurred"}), 500

    return app, api


app, api = create_app()

# Import and register API resources
from applications.auth_api import Login, Register, Logout
from applications.quizmanagement_api import (
    AllSubjects,
    ChapterManagement,
    QuestionManagement,
    QuizManagement,
    ScoreManagement,
    QuizDetails,
    SubmitQuiz
)

# Auth API endpoints
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Logout, '/logout')

# Subject, Chapter, Quiz, Question, and Score Management endpoints
api.add_resource(AllSubjects, '/subjects', '/subjects/<int:subject_id>')
api.add_resource(ChapterManagement, '/chapters', '/chapters/<int:chapter_id>', '/chapters/subject/<int:subject_id>')

api.add_resource(QuizManagement, '/quizzes', '/quizzes/<int:quiz_id>')
api.add_resource(QuestionManagement, '/questions', '/questions/<int:question_id>', '/quizzes/<quiz_id>/questions')

api.add_resource(SubmitQuiz, '/quizzes','/quizzes/<int:quiz_id>/submit')

# Additional routes if needed

api.add_resource(ScoreManagement, '/scores')

if __name__ == '__main__':
    app.run(debug=True)
