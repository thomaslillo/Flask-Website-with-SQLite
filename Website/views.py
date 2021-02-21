from flask import Blueprint, render_template
from flask_login import login_required, current_user

# this file is a blueprint of the application, defining how all the files are organized
views = Blueprint('views', __name__)

## defining the views

# the home page function
@views.route('/')
def home():
    # can pass the current user to make options in the template dynamic (eg only show link to specific user)
    # this can be done with "{% if user.is_authenticated %} <html> {% method %}" within the template
    return render_template("home.html", user=current_user)