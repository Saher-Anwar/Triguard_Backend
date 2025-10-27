# app/main.py
import os
import sys
sys.path.append('/app')

from flask import Flask
from flask_cors import CORS
from config import config
from extensions import db, migrate
from routes.appointments import appointments_bp
from routes.customers import customers_bp
from routes.dispositions import dispositions_bp
from routes.users import users_bp
from routes.roles import roles_bp
from routes.permissions import permissions_bp
from error_handlers import register_error_handlers

from seed_data import seed_database
from flask.cli import with_appcontext
import click

def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(appointments_bp, url_prefix='/api/')
    app.register_blueprint(customers_bp, url_prefix='/api/')
    app.register_blueprint(dispositions_bp, url_prefix='/api/')
    app.register_blueprint(users_bp, url_prefix='/api/')
    app.register_blueprint(roles_bp, url_prefix='/api/')
    app.register_blueprint(permissions_bp, url_prefix='/api/')

    register_error_handlers(app)

    @app.teardown_request
    def teardown_request(exception=None):
        if exception:
            db.session.rollback()
        db.session.remove()

    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Triguard Backend API is running'}

    # Import models so migrations detect them
    from models import models

    register_commands(app)
    return app

@click.command("seed")
@with_appcontext
def seed_command():
    seed_database()

def register_commands(app):
    app.cli.add_command(seed_command)

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
