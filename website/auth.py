from flask import Blueprint, render_template, request
from flask import flash # flashing message
from flask import redirect, url_for  # redirect webpage after submitting form
from .models import User #importing database models to auth
from werkzeug.security import generate_password_hash, check_password_hash #importing password hash security feature
from . import db  #from app package root folder import db
from flask_login import login_user,login_required,logout_user,current_user #importing user login and logout modules; current_user model interacts with db usermixin module

auth = Blueprint('auth', __name__)

# defining request types accepted in the route, by default, Get request only
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # access form attribute of request
        username = request.form.get('UserName')
        password = request.form.get('password')
        user = User.query.filter_by(user_name = username).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!', category= 'success')
                login_user(user,remember=True) #flask server remembers user login in
                return redirect( url_for( 'views.home' ) )
            else:
                flash('Incorrect password, try again!!',category='error')
        else:
            flash( 'User does not exist, please sign up!!', category='error' )

    return render_template("login.html", user = current_user)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # access form attribute of request
        username = request.form.get('UserName')
        password1 = request.form.get('password1')
        password2 = request.form.get( 'password2' )
        user = User.query.filter_by( user_name=username ).first()
        if user:
            flash( 'User name already exists. Please try a different one!!', category='error' )
        elif len(username) < 2:
            flash('User name needs to have more than 1 character',category='error')
        elif len(password1) < 6 or len(password1) > 12:
            flash('Password length needs to be between 6 - 12 characters',category='error')
        elif password1 != password2:
            flash( 'Passwords do not match!', category='error' )
        else:
            new_user = User(user_name = username,password = generate_password_hash(password1))
            db.session.add(new_user) #adding new user data to database table
            db.session.commit()
            flash( 'your account has been created successfully!', category='success' )
            login_user( new_user, remember=True )  # flask server remembers user login in
            return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)

@auth.route('/logout')
@login_required #checking if user login already before logging out
def logout():
    logout_user()
    return redirect(url_for('auth.login'))