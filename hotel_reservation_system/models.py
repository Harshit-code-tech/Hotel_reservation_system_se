from flask import current_app

class Hotel:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    @staticmethod
    def create_hotel(data):
        db = current_app.db
        return db.hotels.insert_one(data)

    @staticmethod
    def get_all_hotels():
        db = current_app.db
        return db.hotels.find()

class Room:
    def __init__(self, room_number, price_per_night, hotel_id):
        self.room_number = room_number
        self.price_per_night = price_per_night
        self.hotel_id = hotel_id

    @staticmethod
    def create_room(data):
        db = current_app.db
        return db.rooms.insert_one(data)

    @staticmethod
    def check_availability(room_id):
        db = current_app.db
        return db.rooms.find_one({'_id': room_id, 'is_available': True})

class Reservation:
    def __init__(self, room_id, customer_name, check_in, check_out):
        self.room_id = room_id
        self.customer_name = customer_name
        self.check_in = check_in
        self.check_out = check_out

    @staticmethod
    def create_reservation(data):
        db = current_app.db
        return db.reservations.insert_one(data)

    @staticmethod
    def get_reservations_by_customer(customer_id):
        db = current_app.db
        return db.reservations.find({'customer_id': customer_id})

class Customer:
    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

    @staticmethod
    def register_customer(data):
        db = current_app.db
        return db.customers.insert_one(data)

    @staticmethod
    def login(email):
        db = current_app.db
        return db.customers.find_one({'email': email})
