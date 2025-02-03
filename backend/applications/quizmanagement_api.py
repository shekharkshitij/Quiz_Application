from flask_restful import Resource
from flask import request, jsonify
from applications.model import Subject, Chapter, Quiz, Question, Score
from applications.database import db
from flask_cors import cross_origin
from datetime import datetime
import jwt
import logging

logging.basicConfig(level=logging.INFO)

# JWT Configuration
SECRET_KEY = "your_secret_key"  # Replace with a secure secret key


# Middleware for JWT Authenticationdef auth_token_required(func):
def auth_token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            logging.warning("Missing token in request headers.")
            return {"message": "Authorization token is required"}, 401

        try:
            token = token.split(" ")[1]  # Remove 'Bearer' prefix
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            logging.info(f"Decoded token payload: {payload}")
            request.user = payload
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired.")
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token: {str(e)}")
            return {"message": "Invalid token"}, 401

        return func(*args, **kwargs)
    return wrapper




# Middleware for Role-Based Access Control
def roles_required(required_role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_role = request.user.get("role")
            if user_role != required_role:
                return {"message": "Access denied: insufficient privileges"}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Questions By Quiz
class QuestionsByQuiz(Resource):
    @auth_token_required
    def get(self, quiz_id):
        """Fetch questions for a specific quiz."""
        try:
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            if not questions:
                return {"message": "No questions found for this quiz."}, 404
            return jsonify([
                {
                    'id': question.id,
                    'text': question.question_text,
                    'options': [question.option1, question.option2, question.option3, question.option4],
                    'correct_option': question.correct_option
                }
                for question in questions
            ])
        except Exception as e:
            return {"error": str(e)}, 500


# All Subjects Management
class AllSubjects(Resource):
    @auth_token_required
    def get(self):
        """Fetch all subjects."""
        try:
            subjects = Subject.query.all()
            return jsonify([
                {
                    'id': subject.id,
                    'name': subject.name,
                    'description': subject.description,
                    'created_at': subject.created_at
                }
                for subject in subjects
            ])
        except Exception as e:
            logging.error(f"Error fetching subjects: {e}")
            return {"error": "An error occurred while fetching subjects."}, 500

    @auth_token_required
    @roles_required('admin')
    def post(self):
        """Add a new subject."""
        try:
            data = request.json
            if not data.get('name'):
                return {"message": "Subject name is required."}, 400

            if Subject.query.filter_by(name=data['name']).first():
                return {"message": "Subject with this name already exists."}, 409

            subject = Subject(
                name=data['name'],
                description=data.get('description', '')
            )
            db.session.add(subject)
            db.session.commit()
            return {"message": "Subject added successfully"}, 201
        except Exception as e:
            logging.error(f"Error adding subject: {e}")
            return {"error": "An error occurred while adding the subject."}, 500

    @auth_token_required
    @roles_required('admin')
    def put(self,subject_id):
        """Update an existing subject."""
        try:
            data = request.json
            subject = Subject.query.get_or_404(subject_id, description="Subject not found.")
            subject.name = data.get('name', subject.name)
            subject.description = data.get('description', subject.description)
            db.session.commit()
            return {"message": "Subject updated successfully"}, 200
        except Exception as e:
            logging.error(f"Error updating subject: {e}")
            return {"error": "An error occurred while updating the subject."}, 500

    @auth_token_required
    @roles_required('admin')
    def delete(self):
        """Delete a subject."""
        try:
            data = request.json
            subject_id = data.get('id')
            if not subject_id:
                return {"message": "Subject ID is required for deletion."}, 400

            subject = Subject.query.get_or_404(subject_id, description="Subject not found.")
            db.session.delete(subject)
            db.session.commit()
            return {"message": "Subject deleted successfully"}, 200
        except Exception as e:
            logging.error(f"Error deleting subject: {e}")
            return {"error": "An error occurred while deleting the subject."}, 500


# Chapter Management
class ChapterManagement(Resource):
    @auth_token_required
    def get(self, subject_id=None):
        """Fetch all chapters for a subject."""
        try:
            if subject_id is None:
                return {"message": "Subject ID is required as a URL parameter"}, 400

            chapters = Chapter.query.filter_by(subject_id=subject_id).all()
            if not chapters:
                return {"message": "No chapters found for this subject"}, 404

            return jsonify([
                {"id": chapter.id, "name": chapter.name, "description": chapter.description}
                for chapter in chapters
            ])
        except Exception as e:
            return {"error": str(e)}, 500


    @auth_token_required
    @roles_required('admin')
    def post(self):
        """Add a new chapter to a subject."""
        try:
            data = request.json
            chapter = Chapter(
                subject_id=data['subject_id'],
                name=data['name'],
                description=data.get('description', '')
            )
            db.session.add(chapter)
            db.session.commit()
            return {"message": "Chapter added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def put(self, chapter_id):
        """Update a chapter."""
        try:
            data = request.json
            chapter = Chapter.query.get_or_404(chapter_id)
            chapter.name = data.get('name', chapter.name)
            chapter.description = data.get('description', chapter.description)
            db.session.commit()
            return {"message": "Chapter updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def delete(self, chapter_id):
        """Delete a chapter."""
        try:
            chapter = Chapter.query.get_or_404(chapter_id)
            db.session.delete(chapter)
            db.session.commit()
            return {"message": "Chapter deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


# Quiz Management
class QuizManagement(Resource):
    @auth_token_required
    def get(self):
        """Fetch quizzes, optionally filter by chapter_id."""
        try:
            chapter_id = request.args.get("chapter_id")
            if chapter_id:
                quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
            else:
                quizzes = Quiz.query.all()

            if not quizzes:
                return {"message": "No quizzes found."}, 404

            return jsonify([
                {
                    "id": quiz.id,
                    "name": quiz.name,
                    "description": quiz.description,
                    "chapter_id": quiz.chapter_id
                }
                for quiz in quizzes
            ])
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def post(self):
        """Add a new quiz to a chapter."""
        try:
            data = request.json
            quiz = Quiz(
                chapter_id=data['chapter_id'],
                name=data['name'],
                description=data.get('description', ''),
                difficulty_level=data.get('difficulty_level', 'Medium'),
                time_limit=data.get('time_limit', 30),
                total_marks=data.get('total_marks', 100)
            )
            db.session.add(quiz)
            db.session.commit()
            return {"message": "Quiz added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def put(self, quiz_id):
        """Update a quiz."""
        try:
            data = request.json
            quiz = Quiz.query.get_or_404(quiz_id)
            quiz.name = data.get('name', quiz.name)
            quiz.description = data.get('description', quiz.description)
            quiz.difficulty_level = data.get('difficulty_level', quiz.difficulty_level)
            quiz.time_limit = data.get('time_limit', quiz.time_limit)
            quiz.total_marks = data.get('total_marks', quiz.total_marks)
            db.session.commit()
            return {"message": "Quiz updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def delete(self, quiz_id):
        """Delete a quiz."""
        try:
            quiz = Quiz.query.get_or_404(quiz_id)
            db.session.delete(quiz)
            db.session.commit()
            return {"message": "Quiz deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


# Question Management
class QuestionManagement(Resource):
    @auth_token_required
    def get(self, quiz_id):
        """Fetch all questions for a quiz."""
        try:
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            return jsonify([
                {
                    'id': question.id,
                    'text': question.question_text,
                    'options': [question.option1, question.option2, question.option3, question.option4],
                    'correct_option': question.correct_option,
                    'marks': question.marks
                }
                for question in questions
            ])
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def post(self):
        """Add a new question to a quiz."""
        try:
            data = request.json
            question = Question(
                quiz_id=data['quiz_id'],
                question_text=data['text'],
                option1=data['option1'],
                option2=data['option2'],
                option3=data['option3'],
                option4=data['option4'],
                correct_option=data['correct_option'],
                marks=data.get('marks', 1)
            )
            db.session.add(question)
            db.session.commit()
            return {"message": "Question added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def put(self, question_id):
        """Update a question."""
        try:
            data = request.json
            question = Question.query.get_or_404(question_id)
            question.question_text = data.get('text', question.question_text)
            question.option1 = data.get('option1', question.option1)
            question.option2 = data.get('option2', question.option2)
            question.option3 = data.get('option3', question.option3)
            question.option4 = data.get('option4', question.option4)
            question.correct_option = data.get('correct_option', question.correct_option)
            question.marks = data.get('marks', question.marks)
            db.session.commit()
            return {"message": "Question updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def delete(self, question_id):
        """Delete a question."""
        try:
            question = Question.query.get_or_404(question_id)
            db.session.delete(question)
            db.session.commit()
            return {"message": "Question deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


# Score Management
class ScoreManagement(Resource):
    @auth_token_required
    def get(self):
        """Fetch all scores."""
        try:
            scores = Score.query.all()
            return jsonify([
                {
                    'id': score.id,
                    'user_id': score.user_id,
                    'quiz_id': score.quiz_id,
                    'time_stamp_of_attempt': score.time_stamp_of_attempt,
                    'total_scored': score.total_scored,
                    'total_time_taken': score.total_time_taken
                }
                for score in scores
            ])
        except Exception as e:
            return {"error": str(e)}, 500

class QuizDetails(Resource):
    @auth_token_required
    def get(self, quiz_id):
        """Fetch quiz details and associated questions."""
        try:
            # Fetch quiz details
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                return {"message": "Quiz not found."}, 404

            # Fetch associated questions
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            question_list = [
                {
                    "id": q.id,
                    "text": q.question_text,
                    "options": [q.option1, q.option2, q.option3, q.option4],
                }
                for q in questions
            ]

            return {
                "quiz": {
                    "id": quiz.id,
                    "name": quiz.name,
                    "description": quiz.description,
                },
                "questions": question_list,
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500

class SubmitQuiz(Resource):
    @auth_token_required
    def post(self, quiz_id):
        """Submit quiz answers and calculate score."""
        try:
            # Parse JSON payload
            data = request.json
            answers = data.get("answers", {})
            time_taken = data.get("time_taken", 0)

            if not answers:
                return jsonify({"message": "Answers are required."}), 400

            # Fetch questions for the quiz
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            if not questions:
                return jsonify({"message": "No questions found for this quiz."}), 404

            # Evaluate answers
            score = 0
            total_questions = len(questions)

            for question in questions:
                question_id = str(question.id)
                correct_option = str(question.correct_option)

                if question_id in answers:
                    user_answer = str(answers[question_id])
                    if user_answer == correct_option:
                        score += 1
                    else:
                        print(f"Incorrect answer for question {question_id}: Expected {correct_option}, got {user_answer}")
                else:
                    print(f"Question {question_id} not answered.")

            # Save the score in the database
            new_score = Score(
                user_id=request.user["user_id"],  # Assuming JWT middleware sets user info
                quiz_id=quiz_id,
                total_scored=score,
                total_time_taken=time_taken,
                time_stamp_of_attempt=datetime.utcnow()
            )
            db.session.add(new_score)
            db.session.commit()

            # Return the response as JSON
            return {
                "message": "Quiz submitted successfully",
                "score": score,
                "total_questions": total_questions,
                "time_taken": time_taken,
            }, 200

        except Exception as e:
            print(f"Error during quiz submission: {str(e)}")
            return {
                "message": "Internal server error",
                "error": str(e),
            }, 500
