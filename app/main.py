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

@click.command("unseed")
@with_appcontext
def unseed_command():
    """Remove all seeded data safely from the database."""
    from models.models import Appointment, Customer, Disposition, User, Role, Permission, role_permissions
    from extensions import db

    try:
        # Delete in reverse dependency order to avoid FK violations
        db.session.query(Appointment).delete()
        db.session.query(Disposition).delete()
        db.session.query(Customer).delete()
        db.session.query(User).delete()
        
        # Clear the many-to-many association table first
        db.session.execute(role_permissions.delete())
        
        # Then delete roles and permissions
        db.session.query(Role).delete()
        db.session.query(Permission).delete()

        db.session.commit()
        click.echo("✅ Database unseeded successfully.")

    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error during unseeding: {e}")

@click.command("wipe")
@with_appcontext
def wipe_command():
    """Completely drop and recreate all tables."""
    from extensions import db
    from models import models  # ensures all models are loaded

    click.confirm(
        "⚠️  This will delete ALL data and drop ALL tables. Continue?",
        abort=True
    )

    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("🧱 Database wiped and recreated successfully.")

def register_commands(app):
    app.cli.add_command(seed_command)
    app.cli.add_command(unseed_command)
    app.cli.add_command(wipe_command)

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
