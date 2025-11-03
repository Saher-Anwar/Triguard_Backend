from flask import Blueprint, request, jsonify
from extensions import db
from models.models import User, Role

users_bp = Blueprint('users', __name__)

# ✅ Create
@users_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    name = data.get('name')
    email = data.get('email')
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Check for duplicate email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": f"User with email '{email}' already exists"}), 400
    
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# ✅ Read all
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# ✅ Read one by ID
@users_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# ✅ Read one by email
@users_bp.route('/user/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
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

    # Handle None or empty string - user has no role and no permissions
    if role_id is None or role_id == '' or role_id == 'null':
        user.role_id = None
        user.permissions = []
        db.session.commit()
        return jsonify(user.to_dict())

    # Validate that the role exists
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": f"Role with id {role_id} not found"}), 404

    # Update role and copy permission codes from role to user
    user.role_id = role_id
    user.permissions = [perm.code for perm in role.permissions]

    db.session.commit()
    return jsonify(user.to_dict())

# ✅ Update user permissions
@users_bp.route('/user/<int:id>/permissions', methods=['PUT'])
def update_user_permissions(id):
    from models.models import Permission

    user = User.query.get_or_404(id)
    data = request.get_json()

    permission_codes = data.get('permission_codes', [])

    # Validate that all permission codes exist
    if permission_codes:
        existing_perms = Permission.query.filter(Permission.code.in_(permission_codes)).all()
        existing_codes = {perm.code for perm in existing_perms}
        invalid_codes = [code for code in permission_codes if code not in existing_codes]

        if invalid_codes:
            return jsonify({
                "error": "Invalid permission codes provided",
                "invalid_permissions": invalid_codes
            }), 400

    # Replace user's permissions with new list
    user.permissions = permission_codes

    db.session.commit()
    return jsonify(user.to_dict())

# ✅ Delete
@users_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
