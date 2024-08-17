from app import db

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rooms = db.relationship('Room', backref='hotel', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

class Reservation:
    def __init__(self, room_id, customer_name, check_in, check_out):
        self.room_id = room_id
        self.customer_name = customer_name
        self.check_in = check_in
        self.check_out = check_out