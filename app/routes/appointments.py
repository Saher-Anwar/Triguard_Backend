from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Appointment, User
import math

appointments_bp = Blueprint('appointments', __name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on earth (in miles)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in miles
    r = 3959
    return c * r

@appointments_bp.route('/appointment', methods=['POST'])
def create_appointment():
    from datetime import datetime
    from models.models import Customer
    
    data = request.get_json()
    
    # Convert ISO 8601 string to datetime object
    if 'booking_datetime' in data and isinstance(data['booking_datetime'], str):
        try:
            data['booking_datetime'] = datetime.fromisoformat(data['booking_datetime'])
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"}), 400
    
    # Handle nested customer creation
    if 'customer' in data:
        customer_data = data.pop('customer')
        
        # Check if customer already exists by email
        existing_customer = Customer.query.filter_by(email=customer_data['email']).first()
        if existing_customer:
            data['customer_id'] = existing_customer.id
        else:
            # Create new customer
            new_customer = Customer(**customer_data)
            db.session.add(new_customer)
            db.session.flush()  # Get the customer ID without committing
            data['customer_id'] = new_customer.id
    
    appointment = Appointment(**data)
    db.session.add(appointment)
    db.session.commit()
    return jsonify(appointment.to_dict()), 201

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])

@appointments_bp.route('/appointment/<int:id>', methods=['GET'])
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return jsonify(appointment.to_dict())

@appointments_bp.route('/appointment/<int:id>', methods=['PUT'])
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(appointment, key, value)
    db.session.commit()
    return jsonify(appointment.to_dict())

@appointments_bp.route('/appointment/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'})

@appointments_bp.route('/users/<int:user_id>/appointments', methods=['GET'])
def get_user_appointments(user_id):
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in appointments])

@appointments_bp.route('/appointment/<int:appointment_id>/users', methods=['GET'])
def get_users_by_appointment_distance(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Get appointment location from customer
    if not appointment.customer or not appointment.customer.location:
        return jsonify({"error": "Appointment customer location not found"}), 400
    
    customer_location = appointment.customer.location
    appointment_lat = customer_location.get('latitude')
    appointment_lon = customer_location.get('longitude')
    
    if appointment_lat is None or appointment_lon is None:
        return jsonify({"error": "Appointment coordinates not found"}), 400
    
    # Get all users with locations
    users = User.query.all()
    users_with_distance = []
    
    for user in users:
        if user.location and user.location.get('latitude') and user.location.get('longitude'):
            user_lat = user.location.get('latitude')
            user_lon = user.location.get('longitude')
            
            distance = haversine_distance(appointment_lat, appointment_lon, user_lat, user_lon)
            
            user_data = user.to_dict()
            user_data['distance_miles'] = round(distance, 2)
            users_with_distance.append(user_data)
    
    # Sort by distance (closest first)
    users_with_distance.sort(key=lambda x: x['distance_miles'])
    
    return jsonify(users_with_distance)
