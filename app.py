"""Blogly application."""

from flask import Flask, redirect, request, render_template
from models import db, connect_db, User
from seed import seed_database
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


connect_db(app)

seed_database(db)

@app.get("/")
def show_homepage():
    return redirect("/users")


@app.get("/users")
def show_user_list():
    """shows users of blog"""

    user_data = User.query.all()

    return render_template("user_listing.html", users = user_data)


@app.get("/users/new")
def show_add_user():
    """Shows add user form page"""

    return render_template("add_user.html")

@app.post("/users/new")
def add_new_user():
    """Adds new user to database"""
    if request.form["img_url"] == "":
        new_user = User(
            first_name = request.form["first_name"],
            last_name = request.form["last_name"]
        )
    else:
        new_user = User(
            first_name = request.form["first_name"],
            last_name = request.form["last_name"],
            img_url = request.form["img_url"]
        )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user(user_id):
    """shows specific <user_id> details"""

    user = User.query.get(user_id)
    return render_template("user_detail.html", user = user)

@app.get("/users/<user_id>/edit")
def show_edit_user(user_id):
    """Shows user edit form"""

    return render_template("edit_user.html")

@app.post("/users/<user_id>/edit")
def edit_user(user_id):
    return

@app.post("/users/<user_id>/delete")
def delete_user(user_id):
    return
