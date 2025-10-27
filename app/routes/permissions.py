from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Permission

permissions_bp = Blueprint('permissions', __name__)

# ✅ Create
@permissions_bp.route('/permission', methods=['POST'])
def create_permission():
    data = request.get_json()
    permission = Permission(**data)
    db.session.add(permission)
    db.session.commit()
    return jsonify(permission.to_dict()), 201

# ✅ Read all
@permissions_bp.route('/permissions', methods=['GET'])
def get_permissions():
    permissions = Permission.query.all()
    return jsonify([p.to_dict() for p in permissions])

# ✅ Read one
@permissions_bp.route('/permission/<int:id>', methods=['GET'])
def get_permission(id):
    permission = Permission.query.get_or_404(id)
    return jsonify(permission.to_dict())

# ✅ Update
@permissions_bp.route('/permission/<int:id>', methods=['PUT'])
def update_permission(id):
    permission = Permission.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(permission, key, value)
    db.session.commit()
    return jsonify(permission.to_dict())

# ✅ Delete
@permissions_bp.route('/permission/<int:id>', methods=['DELETE'])
def delete_permission(id):
    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    return jsonify({'message': 'Permission deleted successfully'})
