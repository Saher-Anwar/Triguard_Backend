from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Role

roles_bp = Blueprint('roles', __name__)

# ✅ Create
@roles_bp.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    role = Role(**data)
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_dict()), 201

# ✅ Read all
@roles_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([r.to_dict() for r in roles])

# ✅ Read one
@roles_bp.route('/roles/<int:id>', methods=['GET'])
def get_role(id):
    role = Role.query.get_or_404(id)
    return jsonify(role.to_dict())

# ✅ Update
@roles_bp.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(role, key, value)
    db.session.commit()
    return jsonify(role.to_dict())

# ✅ Delete
@roles_bp.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted successfully'})
