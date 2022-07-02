from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) #initiate app
    app.config['SECRET_KEY'] ='sdfhaksjdfh' #encript or secure the cookies of the webiste
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #configging database url
    db.init_app(app) #initiate database in app
    from .models import User, Vocabulary,Result  # importing database models/tables
    create_database( app )  #create database prior to logging in

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  #flask login manager default page for login
    login_manager.init_app(app) #initiate login manager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #query User database to load user by primary key id, similar to filter by
    #all neccessary codes to achieve @login_required function

    from .views import views #importing views blueprint from views.py
    from .auth import auth #importing auth blueprint from auth.py
    app.register_blueprint(views,url_prefix = '/')  #register blueprint without prefix
    app.register_blueprint(auth, url_prefix='/' )  # register blueprint without prefix
    return app

def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print("Database has been created!!")

