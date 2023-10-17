from datetime import datetime
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    contactnumber = db.Column(db.Integer)
    address = db.Column(db.String(15), unique=True, index=True, nullable=True)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

class Events(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='destination')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))