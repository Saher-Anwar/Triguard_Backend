from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import JSONB

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    code = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Permission {self.code}>'

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions_id = db.Column(db.String(50), db.ForeignKey('permissions.code'), nullable=False)
    
    permission = db.relationship('Permission', backref='roles')
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('on-site', 'en-route', 'available', 'offline', name='user_status'), 
                      default='offline')
    permissions_id = db.Column(db.String(50), db.ForeignKey('permissions.code'), nullable=False)
    
    permission = db.relationship('Permission', backref='users')
    
    def __repr__(self):
        return f'<User {self.name}>'

class Disposition(db.Model):
    __tablename__ = 'dispositions'
    
    code = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Disposition {self.code}>'

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    profile_data = db.Column(JSONB)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('unassigned', 'scheduled', 'in progress', 'complete', 
                              name='appointment_status'), default='unassigned')
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    details = db.Column(JSONB)
    disposition_id = db.Column(db.String(50), db.ForeignKey('dispositions.code'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    customer = db.relationship('Customer', backref='appointments')
    disposition = db.relationship('Disposition', backref='appointments')
    user = db.relationship('User', backref='appointments')
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_datetime': self.booking_datetime.isoformat() if self.booking_datetime else None,
            'status': self.status,
            'customer': {
                'id': self.customer.id,
                'name': self.customer.name,
                'email': self.customer.email,
                'phone': self.customer.phone,
                'address': self.customer.address
            } if self.customer else None,
            'details': self.details,
            'disposition': {
                'code': self.disposition.code,
                'description': self.disposition.description
            } if self.disposition else None,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email,
                'status': self.user.status
            } if self.user else None
        }