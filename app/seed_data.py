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
    p1 = Permission(code="APPOINTMENTS.VIEW.ALL", description="View Appointments")
    p2 = Permission(code="APPOINTMENTS.VIEW.SELF", description="View Your Appointments")
    p3 = Permission(code="APPOINTMENTS.CREATE", description="Create Appointments")
    p4 = Permission(code="APPOINTMENTS.DELETE", description="Delete Appointments")
    p5 = Permission(code="APPOINTMENTS.UPDATE.ASSIGN_AGENT", description="Assign or Reassign Agents to Appointment")
    p6 = Permission(code="APPOINTMENTS.UPDATE.SELF_ASSIGN", description="Assign Yourself to Appointment")
    p7 = Permission(code="APPOINTMENTS.UPDATE.STATUS", description="Update Appointment Status")
    p8 = Permission(code="USERS.VIEW", description="View All Users")
    p9 = Permission(code="USERS.CREATE", description="Create Users")
    p10 = Permission(code="USERS.DELETE", description="Delete Users")
    p11 = Permission(code="USERS.UPDATE.PERMISSIONS", description="Update User Permissions")
    p12 = Permission(code="ROLES.CREATE", description="Create Roles")
    p13 = Permission(code="ROLES.DELETE", description="Delete Roles")
    p14 = Permission(code="ROLES.UPDATE", description="Add Permissions to Roles")
    p15 = Permission(code="DISPOSITIONS.CREATE", description="Create Dispositions")
    p16 = Permission(code="DISPOSITIONS.DELETE", description="Delete Dispositions")

    # --- Roles ---
    admin_role = Role(name="Admin")
    staff_role = Role(name="Field Agent")
    
    # Assign permissions to admin role (all permissions)
    admin_role.permissions.extend([p1, p3, p4, p5, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16])
    
    # Assign permissions to staff role (limited permissions)
    staff_role.permissions.extend([p2, p6])

    # --- Users ---
    user1 = User(
        name="John Doe",
        email="john@example.com",
        address="123 Maple Street",
        phone="555-111-2222",
        status="available",
        permissions_id="APPOINTMENTS.CREATE"
    )
    user2 = User(
        name="Jane Smith",
        email="jane@example.com",
        address="456 Oak Avenue",
        phone="555-333-4444",
        status="on-site",
        permissions_id="USERS.VIEW"
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
        p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16,
        admin_role, staff_role,
        user1, user2,
        customer1, customer2,
        disp1, disp2,
        appt1, appt2
    ])

    db.session.commit()
    print("✅ Database seeded successfully!")
