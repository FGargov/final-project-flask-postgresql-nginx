from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Sample(db.Model):
    """
    Example model for demonstration. Replace or extend for your assignment.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


# --- Sample Quiz App Models ---
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
# -------------------------------------------------------------------
