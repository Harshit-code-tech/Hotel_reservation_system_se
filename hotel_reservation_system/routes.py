# routes.py
from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for, session, flash
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
bp = Blueprint('routes', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first.", "warning")
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        db = current_app.db
        user = db.users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            return jsonify({'success': True, 'redirect': url_for('routes.index')})
        return jsonify({'success': False, 'message': 'Invalid credentials. Please try again.'})
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        db = current_app.db
        existing_user = db.users.find_one({'email': data['email']})
        password_error = validate_password(data['password'])
        if existing_user:
            return jsonify({'success': False, 'message': 'User already exists with this email.'})
        if password_error:
            return jsonify({'success': False, 'message': password_error})
        hashed_password = generate_password_hash(data['password'])
        db.users.insert_one({
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password
        })
        return jsonify({'success': True, 'redirect': url_for('routes.login')})
    return render_template('register.html')
@bp.route('/logout')
@login_required
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.index'))

@bp.route('/')
@login_required
def index():
    try:
        db = current_app.db
        hotels = db.hotels.find()
        return render_template('hotel_list.html', hotels=hotels)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return render_template('error.html'), 500

@bp.route('/hotel/<string:hotel_id>')
def get_hotel(hotel_id):
    try:
        db = current_app.db
        hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
        if not hotel:
            flash('Hotel not found.', 'warning')
            return redirect(url_for('routes.index'))

        rooms = db.rooms.find({"hotel_id": hotel_id})
        return render_template('hotel_details.html', hotel=hotel, rooms=rooms)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return render_template('error.html'), 500

@bp.route('/add_reservation', methods=['POST'])
@login_required
def add_reservation():
    try:
        data = request.json
        required_fields = ['room_id', 'customer_name', 'check_in', 'check_out']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        db = current_app.db
        db.reservations.insert_one(data)
        return jsonify({"message": "Reservation added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
