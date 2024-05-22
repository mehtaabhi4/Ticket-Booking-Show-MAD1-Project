from datetime import datetime
from application import db
from flask_login import UserMixin


class Venue(db.Model):
    __tablename__ = 'Venue'
    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(150), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    no_of_screens = db.Column(db.Integer, nullable=False)

    bookings = db.relationship('Booking', backref='Venue', lazy=True)
    shows = db.relationship('Show', backref='Venue', lazy=True)

    def __init__(self, name, place, capacity, no_of_screens):
        self.venue_name = name
        self.place = place
        self.capacity = capacity
        self.no_of_screens = no_of_screens


class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    show_date = db.Column(db.Date, nullable=False)
    show_start_time = db.Column(db.Time, nullable=False)
    show_end_time = db.Column(db.Time, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(250), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_available = db.Column(db.Integer, nullable=False)

    # venue_id (integer, foreign key to Venue table)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'), nullable=False)
    bookings = db.relationship('Booking', backref='Show', lazy=True)

    # later use lazy=True argument in relationship

    def __init__(self, name, description, show_date, show_start_time, show_end_time, rating, tags, ticket_price,
                 venue_id):
        self.show_name = name
        self.description = description
        self.show_date = show_date
        self.show_start_time = show_start_time
        self.show_end_time = show_end_time
        self.rating = rating
        self.tags = tags
        self.ticket_price = ticket_price
        self.venue_id = venue_id
        self.ticket_available = Venue.query.filter_by(venue_id=venue_id).first().capacity


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    bookings = db.relationship('Show', backref='Venue', lazy=True)
    bookings = db.relationship('Booking', backref='User', lazy=True, viewonly=True)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password

    def get_id(self):
        return self.user_id


class Booking(db.Model):
    __tablename__ = 'Booking'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('Show.show_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False, default=0)
    total_ticket_price = db.Column(db.Float, nullable=False, default=0)
    user = db.relationship('User', backref='Booking')

    def __init__(self, user_id, show_id, venue_id, number_of_tickets, total_ticket_price):
        self.user_id = user_id
        self.show_id = show_id
        self.venue_id = venue_id
        self.number_of_tickets = number_of_tickets
        self.total_ticket_price = total_ticket_price
