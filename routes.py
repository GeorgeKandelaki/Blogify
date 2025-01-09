from flask import render_template, redirect, request, flash
from flask_login import login_user, logout_user, current_user, login_required


import os
from werkzeug.utils import secure_filename
from re import match
from uuid import uuid4


from sqlalchemy import and_

from ext import app, db
from utilities import get_votes, get_votes_blogs


from forms import (
    BlogForm,
    SignupForm,
    LoginForm,
    EditBlogForm,
    UpdateUserForm,
    ChangePasswordForm,
    CommentForm,
    UpdateCommentForm,
)


from models import (
    Blog,
    User,
    Comment,
    Up_votes,
    Down_votes,
    Comment_Up_Votes,
    Comment_Down_Votes,
    Bookmark,
)


@app.route("/login", methods=["GET", "POST"])
def renderLogin():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        else:
            flash("Password or Email is incorrect", "error")

    else:
        print(form.errors)

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def renderSignup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            role="user",
        )
        user.add()

        login_user(user, remember=True)
        return redirect("/")

    else:
        print(form.errors)

    return render_template("signup.html", form=form)


@app.route("/")
def renderOverview():
    page = request.args.get("page", 1, type=int)
    blogs_len = len(Blog.query.all())
    blogs = Blog.query.order_by(Blog.likes.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template(
        "overview.html",
        blogs=blogs.items,
        title="Home",
        page_name=f"All Blogs. Results: ({blogs_len}). Page: {page}",
        pagination=blogs,
    )


@app.route("/me")
@login_required
def renderUser():
    update_form = UpdateUserForm()
    password_form = ChangePasswordForm()

    return render_template(
        "profile.html",
        title="Profile",
        form1=update_form,
        form2=password_form,
    )


@app.route("/user/change_password", methods=["GET", "POST"])
@login_required
def changeCurrentUsersPassword():
    password_form = ChangePasswordForm()
    update_form = UpdateUserForm()

    if password_form.validate_on_submit():
        if 8 < len(password_form.new_password.data) < 80:
            current_user.password = User.hashPassword(password_form.new_password.data)
        else:
            flash("Password must be more than 8 and less than 80 characters!")

        db.session.commit()
        return redirect("/me")
    else:
        print(password_form.errors)

    return render_template(
        "profile.html",
        title="Profile",
        form1=update_form,
        form2=password_form,
    )


@app.route("/user/update_me", methods=["GET", "POST"])
@login_required
def updateCurrentUser():
    update_form = UpdateUserForm()
    password_form = ChangePasswordForm()

    if update_form.validate_on_submit():
        f = update_form.image.data
        image_name = "default_user.jpg"

        if f:
            filename, filetype = os.path.splitext(secure_filename(f.filename))
            filename = uuid4()
            image_name = f"{filename}{filetype}"
            filepath = os.path.join(
                app.root_path, "static", "images", "users", f"{filename}{filetype}"
            )
            f.save(filepath)
            current_user.image = image_name

        if 2 < len(update_form.name.data) < 60:
            current_user.name = update_form.name.data
        else:
            flash("Name must be more than 1 and less than 60 characters! ")

        if match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", update_form.email.data
        ):
            current_user.email = update_form.email.data
        else:
            flash("Must be a valid Email!")

        db.session.commit()
        return redirect("/me")
    else:
        print(update_form.errors)

    return render_template(
        "profile.html",
        title="Profile",
        form1=update_form,
        form2=password_form,
    )


@app.route("/my_blogs")
@login_required
def renderOwnedBlogs():
    blogs = (
        Blog.query.filter(Blog.user == current_user.id)
        .order_by(Blog.likes.desc())
        .all()
    )

    return render_template(
        "searched_blogs.html",
        blogs=blogs,
        title="My Blogs",
        page_name=f"My Blogs ({current_user.name}). Results: {len(blogs)}",
    )


