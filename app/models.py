from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Sample(db.Model):
    """
    Example model for demonstration. Replace or extend for your assignment.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
