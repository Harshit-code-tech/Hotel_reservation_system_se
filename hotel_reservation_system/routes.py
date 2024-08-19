from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for, session, flash
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
import jwt
import datetime
from flask_mail import Mail, Message

bp = Blueprint('routes', __name__)

def generate_reset_token(email):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'email': email, 'exp': expiration}, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_reset_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['email']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

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

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        token = generate_reset_token(email)
        msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'''To reset your password, visit the following link:
        {url_for('routes.reset_password', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''

        try:
            mail = Mail(current_app)
            mail.send(msg)
            flash('An email has been sent with instructions to reset your password.', 'info')
        except Exception as e:
            flash('There was an issue sending the email. Please try again later.', 'danger')
            print(f"Error: {e}")
        return redirect(url_for('routes.login'))
    return render_template('forgot_password.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('The link is invalid or has expired.', 'warning')
        return redirect(url_for('routes.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        password_error = validate_password(password)
        if password_error:
            flash(password_error, 'warning')
            return render_template('reset_password.html', token=token)

        db = current_app.db
        hashed_password = generate_password_hash(password)
        db.users.update_one({'email': email}, {'$set': {'password': hashed_password}})
        flash('Your password has been updated.', 'info')
        return redirect(url_for('routes.login'))

    return render_template('reset_password.html', token=token)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        db = current_app.db
        user = db.users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is AJAX
                return jsonify({'success': True, 'redirect': url_for('routes.index')})
            else:
                return redirect(url_for('routes.index'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is AJAX
                return jsonify({'success': False, 'message': 'Invalid credentials. Please try again.'})
            else:
                flash('Invalid credentials. Please try again.', 'danger')
                return render_template('login.html')
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        db = current_app.db
        existing_user = db.users.find_one({'email': data['email']})
        password_error = validate_password(data['password'])

        if existing_user:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is AJAX
                return jsonify({'success': False, 'message': 'User already exists with this email.'})
            else:
                flash('User already exists with this email.', 'danger')
                return render_template('register.html')

        if password_error:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is AJAX
                return jsonify({'success': False, 'message': password_error})
            else:
                flash(password_error, 'danger')
                return render_template('register.html')

        hashed_password = generate_password_hash(data['password'])
        db.users.insert_one({
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password
        })

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is AJAX
            return jsonify({'success': True, 'redirect': url_for('routes.login')})
        else:
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('routes.login'))

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
        location = request.args.get('location', None)
        min_rating = request.args.get('min_rating', None)

        query = {}
        if location:
            query['location'] = {"$regex": location, "$options": "i"}  # Case-insensitive search
        if min_rating:
            query['rating'] = {"$gte": float(min_rating)}  # Filter by minimum rating

        hotels = db.hotels.find(query)
        return render_template('hotel_list.html', hotels=hotels)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return render_template('error.html'), 500

@bp.route('/hotel/<string:hotel_id>')
@login_required
def get_hotel(hotel_id):
    try:
        db = current_app.db
        hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
        if not hotel:
            flash('Hotel not found.', 'warning')
            return redirect(url_for('routes.index'))

        rooms = db.rooms.find({"hotel_id": ObjectId(hotel_id)})
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
        room = db.rooms.find_one({"_id": ObjectId(data['room_id'])})

        if not room or room.get('status') != "Available":
            return jsonify({"error": "Room not available"}), 400

        # Optionally update room status to 'Booked'
        db.rooms.update_one({"_id": ObjectId(data['room_id'])}, {"$set": {"status": "Booked"}})

        db.reservations.insert_one(data)
        return jsonify({"message": "Reservation added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

