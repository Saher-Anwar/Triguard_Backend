# app/routes/customers.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customer', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'address': c.address,
        'profile_data': c.profile_data
    } for c in customers])

@customers_bp.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address,
        'profile_data': customer.profile_data
    })

@customers_bp.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address'),
        profile_data=data.get('profile_data', {})
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer created', 'id': customer.id}), 201

@customers_bp.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    for key in ['name', 'email', 'phone', 'address', 'profile_data']:
        if key in data:
            setattr(customer, key, data[key])
    db.session.commit()
    return jsonify({'message': 'Customer updated'})

@customers_bp.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'})
