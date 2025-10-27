# app/seed_data.py
from datetime import datetime
from extensions import db
from models.models import (
    Customer,
    User,
    Role,
    Permission,
    Disposition,
    Appointment
)

def seed_database():
    """Insert sample data into the database."""
    print("🌱 Seeding database...")

    # --- Permissions ---
    p1 = Permission(code="CREATE_APPOINTMENT", description="Can create new appointments")
    p2 = Permission(code="EDIT_APPOINTMENT", description="Can edit existing appointments")
    p3 = Permission(code="VIEW_CUSTOMERS", description="Can view customer details")

    # --- Roles ---
    admin_role = Role(name="Admin", permissions_id="CREATE_APPOINTMENT")
    staff_role = Role(name="Staff", permissions_id="VIEW_CUSTOMERS")

    # --- Users ---
    user1 = User(
        name="John Doe",
        email="john@example.com",
        address="123 Maple Street",
        phone="555-111-2222",
        status="available",
        permissions_id="CREATE_APPOINTMENT"
    )
    user2 = User(
        name="Jane Smith",
        email="jane@example.com",
        address="456 Oak Avenue",
        phone="555-333-4444",
        status="on-site",
        permissions_id="VIEW_CUSTOMERS"
    )

    # --- Customers ---
    customer1 = Customer(
        name="Alice Johnson",
        email="alice@example.com",
        phone="555-777-8888",
        address="789 Pine Blvd",
        profile_data={"preferred_time": "morning", "notes": "VIP customer"}
    )
    customer2 = Customer(
        name="Bob Brown",
        email="bob@example.com",
        phone="555-999-0000",
        address="321 Cedar Lane",
        profile_data={"preferred_time": "evening", "notes": "Repeat customer"}
    )

    # --- Dispositions ---
    disp1 = Disposition(code="COMPLETE", description="Job completed successfully")
    disp2 = Disposition(code="CANCELLED", description="Appointment cancelled")

    # --- Appointments ---
    appt1 = Appointment(
        booking_datetime=datetime.utcnow(),
        status="scheduled",
        customer=customer1,
        user=user1,
        details={"service": "inspection", "priority": "high"},
        disposition=disp1
    )
    appt2 = Appointment(
        booking_datetime=datetime.utcnow(),
        status="in progress",
        customer=customer2,
        user=user2,
        details={"service": "maintenance"},
        disposition=None
    )

    # Add all data
    db.session.add_all([
        p1, p2, p3,
        admin_role, staff_role,
        user1, user2,
        customer1, customer2,
        disp1, disp2,
        appt1, appt2
    ])

    db.session.commit()
    print("✅ Database seeded successfully!")
