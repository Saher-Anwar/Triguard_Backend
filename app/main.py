import os
import sys
sys.path.append('/app')

from flask import Flask
from config import config
from extensions import db, migrate
from routes.appointments import appointments_bp

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
  
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)