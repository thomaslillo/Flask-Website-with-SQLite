from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.wrappers import Request
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user

# for password storage security
from werkzeug.security import generate_password_hash, check_password_hash

# this file is a blueprint of the application, defining how all the files are organized
auth = Blueprint('auth', __name__)

## ROUTES

@auth.route('/login', methods=["GET","POST"])
def login():
    # if the person is posting data (signing in)
    if request.method == 'Post':
        email = request.form.get('email')
        password = request.form.get('password')
        # check if user email is valid
        user = User.query.filter_by(email=email).first()
        # if a user if found
        if user:
            if check_password_hash(user.password, password):
                flash('signed in', category='success')
                # call the login user function - remembers user in session info until cleared
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('not signed in', category='error')
        else:
            flash('you aint in the records', category='error')
            
    # here is where you return the specific template and any additional variables that you need to be accessible 
    # within the template, you can access these variables within the templates youre passing them variables to
    return render_template("login.html", text="Testing", boolean=True)

@auth.route('/logout')
@login_required # function decorator - requires login for the page to be accessible 
def logout():
    # logout the user - clear from session and return to login page
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=["GET","POST"])
def register():
    # if there is data in the post request from the form take in the info
    # at this stage I can do data validation for my form input
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        # data validation prior to writing to the database
        if user:
            flash('This email is already staying here', category='error')
        elif len(email) < 4:
            # send a message to the user on the screen
            flash('email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 3:
            flash('Password must be longer than 3 characters.', category='error')
        else:
            # create a new user
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256')) # with pwd hash sha256
            db.session.add(new_user)
            db.session.commit()
            # success message
            flash('Welcome to the tavern!', category='success')
            # redirect the user to the main page - url_for finds the url for the home page (views.home function in this case so its dynamic)
            return redirect(url_for('views.home'))
    # the register page
    return render_template("register.html")
