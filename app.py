"""Blogly application."""

from flask import Flask, redirect, request, render_template
from models import DEFAULT_IMAGE_URL, db, connect_db, User, Post
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

empty_user = User(first_name="", last_name="", img_url="")


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
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"] if request.form["img_url"] != "" else None

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        img_url=img_url
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Shows specific <user_id> details"""

    user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=user, posts=user.posts)


@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Shows user edit form"""

    action_type = f"/users/{user_id}/edit"

    return render_template("edit_user.html",
                           title="Edit User",
                           user=User.query.get_or_404(user_id),
                           action=action_type)


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edits user data"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"] if request.form["img_url"] != "" else DEFAULT_IMAGE_URL

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Removes user data from db"""

    user = User.query.filter(User.id == user_id).first()

    if not user:
        return redirect("/users")
    else:
        user.posts.clear()
        # user.query.delete()
        db.session.delete(user)
        db.session.commit()

        return redirect("/users")


@app.get("/posts/<int:post_id>")
def show_post(post_id):
    """shows post page"""

    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post, user_id=post.user_id)


@app.get("/users/<int:user_id>/posts/new")
def show_add_post(user_id):
    return
