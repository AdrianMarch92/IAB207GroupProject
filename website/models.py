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

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(400), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    ga_price = db.Column(db.Numeric, nullable=False)
    ga_availability = db.Column(db.Integer, nullable=False)
    concession_price = db.Column(db.Numeric, nullable=False)
    concession_availability = db.Column(db.Integer, nullable=False)
    vip_price = db.Column(db.Numeric, nullable=False)
    vip_availability = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(400), nullable=True)
    event_guidelines = db.Column(db.Text, nullable=True)
    terms_conditions = db.Column(db.Text, nullable=True)  
    status = db.Column(db.String(80), nullable=True)
    category = db.Column(db.String(80), nullable=True) 
    comments = db.relationship('Comment', backref='event')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref=db.backref('events', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "location": self.location,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "start_time": self.start_time.strftime('%H:%M:%S'),
            "end_time": self.end_time.strftime('%H:%M:%S'),
            "category": self.category
            # Add other fields as needed
        }

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ga_quantity = db.Column(db.Integer, default=0)
    concession_quantity = db.Column(db.Integer, default=0)
    vip_quantity = db.Column(db.Integer, default=0)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))