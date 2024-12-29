from models import User
from flask_login import current_user


from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    EmailField,
    FileField,
)

from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


# BlogForm
class BlogForm(FlaskForm):
    name = StringField(
        "Name of the blog...",
        validators=[
            DataRequired("Blog must have a name"),
            Length(
                min=5,
                max=80,
                message="Blog name must be more than 5 and less than 80 characters!",
            ),
        ],
    )
    description = StringField(
        "Small description of your post...",
        validators=[
            DataRequired("Blog must have a description"),
            Length(
                min=5,
                max=120,
                message="Blog Description must be more than 5 and less than 120 characters!",
            ),
        ],
    )
    article = TextAreaField(
        "Your article...",
        validators=[
            DataRequired("Blog must have an article in it"),
            Length(
                min=10,
                message="Blog Article must be equal to or more than 10 characters!",
            ),
        ],
    )
    bg_image = FileField(
        "Cover Image for your blog.",
        validators=[FileAllowed(["jpg", "png", "webp", "jpeg"])],
    )

    submit = SubmitField("Create Blog")


# EditBlogForm
class EditBlogForm(FlaskForm):
    name = StringField(
        "Name of the blog...",
        validators=[
            DataRequired("Blog must have a name"),
            Length(
                min=5,
                max=80,
                message="Blog name must be more than 5 and less than 80 characters!",
            ),
        ],
    )
    description = StringField(
        "Small description of your post...",
        validators=[
            DataRequired("Blog must have a description"),
            Length(
                min=5,
                max=120,
                message="Blog Description must be more than 5 and less than 120 characters!",
            ),
        ],
    )
    article = TextAreaField(
        "Your article...",
        validators=[
            DataRequired("Blog must have an article in it"),
            Length(
                min=10,
                message="Blog Article must be equal to or more than 10 characters!",
            ),
        ],
    )

    bg_image = FileField(
        "Update Cover Image.", validators=[FileAllowed(["jpg", "png", "webp", "jpeg"])]
    )

    submit = SubmitField("Edit Blog")


# LoginForm
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired("Email is necessary!")])
    password = PasswordField(
        "Password", validators=[DataRequired("Password is necessary!")]
    )

    submit = SubmitField("Log In")


# SignupForm
class SignupForm(FlaskForm):
    name = StringField(
        "Username",
        validators=[DataRequired("User must have a name!"), Length(min=3, max=50)],
    )
    email = EmailField(
        "Email",
        validators=[DataRequired("User must have an email!"), Length(min=3, max=100)],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("User must have a password!"),
            Length(min=8, max=100),
        ],
    )
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired("You must confirm your password!"),
            EqualTo("password", "Passwords are not the same!"),
        ],
    )

    submit = SubmitField("Sign Up")

    # Custom validator for duplicate email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is already taken. Please choose a different one."
            )


# UpdateUserForm
class UpdateUserForm(FlaskForm):
    name = StringField("Updated Name")
    email = EmailField("Updated Email")
    image = FileField(
        "Update Image", validators=[FileAllowed(["jpg", "png", "jpeg", "webp"])]
    )

    submit = SubmitField("SAVE SETTINGS")

    # Custom validator for duplicate email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError(
                "This email is already taken. Please choose a different one."
            )


# ChangePasswordForm
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Your Current Password...",
        validators=[DataRequired("Current Password is necessary to change password!")],
    )
    new_password = PasswordField(
        "New Password...",
        validators=[DataRequired("New Password is necessary to change password!")],
    )
    confirm_password = PasswordField(
        "Confirm New Password...",
        validators=[
            DataRequired("Confirming the Password is necessary to change password!"),
            EqualTo("new_password", "Passwords are not the same!"),
        ],
    )

    submit = SubmitField("CHANGE PASSWORD")

    # Custom validator for current password
    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValidationError("The current password is incorrect!")


# Comment Form
class CommentForm(FlaskForm):
    comment = TextAreaField(
        "Write Your Comment...",
        validators=[
            DataRequired("Comment must have a text in it!"),
            Length(min=2, max=10000),
        ],
    )

    submit = SubmitField("Comment")


# Update Comment Form
class UpdateCommentForm(FlaskForm):
    comment = TextAreaField(
        "Write Your Comment...",
        validators=[
            DataRequired("You have to update your comment."),
            Length(min=2, max=10000),
        ],
    )

    submit = SubmitField("Update Comment")
