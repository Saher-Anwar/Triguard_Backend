from flask import Blueprint, request, jsonify
from extensions import db
from models.models import User, Role

users_bp = Blueprint('users', __name__)

# ✅ Create
@users_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# ✅ Read all
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# ✅ Read one
@users_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# ✅ Update
@users_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict())

# ✅ Update user role
@users_bp.route('/user/<int:id>/role', methods=['PUT'])
def update_user_role(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    role_id = data.get('role_id')
    if role_id is None:
        return jsonify({"error": "role_id is required"}), 400
    
    # Validate that the role exists
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": f"Role with id {role_id} not found"}), 404
    
    user.role_id = role_id
    db.session.commit()
    return jsonify(user.to_dict())

# ✅ Delete
@users_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
