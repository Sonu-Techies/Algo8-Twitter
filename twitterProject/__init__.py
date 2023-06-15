from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

__engine = None
__connection = None
__user = 'root'
__pass = 'oy9Vyr1Yh0EhbGs6Ouza'
__host = 'containers-us-west-2.railway.app'
__port = 6495
__db = 'railway'


db = SQLAlchemy()



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = '4YrzfpQ4kGXjuP6w'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{__user}:{__pass}@{__host}:{__port}/{__db}'

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "username@gmail.com"
    app.config['MAIL_PASSWORD'] = "password"
    mail = Mail(app)
    # migrate = Migrate(app, db)
    db.init_app(app)
    # migrate.init_app(app, db)

    with app.app_context():
        from . import apiviews  # Import routes

        db.create_all()  # Create database tables for our data models

        return app