"""Models for User"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True,
        nullable=False)

    password = db.Column(
        db.String(100),
        nullable=False)

    email = db.Column(
        db.String(50),
        nullable=False)

    first_name = db.Column(
        db.String(30),
        nullable=False)

    last_name = db.Column(
        db.String(30),
        nullable=False)

    notes = db.relationship("Note", backref="owning_user")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        new_user = cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        # db.session.commit()
        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """ Validate user exists and password is correct
         return user if valid; else return False
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Note(db.Model):
    """Note"""

    # __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False)

    content = db.Column(
        db.Text,
        nullable=False)

    owner = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False)
