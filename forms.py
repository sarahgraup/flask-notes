"""form for users"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Optional, Length, Email


class RegisterUser(FlaskForm):
    """form for registering/creating a new user"""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=5, max=100)]
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(min=5, max=50)]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=1, max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=1, max=30)]
    )


class LoginForm(FlaskForm):
    """ Form for logging in user"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=5, max=100)]

    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""


class NoteForm(FlaskForm):
    """form for creating notes""" #add that the form is also for editing as well 

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(min=1, max=100)]
    )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()]
    )
