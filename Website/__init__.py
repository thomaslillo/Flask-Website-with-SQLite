from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# setting up the database
db = SQLAlchemy()
DB_NAME = "database.db"

# initializing flask
def create_app():
    app = Flask(__name__)
    # encryption config variable
    app.config['SECRET_KEY'] = "shh"
    # configure SQLite db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # import the views
    from .views import views
    from .auth import auth
    
    # register the blueprints with the flask application
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # run and define the database classes - if you import a relative file (.something) you need import things individually
    from .models import User, Note
       
    # create the db if it does not exist
    create_db(app)
    
    # LOGING IN & STUFF
    login_manager = LoginManager()
    # where to send people if they read a page they need to login for (has the login_required decorator)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # tells flask how to load a user - check 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# run the database
def create_db(app):
    # if it does not exist make it do the existing
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("DB Created")