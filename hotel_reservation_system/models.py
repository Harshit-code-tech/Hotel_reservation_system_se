# models.py
from pymongo import MongoClient
from config import Config
from bson.objectid import ObjectId

# MongoDB client initialization
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB]

class Hotel:
    @staticmethod
    def get_all_hotels():
        return list(db.hotels.find())

    @staticmethod
    def get_hotel_by_id(hotel_id):
        return db.hotels.find_one({"_id": ObjectId(hotel_id)})

    @staticmethod
    def create_hotel(data):
        return db.hotels.insert_one(data)

    @staticmethod
    def delete_hotel(hotel_id):
        return db.hotels.delete_one({"_id": ObjectId(hotel_id)})

class Room:
    @staticmethod
    def get_room_by_id(room_id):
        return db.rooms.find_one({"_id": ObjectId(room_id)})

    @staticmethod
    def get_rooms_by_hotel(hotel_id):
        return list(db.rooms.find({"hotel_id": ObjectId(hotel_id)}))

    @staticmethod
    def check_availability(room_id, start_date, end_date):
        reservation = db.reservations.find_one({
            "room_id": ObjectId(room_id),
            "check_in": {"$lt": end_date},
            "check_out": {"$gt": start_date}
        })
        return reservation is None

    @staticmethod
    def create_room(data):
        return db.rooms.insert_one(data)

    @staticmethod
    def delete_room(room_id):
        return db.rooms.delete_one({"_id": ObjectId(room_id)})

class Reservation:
    @staticmethod
    def create_reservation(data):
        return db.reservations.insert_one(data)

    @staticmethod
    def get_reservation_by_id(reservation_id):
        return db.reservations.find_one({"_id": ObjectId(reservation_id)})

    @staticmethod
    def get_reservations_by_customer(customer_id):
        return list(db.reservations.find({"customer_id": ObjectId(customer_id)}))

    @staticmethod
    def cancel_reservation(reservation_id):
        return db.reservations.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": {"status": "Cancelled"}}
        )

    @staticmethod
    def delete_reservation(reservation_id):
        return db.reservations.delete_one({"_id": ObjectId(reservation_id)})

class Customer:
    @staticmethod
    def register_customer(data):
        return db.customers.insert_one(data)

    @staticmethod
    def login(email, password):
        customer = db.customers.find_one({"email": email})
        if customer and customer['password'] == password:
            return customer
        return None

    @staticmethod
    def delete_customer(customer_id):
        return db.customers.delete_one({"_id": ObjectId(customer_id)})

class Payment:
    @staticmethod
    def process_payment(data):
        return db.payments.insert_one(data)

    @staticmethod
    def get_payment_by_reservation(reservation_id):
        return db.payments.find_one({"reservation_id": ObjectId(reservation_id)})

    @staticmethod
    def delete_payment(payment_id):
        return db.payments.delete_one({"_id": ObjectId(payment_id)})
