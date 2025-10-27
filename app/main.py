import os
import sys
sys.path.append('/app')

from flask import Flask
from config import config
from extensions import db, migrate
from routes.appointments import appointments_bp
# Register a CLI command to seed the database
from seed_data import seed_database
from flask.cli import with_appcontext
import click

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(appointments_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Triguard Backend API is running'}
    
    # Import models to ensure they are registered with SQLAlchemy
    from models import models
    
    with app.app_context():
      from models import models  # ensure models are registered
      print("Models imported successfully")

      if config_name == 'development':
          print("Running in development mode")
  
    register_commands(app)
    return app


@click.command("seed")
@with_appcontext
def seed_command():
    """Seed the database with sample data."""
    seed_database()

def register_commands(app):
    app.cli.add_command(seed_command)

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)