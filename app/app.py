from flask import Flask

from .config import get_database_url
from .models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/health")
def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}, 200


# TODO: Implement quiz endpoints here

if __name__ == "__main__":
    # For local dev only; use Gunicorn in production
    app.run(host="0.0.0.0", port=5000)
