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
        status="available",
        role_id=admin_role.id,
        profile={
            "age": 32,
            "address": "123 Maple Street",
            "phone": "555-111-2222",
            "department": "Security Operations"
        }
    )
    user2 = User(
        name="Jane Smith",
        email="jane@example.com",
        status="on-site",
        role_id=staff_role.id,
        profile={
            "age": 28,
            "address": "456 Oak Avenue", 
            "phone": "555-333-4444",
            "department": "Field Operations"
        }
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
    disp1 = Disposition(code="CANCELLED_AT_DOOR", description="Customer cancelled appointment at door")
    disp2 = Disposition(code="CREDIT_FAILED", description="Customer credit failed")
    disp3 = Disposition(code="SHOPPER", description="Customer is shopper")
    disp4 = Disposition(code="FOLLOW_UP_NEEDED", description="Customer needs followed up appointment")
    disp5 = Disposition(code="NO_SHOWED", description="Customer did not show up")
    disp6 = Disposition(code="CUSTOMER_NOT_INTERESTED", description="Customer needs followed up appointment")
    disp7 = Disposition(code="BEYOND_REPAIR", description="Home was beyond a roof repair")
    disp8 = Disposition(code="ONE_LEGGER", description="One party was not there or unsure")
    disp9 = Disposition(code="SOLD_CASH_DEAL", description="Sold Cash Deal")
    disp10 = Disposition(code="SOLD_PENDING", description="Sold pending final underwriting")

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
        disp1, disp2, disp3, disp4, disp5, disp6, disp7, disp8, disp9, disp10,
        appt1, appt2
    ])

    db.session.commit()
    print("✅ Database seeded successfully!")
