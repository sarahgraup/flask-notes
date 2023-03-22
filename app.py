import os
from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterUser, LoginForm, CSRFProtectForm, NoteForm
AUTH_KEY_NAME = "username"
app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///users')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Home page of site"""
    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """showing user registration form to register/create User
    handle submission of form
    """
    form = RegisterUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.commit()

        session[AUTH_KEY_NAME] = new_user.username

        flash(f"User {new_user.first_name} added!")
        return redirect(f"users/{new_user.username}")

    else:
        return render_template("register_user_form.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """show form to login user and handle submision of login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session[AUTH_KEY_NAME] = user.username
            return redirect(f"users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


@app.get("/users/<username>")
def show_user_page(username):
    """shows the user page and logout button"""

    if AUTH_KEY_NAME not in session or username != session[AUTH_KEY_NAME]:
        flash("You must be logged in to view!")
        return redirect("/")

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    return render_template("show.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()
    # breakpoint()

    if form.validate_on_submit():
        session.pop(AUTH_KEY_NAME)
        flash('user is popped')
        return redirect("/login")

    return redirect("/")


@app.post("/users/<username>/delete")
def delete_user(username):
    """delete user from database and redirect to base"""

    user = User.query.get_or_404(username) #move to 121

    if AUTH_KEY_NAME not in session or username != session[AUTH_KEY_NAME]:
        flash("You must be logged in to view!")
        return redirect("/")

    form = CSRFProtectForm()

    if form.validate_on_submit():

        Note.query.filter_by(owner=username).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop(AUTH_KEY_NAME)

        return redirect("/")
    else:
        return redirect(f"/users/{user.username}")


@app.route("/users/<username>/notes/add", methods=['GET', 'POST'])
def add_notes(username):
    """displays form to add notes and processes form"""

    if AUTH_KEY_NAME not in session or username != session[AUTH_KEY_NAME]:
        flash("You must be logged in to view!")
        return redirect("/")
    
    form = NoteForm()
    # breakpoint()


    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(
            title=title,
            content=content,
            owner=username
        )

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{note.owner}")
    else:
        return render_template("add_notes.html", form=form)


@app.route("/notes/<note_id>/update", methods=['GET', 'POST'])
def update_note(note_id):
    """displays form to update note and processes form"""

    note = Note.query.get_or_404(note_id)

    if AUTH_KEY_NAME not in session or note.owner != session[AUTH_KEY_NAME]:
        flash("You must be logged in to view!")
        return redirect("/")

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")
    else:
        return render_template("update.html", form=form, note=note)


@app.post("/notes/<note_id>/delete")
def delete_note(note_id):
    """deletes note and redirects to /users/<username>"""

    note = Note.query.get_or_404(note_id)

    if AUTH_KEY_NAME not in session or note.owner != session[AUTH_KEY_NAME]:
        flash("You must be logged in to view!")
        return redirect("/")

    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

    return redirect(f"/users/{note.owner}")

