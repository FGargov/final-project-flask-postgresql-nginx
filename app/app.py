from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
import os

from config import get_database_url
from models import db, Quiz, Question, Answer, Result

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db.init_app(app)
migrate = Migrate(app, db)

# Initialize database schema on startup
with app.app_context():
    print("APP: Before db.create_all()")
    db.create_all()
    print("APP: After db.create_all()")
    quiz_count = Quiz.query.count()
    print(f"APP: Quiz count before populating: {quiz_count}")
    if quiz_count == 0:
        print("APP: Condition Quiz.query.count() == 0 is TRUE. Importing sample_data...")
        from sample_data import populate_sample_data

        populate_sample_data()
    else:
        print("APP: Condition Quiz.query.count() == 0 is FALSE. Skipping sample_data.")


@app.route("/")
def index():
    quizzes = Quiz.query.all()
    return render_template("index.html", quizzes=quizzes)


@app.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        quiz = Quiz(title=title, description=description)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("add_question", quiz_id=quiz.id))
    return render_template("create_quiz.html")


@app.route("/add_question/<int:quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == "POST":
        text = request.form.get("text")
        question = Question(text=text, quiz_id=quiz_id)
        db.session.add(question)
        db.session.commit()
        answers = request.form.getlist("answers")
        correct = request.form.get("correct")
        for i, answer_text in enumerate(answers):
            if answer_text:
                answer = Answer(
                    text=answer_text, question_id=question.id, is_correct=(str(i) == correct)
                )
                db.session.add(answer)
        db.session.commit()
        if "add_another" in request.form:
            return redirect(url_for("add_question", quiz_id=quiz_id))
        return redirect(url_for("index"))
    return render_template("add_question.html", quiz=quiz)


@app.route("/take_quiz/<int:quiz_id>", methods=["GET", "POST"])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == "POST":
        user_name = request.form.get("user_name")
        score = 0
        total_questions = len(quiz.questions)
        for question in quiz.questions:
            answer_id = request.form.get(f"answer_{question.id}")
            if answer_id:
                answer = Answer.query.get(answer_id)
                if answer and answer.is_correct:
                    score += 1
        result = Result(
            quiz_id=quiz_id, user_name=user_name, score=score, total_questions=total_questions
        )
        db.session.add(result)
        db.session.commit()
        return redirect(url_for("view_results", quiz_id=quiz_id))
    return render_template("take_quiz.html", quiz=quiz)


@app.route("/results/<int:quiz_id>")
def view_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    results = Result.query.filter_by(quiz_id=quiz_id).order_by(Result.score.desc()).all()
    return render_template("results.html", quiz=quiz, results=results)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
