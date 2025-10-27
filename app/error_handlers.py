# app/error_handlers.py
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from extensions import db

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad request', 'details': str(error)}), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Database integrity error',
            'details': str(error.orig)
        }), 409

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Database error',
            'details': str(error)
        }), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Unexpected server error',
            'details': str(error)
        }), 500
