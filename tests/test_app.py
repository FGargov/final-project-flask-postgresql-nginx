from models import Quiz, Question, Answer, Result, db


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Quiz" in response.data or b"quiz" in response.data


def test_404(client):
    response = client.get("/no-such-page")
    assert response.status_code == 404


def test_create_quiz_post_success(client):
    response = client.post(
        "/create_quiz",
        data={"title": "Test Quiz", "description": "Test Description"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test Quiz" in response.data


def test_create_quiz_post_missing_title(client):
    response = client.post(
        "/create_quiz",
        data={"title": "", "description": "No Title"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"required" in response.data or b"Title" in response.data


def test_add_question_get_valid_quiz(client):
    quiz = Quiz(title="Quiz for question", description="desc")
    db.session.add(quiz)
    db.session.commit()
    response = client.get(f"/add_question/{quiz.id}")
    assert response.status_code == 200
    assert b"Add Question" in response.data


def test_add_question_get_invalid_quiz(client):
    response = client.get("/add_question/99999")
    assert response.status_code == 404


def test_take_quiz_get(client):
    quiz = Quiz(title="Take Quiz", description="desc")
    db.session.add(quiz)
    db.session.commit()
    response = client.get(f"/take_quiz/{quiz.id}")
    assert response.status_code == 200
    assert b"Take Quiz" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
