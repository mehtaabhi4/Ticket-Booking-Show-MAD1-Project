from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"

app.secret_key = "your_secret_key_here"

db = SQLAlchemy(app)

# from application import controllers
from application.controllers import *

with app.app_context():
    # create the database tables
    db.create_all()
    create_default_user()

    login_manager = LoginManager()
    login_manager.login_view = "ticket_booking_page"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
