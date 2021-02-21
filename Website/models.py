# from the current package import db object
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# defining the schema of the db
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # get the current data and time and store it with func.now
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    # forign key - relationship between user and their notes (forign key is lower case)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # one to many relationship

class User(db.Model, UserMixin):
    # the primary key - unique
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # a relationship with the notes table
    notes = db.relationship('Note')