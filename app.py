"""Blogly application."""

from flask import Flask, redirect, request, render_template, flash
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

######
# User modifying/displaying routes
######
# User Display routes


@app.get("/users")
def show_user_list():
    """shows users of blog"""

    user_data = User.query.order_by("id").all()

    return render_template("user_templates/user_listing.html",
                           users=user_data)


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Shows specific <user_id> details"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).order_by('id').all()

    return render_template("user_templates/user_detail.html",
                           user=user, posts=posts)


# User add routes
@app.get("/users/new")
def show_add_user():
    """Shows add user form page"""

    action_type = "/users/new"

    return render_template("user_templates/edit_user.html",
                           title="Add User",
                           user=empty_user,
                           action=action_type)


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


# User Edit routes
@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Shows user edit form"""

    action_type = f"/users/{user_id}/edit"

    return render_template("user_templates/edit_user.html",
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

# User Delete Route


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

############
# User Post Routes
############


@app.get("/posts/<int:post_id>")
def show_post(post_id):
    """Shows post page"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_templates/post.html",
    post=post, user=post.user)


# Add Post Routes
@app.get("/users/<int:user_id>/posts/new")
def show_add_post(user_id):
    """Shows add post form for specific user"""

    user = User.query.get_or_404(user_id)

    return render_template("post_templates/add_post.html",
    user=user)


@app.post("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Adds new post to db, taking in user_id from url
       new post is related to passed user_id"""

    if(request.form["title"] == None or request.form["content"] == None):
        flash("Error: Title and Content must not be empty")
        return redirect(f"/users/{user_id}")

    post = Post(title=request.form["title"],
                content=request.form["content"],
                user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

# Edit Post Routes
@app.get("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Shows post edit page"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_templates/edit_post.html", post=post)


@app.post("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Edits specific user post"""
    post = Post.query.get_or_404(post_id)

    if(request.form["title"] == None or request.form["content"] == None):
        flash("Error: Title and Content must not be empty")
        return redirect(f"/users/{post.user_id}")

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Deletes post_id post"""

    user = Post.query.get_or_404(post_id).user
    post = Post.query.get_or_404(post_id)

    if not post:
        flash("Error, post does not exist")
        return redirect("/users")
    else:
        post.query.filter(Post.id == post_id).delete()
        db.session.commit()
        return redirect(f"/users/{user.id}")
