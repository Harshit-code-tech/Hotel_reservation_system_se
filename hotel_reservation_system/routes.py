from flask import Blueprint, request, jsonify, render_template, current_app
from models import Hotel, Room, Reservation, Customer

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add_reservation', methods=['POST'])
def add_reservation():
    try:
        data = request.json
        # Validate required fields
        required_fields = ['room_id', 'customer_name', 'check_in', 'check_out']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Insert the reservation into MongoDB
        result = Reservation.create_reservation(data)
        return jsonify({'inserted_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        reservations = Reservation.get_reservations_by_customer(request.args.get('customer_id'))
        result = []
        for reservation in reservations:
            reservation['_id'] = str(reservation['_id'])  # Convert ObjectId to string
            result.append(reservation)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/hotels', methods=['GET'])
def get_hotels():
    try:
        hotels = Hotel.get_all_hotels()
        result = []
        for hotel in hotels:
            hotel['_id'] = str(hotel['_id'])
            result.append(hotel)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/hotel', methods=['POST'])
def add_hotel():
    try:
        data = request.json
        Hotel.create_hotel(data)
        return jsonify({'message': 'Hotel added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/room/availability/<room_id>', methods=['GET'])
def check_room_availability(room_id):
    try:
        room = Room.check_availability(room_id)
        if room:
            return jsonify({'available': True})
        else:
            return jsonify({'available': False})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/register', methods=['POST'])
def register_customer():
    try:
        data = request.json
        Customer.register_customer(data)
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        customer = Customer.login(data['email'])
        if customer and customer['password'] == data['password']:
            return jsonify({'message': 'Login successful'})
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
