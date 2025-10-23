from flask import Blueprint, jsonify
from models.models import Appointment, Customer, User, Disposition
from extensions import db

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        appointments = db.session.query(Appointment)\
            .join(Customer, Appointment.customer_id == Customer.id)\
            .outerjoin(User, Appointment.user_id == User.id)\
            .outerjoin(Disposition, Appointment.disposition_id == Disposition.code)\
            .all()
        
        return jsonify({
            'success': True,
            'data': [appointment.to_dict() for appointment in appointments],
            'count': len(appointments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500