@app.route("/blogs/<id>")
def renderBlog(id):
    blog = Blog.query.get(id)

    # If blog isn't found
    if not blog:
        return "<h1>404: Blog Not Found!</h1>"

    # 1) Get Blog Owner
    user = User.query.get(blog.user)

    # 2) Get Comments on the Blog and if it was bookmarked by current user
    comments = Comment.query.filter(Comment.blog == blog.id).all()
    bookmark = None

    # 3) Initialize the Comment Forms
    form = CommentForm()
    update_form = UpdateCommentForm()

    # 4) Initialize/Declare/Define comments interactions so if no user is logged in it will still be defined and won't error out
    comments_interactions = {"likes": [], "dislikes": []}
    comments_ids = {"likes": [], "dislikes": []}

    # 5) Initialize/Declare/Define interactions, so if no user is logged in it will still be defined and won't error out
    up_vote = []
    down_vote = []

    # 6) If user is authenticated then get the votes
    if current_user.is_authenticated:
        bookmark = Bookmark.query.filter(
            and_(current_user.id == Bookmark.user, blog.id == Bookmark.blog)
        ).first()

        up_vote = Up_votes.query.filter(
            and_(Up_votes.user == current_user.id, Up_votes.blog == id)
        ).first()
        down_vote = Down_votes.query.filter(
            and_(Down_votes.user == current_user.id, Down_votes.blog == id)
        ).first()

        # 7) If user is authenticated then get the comment votes
        comments_interactions["likes"] = Comment_Up_Votes.query.filter(
            and_(
                Comment_Up_Votes.user == current_user.id,
                Comment_Up_Votes.comment.in_([comment.id for comment in comments]),
            )
        ).all()

        comments_interactions["dislikes"] = Comment_Down_Votes.query.filter(
            and_(
                Comment_Down_Votes.user == current_user.id,
                Comment_Down_Votes.comment.in_([comment.id for comment in comments]),
            )
        ).all()

    # 8) Fill out the Likes and Dislikes, No no votes then it will be empty, meaning it won't error out because of variable not being Declared/Defined/Initialized
    comments_ids["likes"] = [
        interaction.comment for interaction in comments_interactions["likes"]
    ]

    comments_ids["dislikes"] = [
        interaction.comment for interaction in comments_interactions["dislikes"]
    ]

    # 9) Render Template with all the Properties
    return render_template(
        "blogpage.html",
        blog=blog,
        user=user,
        upvote=up_vote,
        downvote=down_vote,
        form=form,
        comments=comments,
        update_comment_form=update_form,
        comm_length=len(comments),
        disliked_comments=comments_ids["dislikes"],
        liked_comments=comments_ids["likes"],
        bookmark=bookmark,
    )


@app.route("/blogs/create", methods=["GET", "POST"])
@login_required
def renderBlogForm():
    form = BlogForm()

    if form.validate_on_submit():
        f = form.bg_image.data
        image_name = "default_blog.png"

        if f:
            filename, filetype = os.path.splitext(secure_filename(f.filename))
            filename = uuid4()
            image_name = f"{filename}{filetype}"
            filepath = os.path.join(
                app.root_path, "static", "images", "blogs", f"{filename}{filetype}"
            )
            f.save(filepath)

        blog = Blog(
            name=form.name.data,
            description=form.description.data,
            article=form.article.data,
            user=current_user.id,
            likes=0,
            dislikes=0,
            image=image_name,
        )
        blog.add()

        return redirect(f"/blogs/{blog.id}")
    else:
        print(form.errors)

    return render_template("blogCreate.html", form=form, title="Create Blog")


@app.route("/blogs/<id>/edit", methods=["GET", "POST"])
@login_required
def renderEditPage(id):
    blog = Blog.query.get(id)

    if blog.user != current_user.id and current_user.role != "admin":
        flash("You do not have a permission to edit someones post!", "error")
        return "<h1>401: You do not have permission to edit someones blog!"

    form = EditBlogForm()

    if form.validate_on_submit():
        blog.name = form.name.data
        blog.description = form.description.data
        blog.article = form.article.data

        f = form.bg_image.data
        image_name = "default_blog.png"

        if f:
            filename, filetype = os.path.splitext(secure_filename(f.filename))
            filename = uuid4()
            image_name = f"{filename}{filetype}"
            filepath = os.path.join(
                app.root_path, "static", "images", "blogs", f"{filename}{filetype}"
            )
            f.save(filepath)
            blog.image = image_name

        db.session.commit()
        return redirect(f"/blogs/{blog.id}")

    else:
        print(form.errors)

    return render_template("blogEdit.html", form=form, blog=blog)


