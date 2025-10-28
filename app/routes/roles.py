from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Role, Permission

roles_bp = Blueprint('roles', __name__)

# ✅ Create
@roles_bp.route('/role', methods=['POST'])
def create_role():
    data = request.get_json()

    # 1️⃣ Basic validation
    name = data.get('name')
    permission_codes = data.get('permissions', [])

    if not name:
        return jsonify({"error": "Role name is required"}), 400

    # 2️⃣ Check for duplicates
    if Role.query.filter_by(name=name).first():
        return jsonify({"error": f"Role '{name}' already exists"}), 400

    # 3️⃣ Create the Role
    role = Role(name=name)

    # 4️⃣ Attach existing permissions by code
    if permission_codes:
        print(f"🔍 Looking for permission codes: {permission_codes}", flush=True)
        existing_perms = Permission.query.filter(
            Permission.code.in_(permission_codes)
        ).all()
        print(f"🔍 Found {len(existing_perms)} permissions: {[p.code for p in existing_perms]}", flush=True)
        
        # Check if all provided permission codes exist
        existing_codes = {perm.code for perm in existing_perms}
        invalid_codes = [code for code in permission_codes if code not in existing_codes]
        
        if invalid_codes:
            return jsonify({
                "error": "Invalid permission codes provided",
                "invalid_permissions": invalid_codes
            }), 400
            
        role.permissions = existing_perms  # many-to-many link
        print(f"🔍 Assigned {len(role.permissions)} permissions to role")

    # 5️⃣ Commit
    db.session.add(role)
    db.session.commit()

    return jsonify(role.to_dict()), 201


# ✅ Read all
@roles_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([r.to_dict() for r in roles])

# ✅ Read one
@roles_bp.route('/role/<int:id>', methods=['GET'])
def get_role(id):
    role = Role.query.get_or_404(id)
    return jsonify(role.to_dict())

# ✅ Update
@roles_bp.route('/role/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(role, key, value)
    db.session.commit()
    return jsonify(role.to_dict())

# ✅ Delete
@roles_bp.route('/role/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted successfully'})
