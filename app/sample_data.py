# Sample quiz app data for guidance only.
# Use this as a reference for your own seed/test data.

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
