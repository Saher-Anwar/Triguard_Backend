from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Disposition

dispositions_bp = Blueprint('dispositions', __name__)

# ✅ Create
@dispositions_bp.route('/disposition', methods=['POST'])
def create_disposition():
    data = request.get_json()
    
    # Validate required fields
    code = data.get('code')
    if not code:
        return jsonify({"error": "Disposition code is required"}), 400
    
    # Check for duplicates
    if Disposition.query.filter_by(code=code).first():
        return jsonify({"error": f"Disposition '{code}' already exists"}), 400
    
    disposition = Disposition(**data)
    db.session.add(disposition)
    db.session.commit()
    return jsonify(disposition.to_dict()), 201

# ✅ Read all
@dispositions_bp.route('/dispositions', methods=['GET'])
def get_dispositions():
    dispositions = Disposition.query.all()
    return jsonify([d.to_dict() for d in dispositions])

# ✅ Read one
@dispositions_bp.route('/disposition/<string:code>', methods=['GET'])
def get_disposition(code):
    disposition = Disposition.query.get_or_404(code)
    return jsonify(disposition.to_dict())

# ✅ Update
@dispositions_bp.route('/disposition/<string:code>', methods=['PUT'])
def update_disposition(code):
    disposition = Disposition.query.get_or_404(code)
    data = request.get_json()
    for key, value in data.items():
        setattr(disposition, key, value)
    db.session.commit()
    return jsonify(disposition.to_dict())

# ✅ Delete
@dispositions_bp.route('/disposition/<string:code>', methods=['DELETE'])
def delete_disposition(code):
    disposition = Disposition.query.get_or_404(code)
    db.session.delete(disposition)
    db.session.commit()
    return jsonify({'message': 'Disposition deleted successfully'})
