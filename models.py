"""Models for Blogly."""

from filecmp import DEFAULT_IGNORES
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "/static/default_pic.png"

db = SQLAlchemy()


class User(db.Model):
    """User class that extends SQLAlchemy models.
    contains user data including first and last name,
    and a img_url for profile pics"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    img_url = db.Column(db.Text,
                        nullable=False,
                        default=DEFAULT_IMAGE_URL)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
