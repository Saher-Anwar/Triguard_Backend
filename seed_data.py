from datetime import datetime, timedelta
from extensions import db
from models.models import Permission, Role, User, Customer, Disposition, Appointment

def seed_database():
    if Permission.query.first():
        print("Database already contains data, skipping seed")
        return

    try:
        # Create Permissions
        permissions = [
            Permission(code='ADMIN', description='Full administrative access'),
            Permission(code='TECHNICIAN', description='Technician access for appointments'),
            Permission(code='DISPATCHER', description='Dispatch and scheduling access'),
            Permission(code='VIEWER', description='Read-only access')
        ]
        
        for permission in permissions:
            db.session.add(permission)
        
        # Create Dispositions
        dispositions = [
            Disposition(code='COMPLETED', description='Service completed successfully'),
            Disposition(code='RESCHEDULED', description='Appointment rescheduled'),
            Disposition(code='CANCELLED', description='Appointment cancelled'),
            Disposition(code='NO_SHOW', description='Customer did not show up'),
            Disposition(code='INCOMPLETE', description='Service could not be completed')
        ]
        
        for disposition in dispositions:
            db.session.add(disposition)
        
        # Create Roles
        roles = [
            Role(name='Administrator', permissions_id='ADMIN'),
            Role(name='Senior Technician', permissions_id='TECHNICIAN'),
            Role(name='Dispatcher', permissions_id='DISPATCHER'),
            Role(name='Support', permissions_id='VIEWER')
        ]
        
        for role in roles:
            db.session.add(role)
        
        # Create Users
        users = [
            User(
                name='John Smith', 
                email='john.smith@triguard.com',
                address='123 Main St, City, State 12345',
                phone='+1-555-0101',
                status='available',
                permissions_id='ADMIN'
            ),
            User(
                name='Sarah Johnson', 
                email='sarah.johnson@triguard.com',
                address='456 Oak Ave, City, State 12345',
                phone='+1-555-0102',
                status='on-site',
                permissions_id='TECHNICIAN'
            ),
            User(
                name='Mike Wilson', 
                email='mike.wilson@triguard.com',
                address='789 Pine Rd, City, State 12345',
                phone='+1-555-0103',
                status='en-route',
                permissions_id='TECHNICIAN'
            ),
            User(
                name='Lisa Davis', 
                email='lisa.davis@triguard.com',
                address='321 Elm St, City, State 12345',
                phone='+1-555-0104',
                status='available',
                permissions_id='DISPATCHER'
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        # Create Customers
        customers = [
            Customer(
                name='ABC Corporation',
                email='security@abccorp.com',
                phone='+1-555-1001',
                address='100 Business Park Dr, Corporate City, State 54321',
                profile_data={
                    'industry': 'Technology',
                    'employee_count': 500,
                    'security_level': 'High',
                    'contact_person': 'Robert Miller'
                }
            ),
            Customer(
                name='Downtown Retail Mall',
                email='facilities@downtown-mall.com',
                phone='+1-555-1002',
                address='200 Shopping Center Blvd, Retail City, State 54321',
                profile_data={
                    'industry': 'Retail',
                    'business_type': 'Shopping Mall',
                    'operating_hours': '9AM-9PM',
                    'contact_person': 'Jennifer Lee'
                }
            ),
            Customer(
                name='Heritage Bank',
                email='ops@heritagebank.com',
                phone='+1-555-1003',
                address='300 Financial District, Banking City, State 54321',
                profile_data={
                    'industry': 'Financial Services',
                    'security_level': 'Maximum',
                    'compliance_requirements': ['SOX', 'PCI-DSS'],
                    'contact_person': 'David Thompson'
                }
            ),
            Customer(
                name='City Hospital',
                email='security@cityhospital.org',
                phone='+1-555-1004',
                address='400 Medical Center Dr, Healthcare City, State 54321',
                profile_data={
                    'industry': 'Healthcare',
                    'facility_type': 'Hospital',
                    'bed_count': 300,
                    'contact_person': 'Dr. Maria Rodriguez'
                }
            )
        ]
        
        for customer in customers:
            db.session.add(customer)
        
        db.session.commit()
        
        # Create Appointments (need to commit users and customers first)
        base_date = datetime.now()
        appointments = [
            Appointment(
                booking_datetime=base_date + timedelta(hours=2),
                status='scheduled',
                customer_id=1,
                user_id=2,
                details={
                    'service_type': 'Security System Maintenance',
                    'estimated_duration': '2 hours',
                    'special_instructions': 'Access through main entrance, ask for Robert Miller'
                }
            ),
            Appointment(
                booking_datetime=base_date + timedelta(days=1, hours=9),
                status='scheduled',
                customer_id=2,
                user_id=3,
                details={
                    'service_type': 'Camera Installation',
                    'estimated_duration': '4 hours',
                    'equipment_needed': ['IP Cameras', 'Network Cables', 'Mounting Hardware']
                }
            ),
            Appointment(
                booking_datetime=base_date - timedelta(days=1),
                status='complete',
                customer_id=3,
                user_id=2,
                disposition_id='COMPLETED',
                details={
                    'service_type': 'Security Audit',
                    'estimated_duration': '3 hours',
                    'completed_tasks': ['Perimeter check', 'Access control review', 'Camera functionality test']
                }
            ),
            Appointment(
                booking_datetime=base_date + timedelta(days=2, hours=14),
                status='unassigned',
                customer_id=4,
                details={
                    'service_type': 'Emergency Response System Check',
                    'estimated_duration': '1.5 hours',
                    'priority': 'High'
                }
            ),
            Appointment(
                booking_datetime=base_date - timedelta(days=2),
                status='complete',
                customer_id=1,
                user_id=3,
                disposition_id='COMPLETED',
                details={
                    'service_type': 'Quarterly Security Review',
                    'estimated_duration': '2 hours',
                    'report_generated': True
                }
            )
        ]
        
        for appointment in appointments:
            db.session.add(appointment)
        
        db.session.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")
        raise