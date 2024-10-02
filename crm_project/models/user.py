import re
import enum
import bcrypt

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship, validates

from crm_project.project.config import Base
from  crm_project.models.mixin_model import BaseModelMixin



class RoleName(enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    COMMERCIAL = 'COMMERCIAL'
    SUPPORT = 'SUPPORT'
    MANAGEMENT = 'MANAGEMENT'

# Table d'association entre les rôles et les permissions
role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255))

    # Relationship with Role
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(RoleName), unique=True, index=True)
    description = Column(String(255))

    # Relationship with Permission
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

    # Relationship with User
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return self.name.value
    
    def __str__(self):
        return self.name.value

class User(Base, BaseModelMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(Integer, nullable=False)
    email = Column(String(100), unique=True, index=True)
    first_name = Column(String(100), unique=False, index=True)
    last_name = Column(String(100), unique=False, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # ForeignKey to Role
    role_id = Column(Integer, ForeignKey('roles.id'))
    # RelationShip with Role
    role = relationship("Role", back_populates="users")

    def set_password(self, password):
        # Salage et hashage du password avant de l'enregistrer
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        # Vérifie le password avec sa valeur hashée dans la db
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def has_permission(self, permission_name):
        # Retourne True si l'utilisateur a la permission passée en argument
        return any(permission.name == permission_name for permission in self.role.permissions)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        name = name.replace(" ", "")
        if not re.match("^[a-zA-ZÀ-ÿ'-]+$", name):
            raise ValueError(f"Invalid {key}. Only letters, hyphens, and apostrophes are allowed.")
        return name
    
    @validates('email')
    def validate_email(self, key, email):   
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    @validates('username')
    def validate_username(self, key, username):
        username = username.replace(" ", "")
        if not username or not re.match("^[a-zA-Z0-9_.-]+$", username):
            raise ValueError("Invalid username format")
        return username

    @validates('employee_number')
    def validate_employee_number(self, key, employee_number):
        employee_number_str = str(employee_number)
        if not employee_number_str.isdigit() or len(employee_number_str) > 3:
            raise ValueError("Employee number must be numeric and less than or equal to 3 digits")
        return employee_number

    @validates('hashed_password')
    def validate_password(self, key, password):
        if len(password) < 3:
            raise ValueError("Password must be at least 8 characters long")
        return password
    
    def __repr__(self):
        return (f"<User(id={self.id}, username={self.username}, "
                f"email={self.email})>")
    

