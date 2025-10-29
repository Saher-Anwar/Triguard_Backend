from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import JSONB

# Association table for many-to-many relationship between roles and permissions
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_code', db.String(50), db.ForeignKey('permissions.code'), primary_key=True)
)

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    code = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Permission {self.code}>'
    
    def to_dict(self):
        return {
            'code': self.code,
            'description': self.description,
            'roles': [role.name for role in self.roles] if self.roles else []
        }

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    permissions = db.relationship('Permission', secondary=role_permissions, backref='roles')
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    def to_dict(self):
      return {
          'id': str(self.id),
          'name': self.name,
          'permissions': [
              {
                  'code': perm.code,
                  'description': perm.description
              } for perm in self.permissions
          ] if self.permissions else []
      }


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum('on-site', 'en-route', 'available', 'offline', name='user_status'), 
                      default='available')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    profile = db.Column(JSONB, nullable=True)
    
    role = db.relationship('Role', backref='users')
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),  # Convert to string for frontend
            'name': self.name,
            'email': self.email, 
            'avatar': self.avatar,
            'permissions': [perm.to_dict() for perm in self.role.permissions] if self.role else [],
            'role': self.role.to_dict() if self.role else None,
            'status': self.status,
            'profile': self.profile if self.profile else {}
        }

class Disposition(db.Model):
    __tablename__ = 'dispositions'
    
    code = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Disposition {self.code}>'
    
    def to_dict(self):
        return {
            'code': self.code,
            'description': self.description
        }

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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'profile_data': self.profile_data
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('unassigned', 'scheduled', 'in progress', 'complete', 'cancelled', 'rescheduled',
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
                'status': self.user.status
            } if self.user else None
        }