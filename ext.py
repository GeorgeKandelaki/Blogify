from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_misaka import Misaka


# Flask App and Configurations
app = Flask(__name__)
app.static_folder = "static"
app.config["SECRET_KEY"] = "i-love-to-write-code-i-love-writing-code"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogify.db"

# Markdown Support
Misaka(
    app, html=False, extensions=["tables", "fenced_code", "autolink", "strikethrough"]
)

# SQLAlchemy
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = "renderLogin"
