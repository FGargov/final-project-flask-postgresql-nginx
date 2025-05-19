from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Sample(db.Model):
    """
    Example model for demonstration. Replace or extend for your assignment.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


# --- Sample Quiz App Models (for guidance only, do not implement) ---
# class Quiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(128), nullable=False)
#     questions = db.relationship('Question', backref='quiz', lazy=True)
#
# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(256), nullable=False)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     answers = db.relationship('Answer', backref='question', lazy=True)
#
# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(128), nullable=False)
#     is_correct = db.Column(db.Boolean, default=False)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
#
# class UserScore(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(64), nullable=False)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     score = db.Column(db.Integer, nullable=False)
# -------------------------------------------------------------------
