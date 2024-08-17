from flask import Blueprint, request, jsonify, render_template, current_app

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
        db = current_app.db
        result = db.reservations.insert_one(data)
        return jsonify({'inserted_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        db = current_app.db
        reservations = db.reservations.find()
        result = []
        for reservation in reservations:
            reservation['_id'] = str(reservation['_id'])  # Convert ObjectId to string
            result.append(reservation)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