@app.route("/blogs/<id>/delete")
@login_required
def deleteBlog(id):
    blog = Blog.query.get(id)

    if blog.user != current_user.id and current_user.role != "admin":
        flash("You do not have a permission to edit someones post!", "error")
        return "<h1>401: You do not have permission to edit someones blog!"

    Up_votes.query.filter(Up_votes.blog == blog.id).delete()
    Down_votes.query.filter(Down_votes.blog == blog.id).delete()
    Bookmark.query.filter(Bookmark.blog == blog.id).delete()

    comments = Comment.query.filter(Comment.blog == blog.id).all()
    comment_ids = [comment.id for comment in comments]

    if comment_ids:
        Comment_Up_Votes.query.filter(
            Comment_Up_Votes.comment.in_(comment_ids)
        ).delete()
        Comment_Down_Votes.query.filter(
            Comment_Down_Votes.comment.in_(comment_ids)
        ).delete()

    for comment in comments:
        db.session.delete(comment)

    db.session.delete(blog)

    db.session.commit()
    return redirect("/")


@app.route("/blogs/search")
def renderSearchedBlogs():
    name = request.args["s"]

    blogs = (
        Blog.query.filter(Blog.name.ilike(f"%{name}%"))
        .order_by(Blog.likes.desc())
        .all()
    )

    if not blogs:
        flash("No Blogs Found!")
        return render_template(
            "searched_blogs.html",
            page_name=f"No Blogs Found with the name of: '{name}', Results: 0",
        )

    return render_template(
        "searched_blogs.html",
        title="Home",
        page_name=f"Search Results for '{name}', Results: {len(blogs)}",
        blogs=blogs,
    )


def handle_vote(blog, user, vote_type):
    # Retrieve the vote state for the user and blog
    up_vote, down_vote = get_votes_blogs(user.id, blog.id)

    if vote_type == "up":
        if not up_vote and not down_vote:
            blog.likes += 1
            up_vote = Up_votes(user=user.id, blog=blog.id, blog_owner=blog.user)
            db.session.add(up_vote)
        elif up_vote:
            blog.likes -= 1
            db.session.delete(up_vote)
        elif down_vote:
            blog.dislikes -= 1
            blog.likes += 1

            db.session.delete(down_vote)
            up_vote = Up_votes(user=user.id, blog=blog.id, blog_owner=blog.user)
            db.session.add(up_vote)
    elif vote_type == "down":
        if not up_vote and not down_vote:
            blog.dislikes += 1
            down_vote = Down_votes(user=user.id, blog=blog.id, blog_owner=blog.user)
            db.session.add(down_vote)
        elif down_vote:
            blog.dislikes -= 1
            db.session.delete(down_vote)
        elif up_vote:
            blog.dislikes += 1
            blog.likes -= 1

            db.session.delete(up_vote)
            down_vote = Down_votes(user=user.id, blog=blog.id, blog_owner=blog.user)
            db.session.add(down_vote)

    db.session.commit()
    return


@app.route("/blogs/<id>/upvote")
@login_required
def upvote_blog(id):
    blog = Blog.query.get(id)

    if not blog:
        flash("Blog not found!", "error")
        return redirect("/blogs")

    handle_vote(blog, current_user, "up")
    return redirect(f"/blogs/{id}")


@app.route("/blogs/<id>/downvote")
@login_required
def downvote_blog(id):
    blog = Blog.query.get(id)
    if not blog:
        flash("Blog not found!", "error")
        return redirect("/blogs")

    handle_vote(blog, current_user, "down")
    return redirect(f"/blogs/{id}")


@app.route("/blogs/<id>/comment_create", methods=["POST"])
@login_required
def create_comment(id):
    blog = Blog.query.get(id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            user=current_user.id,
            user_name=current_user.name,
            blog=blog.id,
            comment_content=form.comment.data,
            likes=0,
            dislikes=0,
        )
        comment.add()
    else:
        print(form.errors)

    return redirect(f"/blogs/{id}")


@app.route("/comments/<id>/delete")
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)

    if comment.user != current_user.id and current_user.role != "admin":
        flash("You do not have a permission to delete someones post!", "error")
        return "<h1>401: You do not have permission to edit someones blog!"

    Comment_Up_Votes.query.filter(Comment_Up_Votes.comment == comment.id).delete()
    Comment_Down_Votes.query.filter(Comment_Down_Votes.comment == comment.id).delete()
    db.session.delete(comment)

    db.session.commit()
    return redirect(f"/blogs/{comment.blog}")


