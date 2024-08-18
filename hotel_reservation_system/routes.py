# routes.py
from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

bp = Blueprint('routes', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.config.get('LOGGED_IN_USER'):
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        db = current_app.db
        user = db.users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            current_app.config['LOGGED_IN_USER'] = user['email']
            return redirect(url_for('routes.index'))
        elif not user:
            return redirect(url_for('routes.register'))
        return "Invalid credentials", 401
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        db = current_app.db
        if not db.users.find_one({'email': data['email']}):
            hashed_password = generate_password_hash(data['password'])
            db.users.insert_one({
                'name': data['name'],
                'email': data['email'],
                'password': hashed_password
            })
            return redirect(url_for('routes.login'))
        return "User already exists", 400
    return render_template('register.html')


@login_required
@bp.route('/')
def index():
    try:
        db = current_app.db
        hotels = db.hotels.find()
        return render_template('hotel_list.html', hotels=hotels)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@login_required
@bp.route('/hotel/<string:hotel_id>')
def get_hotel(hotel_id):
    try:
        db = current_app.db
        hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
        if not hotel:
            return "Hotel not found", 404

        rooms = db.rooms.find({"hotel_id": hotel_id})
        return render_template('hotel_details.html', hotel=hotel, rooms=rooms)
    except Exception as e:
        return jsonify({'error': str(e)}), 500





@bp.route('/logout')
@login_required
def logout():
    current_app.config['LOGGED_IN_USER'] = None
    return redirect(url_for('routes.index'))


@bp.route('/add_reservation', methods=['POST'])
@login_required
def add_reservation():
    try:
        data = request.json
        required_fields = ['room_id', 'customer_name', 'check_in', 'check_out']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        db = current_app.db
        reservation_data = {
            'room_id': data['room_id'],
            'customer_name': data['customer_name'],
            'check_in': data['check_in'],
            'check_out': data['check_out']
        }
        result = db.reservations.insert_one(reservation_data)
        return jsonify({'inserted_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/reservations', methods=['GET'])
@login_required
def get_reservations():
    try:
        db = current_app.db
        reservations = db.reservations.find()
        result = []
        for reservation in reservations:
            reservation['_id'] = str(reservation['_id'])
            result.append(reservation)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
