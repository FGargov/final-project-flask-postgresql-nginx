# Sample quiz app data for guidance only.
# Use this as a reference for your own seed/test data.

from models import db, Quiz, Question, Answer


def populate_sample_data():
    """Populate the database with sample quiz data for dev/testing."""
    # Clear existing data
    Answer.query.delete()
    Question.query.delete()
    Quiz.query.delete()
    db.session.commit()

    # Sample Quiz 1: General Knowledge
    quiz1 = Quiz(
        title="General Knowledge", description="Test your general knowledge with this quiz."
    )
    db.session.add(quiz1)
    db.session.commit()

    q1 = Question(text="What is the capital of France?", quiz_id=quiz1.id)
    db.session.add(q1)
    db.session.commit()
    db.session.add(Answer(text="London", question_id=q1.id, is_correct=False))
    db.session.add(Answer(text="Paris", question_id=q1.id, is_correct=True))
    db.session.add(Answer(text="Berlin", question_id=q1.id, is_correct=False))
    db.session.add(Answer(text="Madrid", question_id=q1.id, is_correct=False))

    q2 = Question(text="Which planet is known as the Red Planet?", quiz_id=quiz1.id)
    db.session.add(q2)
    db.session.commit()
    db.session.add(Answer(text="Earth", question_id=q2.id, is_correct=False))
    db.session.add(Answer(text="Mars", question_id=q2.id, is_correct=True))
    db.session.add(Answer(text="Jupiter", question_id=q2.id, is_correct=False))
    db.session.add(Answer(text="Saturn", question_id=q2.id, is_correct=False))

    # Commit all changes
    db.session.commit()
    print("Sample data populated: 1 quiz with 2 questions.")


sample_quizzes = [
    {"id": 1, "title": "General Knowledge"},
    {"id": 2, "title": "Science"},
]

sample_questions = [
    {"id": 1, "text": "What is the capital of France?", "quiz_id": 1},
    {"id": 2, "text": "What planet is known as the Red Planet?", "quiz_id": 2},
]

sample_answers = [
    {"id": 1, "text": "Paris", "is_correct": True, "question_id": 1},
    {"id": 2, "text": "London", "is_correct": False, "question_id": 1},
    {"id": 3, "text": "Mars", "is_correct": True, "question_id": 2},
    {"id": 4, "text": "Jupiter", "is_correct": False, "question_id": 2},
]

sample_user_scores = [
    {"id": 1, "user_name": "alice", "quiz_id": 1, "score": 1},
    {"id": 2, "user_name": "bob", "quiz_id": 2, "score": 1},
]

# Example usage (not for production):
# for quiz in sample_quizzes:
#     print(quiz["title"])
