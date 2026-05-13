# Triguard Backend API

A production-ready REST API backend for the Triguard field service and appointment dispatch platform. Built with Flask and PostgreSQL, it provides full lifecycle management for appointments, field agents (users), customers, roles, permissions, and disposition codes — including geospatial agent-dispatch capabilities via the Haversine formula.

---

## Table of Contents

- [What Is Triguard?](#what-is-triguard)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Prerequisites](#prerequisites)
- [Running With Docker](#running-with-docker)
- [Database Management Commands](#database-management-commands)
- [Error Handling](#error-handling)
- [Running Tests](#running-tests)
- [Production Deployment](#production-deployment)

---

## What Is Triguard?

Triguard is a field service dispatching platform designed to coordinate security and inspection appointments between customers and field agents. The backend manages:

- Scheduling and tracking appointments through their full lifecycle
- Assigning field agents to appointments based on geographic proximity
- Enforcing role-based access control with granular permission codes
- Recording appointment outcomes via configurable disposition codes
- Storing location data for both agents and customers to enable proximity-based dispatch

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Flask 3.0 |
| ORM | Flask-SQLAlchemy 3.1 |
| Database | PostgreSQL (via psycopg2) |
| Migrations | Flask-Migrate 4.0 (Alembic) |
| WSGI Server | Gunicorn 21.2 |
| CORS | Flask-CORS |
| Configuration | python-dotenv |
| Containerization | Docker + Docker Compose |
| Cloud Database | AWS RDS PostgreSQL (production) |

---

## Architecture Overview

```
                        +-------------------------+
                        |     Flask Application    |
                        |  (Application Factory)   |
                        +----------+--+------------+
                                   |  |
              +--------------------+  +--------------------+
              |                                            |
   +----------v----------+                    +-----------v----------+
   |   Route Blueprints  |                    |   Error Handlers     |
   |  /api/appointments  |                    |  404, 400, 409, 500  |
   |  /api/users         |                    +----------------------+
   |  /api/customers     |
   |  /api/roles         |
   |  /api/permissions   |
   |  /api/dispositions  |
   +----------+----------+
              |
   +----------v----------+
   |   SQLAlchemy ORM    |
   |   (Flask-Migrate)   |
   +----------+----------+
              |
   +----------v----------+
   |    PostgreSQL DB     |
   |   (AWS RDS / local) |
   +---------------------+
```

The application uses the **Application Factory** pattern (`create_app()`), with each resource group organized into its own Flask Blueprint. All blueprints are registered under the `/api/` prefix. Database access uses SQLAlchemy with session-scoped teardown and automatic rollback on request exceptions.

---

## Features

- **Full CRUD API** for all resources: appointments, users, customers, roles, permissions, and dispositions
- **Geospatial agent dispatch**: ranks all available field agents by distance from an appointment's customer location using the Haversine formula (result in miles)
- **Role-based access control (RBAC)**: roles group permission codes; users inherit permissions from their assigned role and can also carry individually assigned permissions stored as a JSONB array
- **Automatic customer creation on appointment booking**: if a customer does not exist, the create-appointment endpoint creates one inline
- **ISO 8601 datetime parsing**: booking datetimes are accepted as ISO 8601 strings and stored as proper `DateTime` objects
- **JSONB flexible fields**: `location`, `profile`, and `profile_data` fields use PostgreSQL JSONB for schema flexibility
- **Disposition codes**: configurable outcome codes (e.g. `SOLD_CASH_DEAL`, `NO_SHOWED`) are attached to appointments post-completion
- **Database seeding and management CLI**: `flask seed`, `flask unseed`, `flask wipe` commands for development workflows
- **Global error handling**: consistent JSON error responses for 404, 400, 409 (integrity), and 500 errors with automatic session rollback
- **CORS enabled**: cross-origin requests are permitted for frontend integration
- **Non-root Docker container**: the application runs as a dedicated `appuser` inside the container
- **Connection pooling**: configurable SQLAlchemy pool size and max overflow via environment variables

---

## API Endpoints

All endpoints are prefixed with `/api/`. The health check lives at the root.

### Health Check

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Returns API status |

**Response:**
```json
{ "status": "healthy", "message": "Triguard Backend API is running" }
```

---

### Appointments — `/api/`

| Method | Path | Description |
|---|---|---|
| POST | `/api/appointment` | Create an appointment (auto-creates customer if needed) |
| GET | `/api/appointments` | List all appointments |
| GET | `/api/appointment/<id>` | Get a single appointment by ID |
| PUT | `/api/appointment/<id>` | Update an appointment |
| DELETE | `/api/appointment/<id>` | Delete an appointment |
| GET | `/api/users/<user_id>/appointments` | List all appointments assigned to a specific user |
| GET | `/api/appointment/<appointment_id>/users` | List all users sorted by distance from the appointment's customer location |

**Create Appointment — Request Body:**
```json
{
  "booking_datetime": "2025-10-30T09:00:00",
  "status": "scheduled",
  "customer_id": 1,
  "user_id": 2,
  "disposition_id": null,
  "details": { "service": "inspection", "priority": "high" }
}
```

Or pass a nested `customer` object to auto-create (or match by email) the customer inline:
```json
{
  "booking_datetime": "2025-10-30T09:00:00",
  "status": "unassigned",
  "customer": {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "555-777-8888",
    "location": {
      "address": "789 Pine Blvd",
      "city": "Springfield",
      "country": "USA",
      "zip_code": "12347",
      "latitude": 39.7755,
      "longitude": -89.6598
    }
  },
  "details": { "service": "inspection" }
}
```

**Get Users by Distance — Response:**
```json
[
  {
    "id": "2",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "status": "available",
    "location": { "latitude": 39.7892, "longitude": -89.6445 },
    "distance_miles": 1.23
  }
]
```

---

### Users — `/api/`

| Method | Path | Description |
|---|---|---|
| POST | `/api/user` | Create a user |
| GET | `/api/users` | List all users |
| GET | `/api/user/<id>` | Get a user by ID |
| GET | `/api/user/email/<email>` | Get a user by email address |
| PUT | `/api/user/<id>` | Update a user |
| PUT | `/api/user/<id>/role` | Assign a role to a user (copies role permissions) |
| PUT | `/api/user/<id>/permissions` | Override a user's individual permission codes |
| DELETE | `/api/user/<id>` | Delete a user |

**Create User — Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "status": "available",
  "role_id": 1,
  "location": {
    "address": "123 Maple Street",
    "city": "Springfield",
    "country": "USA",
    "zip_code": "12345",
    "latitude": 39.7817,
    "longitude": -89.6501
  },
  "profile": {
    "phone": "555-111-2222",
    "department": "Security Operations"
  }
}
```

**Assign Role — Request Body:**
```json
{ "role_id": 1 }
```
Passing `null` or `""` removes the role and clears all permissions.

**Override Permissions — Request Body:**
```json
{ "permission_codes": ["APPOINTMENTS.VIEW.SELF", "APPOINTMENTS.UPDATE.SELF_ASSIGN"] }
```

---

### Customers — `/api/`

| Method | Path | Description |
|---|---|---|
| POST | `/api/customer` | Create a customer |
| GET | `/api/customer` | List all customers |
| GET | `/api/customer/<id>` | Get a customer by ID |
| PUT | `/api/customer/<id>` | Update a customer |
| DELETE | `/api/customer/<id>` | Delete a customer |

**Create Customer — Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "555-777-8888",
  "location": {
    "address": "789 Pine Blvd",
    "city": "Springfield",
    "country": "USA",
    "zip_code": "12347",
    "latitude": 39.7755,
    "longitude": -89.6598
  },
  "profile_data": { "preferred_time": "morning", "notes": "VIP customer" }
}
```

---

### Roles — `/api/`

| Method | Path | Description |
|---|---|---|
| POST | `/api/role` | Create a role with optional permission codes |
| GET | `/api/roles` | List all roles with their permissions |
| GET | `/api/role/<id>` | Get a role by ID |
| PUT | `/api/role/<id>` | Update a role |
| DELETE | `/api/role/<id>` | Delete a role |

**Create Role — Request Body:**
```json
{
  "name": "Field Agent",
  "permissions": ["APPOINTMENTS.VIEW.SELF", "APPOINTMENTS.UPDATE.SELF_ASSIGN"]
}
```

---

### Permissions — `/api/`

| Method | Path | Description |
|---|---|---|
| POST | `/api/permission` | Create a permission code |
| GET | `/api/permissions` | List all permissions |
| GET | `/api/permission/<id>` | Get a permission by ID |
| PUT | `/api/permission/<id>` | Update a permission |
| DELETE | `/api/permission/<id>` | Delete a permission |

**Create Permission — Request Body:**
```json
{ "code": "APPOINTMENTS.VIEW.ALL", "description": "View all appointments" }
```

---

### Dispositions — `/api/`

| Method | Path | Description |
|---|---|---|
| POST | `/api/disposition` | Create a disposition code |
| GET | `/api/dispositions` | List all dispositions |
| GET | `/api/disposition/<code>` | Get a disposition by code string |
| PUT | `/api/disposition/<code>` | Update a disposition |
| DELETE | `/api/disposition/<code>` | Delete a disposition |

**Create Disposition — Request Body:**
```json
{ "code": "SOLD_CASH_DEAL", "description": "Sold Cash Deal" }
```

---

## Environment Variables

Create a `.env` file in the project root. The application reads this file via `python-dotenv`.

```env
# Flask Configuration
FLASK_ENV=development          # "development" or "production"
FLASK_DEBUG=1                  # 1 for dev, 0 for production
FLASK_APP=app.main             # Application module reference
SECRET_KEY=replace-with-a-secure-random-string

# Database Connection
DB_NAME=triguard_db
DB_USER=triguard_user
DB_PASSWORD=your-db-password
DB_HOST=localhost              # Use the RDS endpoint in production
DB_PORT=5432

# Optional: Full DATABASE_URL overrides the individual DB_* variables (DevConfig only)
# DATABASE_URL=postgresql+psycopg2://user:password@host:5432/dbname

# Optional: SQLAlchemy Tuning
SQLALCHEMY_ECHO=0              # Set to 1 to log all SQL queries
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
```

> **Security**: Never commit your `.env` file. It is listed in `.gitignore`. For production, inject secrets via your deployment platform's secrets manager or environment variable injection.

---

## Prerequisites

- Python 3.11+
- Docker Engine 24+
- Docker Compose v2+

---

## Running

The Docker Compose configuration runs the Flask application in a container and expects a PostgreSQL database to be available at the `DB_HOST` specified in your `.env` file. The compose file does not bundle a database container — connect it to an existing local PostgreSQL instance, a separate Docker network, or AWS RDS.

**1. Build and start the container:**
```bash
docker-compose up --build
```

**2. Run in the background:**
```bash
docker-compose up -d --build
```

**3. Apply migrations inside the container:**
```bash
docker-compose exec backend flask db upgrade
```

**4. Seed the database:**
```bash
docker-compose exec backend flask seed
```

**5. Verify the service:**
```bash
curl http://localhost:5000/health
```

**6. View logs:**
```bash
docker-compose logs -f backend
```

**7. Stop the service:**
```bash
docker-compose down
```

---

## Database Management Commands

These custom Flask CLI commands are available in both local and Docker environments:

| Command | Description |
|---|---|
| `flask db upgrade` | Apply all pending Alembic migrations |
| `flask db migrate -m "message"` | Generate a new migration from model changes |
| `flask db downgrade` | Roll back the last migration |
| `flask seed` | Insert sample permissions, roles, users, customers, dispositions, and appointments |
| `flask unseed` | Delete all seeded data in safe dependency order |
| `flask wipe` | Drop and recreate all tables (prompts for confirmation) |

**Inside Docker:**
```bash
docker-compose exec backend flask <command>
```

---

## Error Handling

All errors return a consistent JSON envelope. The application registers global handlers for:

| HTTP Status | Trigger |
|---|---|
| `400 Bad Request` | Invalid request format or missing required fields |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Database integrity violation (duplicate unique key, FK violation) |
| `500 Internal Server Error` | Unhandled exception or SQLAlchemy error |

**Error response format:**
```json
{
  "error": "Human-readable error description",
  "details": "Technical detail string (optional)"
}
```

All database errors trigger an automatic `db.session.rollback()` before the response is returned.

---

## Running Tests

A test suite has not yet been added to the project. When one is introduced, the standard entry point will be:

```bash
# Local
python -m pytest

# Inside Docker
docker-compose exec backend python -m pytest
```

To manually verify database connectivity:
```bash
docker-compose exec backend python -c "
from app.main import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    result = db.session.execute(db.text('SELECT 1')).scalar()
    print('DB connection OK:', result)
"
```

---

## Production Deployment

### Security Checklist

- Set `FLASK_ENV=production` and `FLASK_DEBUG=0`
- Use a cryptographically random `SECRET_KEY` (minimum 32 bytes)
- Use a strong, unique `DB_PASSWORD`
- Run behind a reverse proxy (nginx, AWS ALB) that terminates HTTPS/TLS
- Restrict database security group/firewall rules to allow only the application host
- Rotate credentials on a schedule; use AWS Secrets Manager or equivalent
- Review and scope CORS origins to your actual frontend domain

### Running With Gunicorn (WSGI)

The container's default `CMD` uses the Python development server. For production, replace it with Gunicorn:

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 "app.main:create_app()"
```

Or update the `Dockerfile` `CMD`:
```dockerfile
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app.main:create_app()"]
```

### Migration Strategy

Run migrations as a pre-startup step in your deployment pipeline before routing traffic to new containers:

```bash
flask db upgrade
```

This is safe to run against a live database; Alembic tracks applied revisions and is idempotent.
