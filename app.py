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

#debug = DebugToolbarExtension(app)


connect_db(app)

seed_database(db)

empty_user = User(img_url="")


@app.get("/")
def show_homepage():
    """Shows homepage"""

    return redirect("/users")


@app.get("/users")
def show_user_list():
    """shows users of blog"""

    user_data = User.query.order_by("id").all()

    return render_template("user_listing.html", users=user_data)


@app.get("/users/new")
def show_add_user():
    """Shows add user form page"""

    action_type = "/users/new"

    return render_template("edit_user.html", title="Add User", user=empty_user, action=action_type)


@app.post("/users/new")
def add_new_user():
    """Adds new user to database"""

    add_user(request.form)

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Shows specific <user_id> details"""

    user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Shows user edit form"""

    action_type = f"/users/{user_id}/edit"

    return render_template("edit_user.html",
                           title="Edit User",
                           user=User.query.get_or_404(user_id),
                           action=action_type)


@app.post("/users/<user_id>/edit")
def edit_user(user_id):
    """Edits user data"""

    edit_user(request.form, user_id)

    return redirect("/users")


@app.post("/users/<user_id>/delete")
def delete_user(user_id):
    """Removes user data from db"""

    User.query.filter(User.id == user_id).delete()

    db.session.commit()

    return redirect("/users")


def add_user(user_data):
    """takes array of user data, and creates new User
    object, adding to db"""

    if user_data["img_url"] == "":
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"]
        )
    else:
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            img_url=user_data["img_url"]
        )

    db.session.add(new_user)
    db.session.commit()


def edit_user(new_user_data, user_id):
    """Queries db for user_id, alters information
    based on passed new_user_data"""

    user = User.query.get_or_404(user_id)

    user.first_name = new_user_data["first_name"]
    user.last_name = new_user_data["last_name"]

    if new_user_data != "":
        user.img_url = new_user_data["img_url"]
    else:
        user.img_url = "/static/default_pic.png"

    db.session.commit()