@app.route("/comments/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_comment(id):
    form = UpdateCommentForm()
    comment = Comment.query.get(id)

    if current_user.id != comment.user and current_user.role != "admin":
        flash("You do not have a permission to edit someones post!", "error")
        return "<h1>401: You do not have permission to edit someones blog!"

    if form.validate_on_submit():
        comment.comment_content = form.comment.data
        db.session.commit()
    else:
        print(form.errors)

    return redirect(f"/blogs/{comment.blog}")


def handle_comment_vote(comment, user, vote_type):
    # Retrieve the vote state for the user and comment
    up_vote, down_vote = get_votes(user.id, comment.id)

    if vote_type == "up":
        if not up_vote and not down_vote:
            comment.likes += 1
            up_vote = Comment_Up_Votes(user=user.id, comment=comment.id)
            db.session.add(up_vote)
        elif up_vote:
            comment.likes -= 1
            db.session.delete(up_vote)
        elif down_vote:
            comment.dislikes -= 1
            comment.likes += 1

            db.session.delete(down_vote)
            up_vote = Comment_Up_Votes(user=user.id, comment=comment.id)
            db.session.add(up_vote)
    elif vote_type == "down":
        if not up_vote and not down_vote:
            comment.dislikes += 1
            down_vote = Comment_Down_Votes(user=user.id, comment=comment.id)
            db.session.add(down_vote)
        elif down_vote:
            comment.dislikes -= 1
            db.session.delete(down_vote)
        elif up_vote:
            comment.likes -= 1
            comment.dislikes += 1

            db.session.delete(up_vote)
            down_vote = Comment_Down_Votes(user=user.id, comment=comment.id)
            db.session.add(down_vote)

    db.session.commit()
    return


@app.route("/comments/<id>/upvote")
@login_required
def upvote_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        flash("Comment not found!", "error")
        return redirect("/")

    handle_comment_vote(comment, current_user, "up")
    return redirect(f"/blogs/{comment.blog}")


@app.route("/comments/<id>/downvote")
@login_required
def downvote_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        flash("Comment not found!", "error")
        return redirect("/")

    handle_comment_vote(comment, current_user, "down")
    return redirect(f"/blogs/{comment.blog}")


@app.route("/user/logout")
@login_required
def logoutUser():
    logout_user()
    return redirect("/")


@app.route("/user/delete_me")
@login_required
def deleteUser():
    Blog.query.filter(current_user.id == Blog.user).delete()
    Comment.query.filter(current_user.id == Comment.user).delete()
    Up_votes.query.filter(current_user.id == Up_votes.user).delete()
    Down_votes.query.filter(current_user.id == Down_votes.user).delete()
    Comment_Up_Votes.query.filter(current_user.id == Comment_Up_Votes.user).delete()
    Comment_Down_Votes.query.filter(current_user.id == Comment_Down_Votes.user).delete()
    Bookmark.query.filter(current_user.id == Bookmark.user).delete()

    db.session.delete(current_user)
    db.session.commit()

    logout_user()
    return redirect("/")


@app.route("/user/<id>")
def renderUserProfile(id):
    user = User.query.get(id)

    if not user:
        return "<h1>404: User was not found!</h1>"

    user_blogs = Blog.query.filter(Blog.user == user.id).all()
    user_likes = Up_votes.query.filter(Up_votes.blog_owner == user.id).count()
    user_dislikes = Down_votes.query.filter(Down_votes.blog_owner == user.id).count()

    return render_template(
        "public_profile.html",
        user=user,
        blogs=user_blogs,
        blog_len=len(user_blogs),
        upvotes_len=user_likes,
        downvotes_len=user_dislikes,
    )


@app.route("/blogs/<id>/bookmark")
@login_required
def bookmarkBlog(id):
    bookmark = Bookmark.query.filter(
        and_(Bookmark.blog == id, Bookmark.user == current_user.id)
    ).first()

    if bookmark:
        bookmark.delete()
    else:
        bookmark = Bookmark(user=current_user.id, blog=id)
        bookmark.add()

    return redirect(f"/blogs/{id}")


@app.route("/my_bookmarks")
@login_required
def renderBookmarks():
    bookmarks = Bookmark.query.filter(current_user.id == Bookmark.user).all()
    blogs = []
    for bookmark in bookmarks:
        blogs.append(Blog.query.get(bookmark.blog))

    return render_template(
        "searched_blogs.html",
        blogs=blogs,
        title="My Bookmarks",
        page_name=f"My Bookmarks ({current_user.name}). Results: {len(blogs)}",
    )
