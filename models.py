from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db, login_manager
from sqlalchemy.orm import validates
from re import match


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    article = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default="user")

    def __init__(self, name, email, password, image="default.jpg", role="user"):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.image = image
        self.role = role

    @validates("name")
    def validate_name(self, key, value):
        if not 2 < len(value) < 60:
            raise ValueError("Name must be more than 2 and less than 60 characters! ")
        return value

    @validates("email")
    def validate_email(self, key, value):
        valid = match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value)
        if not valid:
            raise ValueError("Email must be valid!")

        return value

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

    @staticmethod
    def hashPassword(password):
        return generate_password_hash(password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    blog = db.Column(db.Integer, nullable=False)
    comment_content = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

    @validates("comment_content")
    def validate_comment_content(self, key, value):
        if not 2 < len(value) < 10000:
            raise ValueError("Comment must be more than 2 characters long! ")
        return value


class Up_votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    blog = db.Column(db.Integer, nullable=False)
    blog_owner = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return


class Down_votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    blog = db.Column(db.Integer, nullable=False)
    blog_owner = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return


class Comment_Up_Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return


class Comment_Down_Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
