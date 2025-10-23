# Triguard Backend API

A production-ready Flask backend application with PostgreSQL database, containerized with Docker.

## Features

- **Flask REST API** with SQLAlchemy ORM
- **PostgreSQL** database with proper relationships
- **Docker Compose** for easy deployment
- **Automatic migrations** with Flask-Migrate
- **Sample data seeding** for development
- **Health check endpoints**
- **Environment-based configuration**

## Project Structure

```
Triguard_Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application factory and startup
│   ├── config.py              # Configuration classes
│   ├── extensions.py          # Flask extensions initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # SQLAlchemy models
│   └── routes/
│       ├── __init__.py
│       └── appointments.py    # Appointments API endpoints
├── docker-compose.yml         # Docker services configuration
├── Dockerfile                 # Flask app container definition
├── requirements.txt           # Python dependencies
├── seed_data.py              # Sample data for development
├── .env                      # Environment variables (create from .env.example)
└── README.md
```

## Database Schema

### Tables and Relationships

- **appointments**: Main booking table with foreign keys to customers, users, and dispositions
- **customers**: Customer information with JSONB profile data
- **users**: System users with status and permissions
- **dispositions**: Appointment outcome codes
- **roles**: User roles linked to permissions
- **permissions**: System permission codes

### Key Relationships

```python
# Foreign Key Relationships:
appointments.customer_id → customers.id
appointments.user_id → users.id (nullable)
appointments.disposition_id → dispositions.code (nullable)
users.permissions_id → permissions.code
roles.permissions_id → permissions.code
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Triguard_Backend

# Copy environment file and update values
cp .env.example .env
# Edit .env with your preferred credentials
```

### 2. Start Services

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Verify Installation

```bash
# Check health endpoint
curl http://localhost:5000/health

# Get appointments with customer and user data
curl http://localhost:5000/api/appointments
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.main:create_app
SECRET_KEY=your-secret-key-change-in-production

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=triguard_db
DB_USER=triguard_user
DB_PASSWORD=triguard_password
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Appointments
- `GET /api/appointments` - Get all appointments with joined customer and user data

Example response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "booking_datetime": "2024-01-15T14:30:00",
      "status": "scheduled",
      "customer": {
        "id": 1,
        "name": "ABC Corporation",
        "email": "security@abccorp.com",
        "phone": "+1-555-1001",
        "address": "100 Business Park Dr, Corporate City, State 54321"
      },
      "user": {
        "id": 2,
        "name": "Sarah Johnson",
        "email": "sarah.johnson@triguard.com",
        "status": "on-site"
      },
      "details": {
        "service_type": "Security System Maintenance",
        "estimated_duration": "2 hours"
      },
      "disposition": null
    }
  ],
  "count": 1
}
```

## Development

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set up database (ensure PostgreSQL is running)
export FLASK_APP=app.main:create_app
export FLASK_ENV=development

# Create database and run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start development server
python app/main.py
```

### Database Operations

```bash
# Access database in Docker
docker-compose exec db psql -U triguard_user -d triguard_db

# View logs
docker-compose logs backend
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up --build
```

### Adding New Models

1. Define model in `app/models/models.py`
2. Import model in `app/main.py`
3. Restart the application (migrations are automatic in development)

### Adding New Routes

1. Create new blueprint in `app/routes/`
2. Register blueprint in `app/main.py`
3. Follow the same pattern as `appointments.py`

## Production Deployment

### Security Considerations

1. **Change default credentials** in `.env`
2. **Use strong SECRET_KEY**
3. **Set FLASK_ENV=production**
4. **Configure proper firewall rules**
5. **Use HTTPS with reverse proxy**
6. **Regular security updates**

### Production Environment Variables

```env
FLASK_ENV=production
SECRET_KEY=your-very-strong-secret-key
DB_PASSWORD=very-strong-database-password
```

### Scaling

- Use `gunicorn` for production WSGI server
- Configure PostgreSQL connection pooling
- Add Redis for caching and sessions
- Use load balancer for multiple backend instances

## Testing

```bash
# Run tests (when test suite is added)
docker-compose exec backend python -m pytest

# Test database connection
docker-compose exec backend python -c "from app.main import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); print('DB Connection:', db.engine.execute('SELECT 1').scalar())"
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check if PostgreSQL container is running: `docker-compose ps`
   - Verify credentials in `.env` file
   - Ensure database has enough time to start: check health check

2. **Port Already in Use**
   - Change ports in `docker-compose.yml`
   - Kill existing processes: `sudo lsof -ti:5000 | xargs kill -9`

3. **Migration Errors**
   - Reset volumes: `docker-compose down -v`
   - Check model definitions for syntax errors

4. **Permission Denied**
   - Ensure proper file permissions
   - Check Docker daemon is running

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f backend
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.