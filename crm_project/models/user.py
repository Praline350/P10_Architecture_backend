import re
import enum
import bcrypt

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship

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
        return self.name

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
    
    @staticmethod
    def validate_username(username):
        return bool(re.match("^[a-zA-Z0-9_.-]+$", username))

    @staticmethod
    def validate_employee_number(employee_number):
        return employee_number.isdigit() and len(employee_number) <= 3

    @staticmethod
    def validate_password(password):
        return len(password) >= 4 # à changer ! (pour le dev pour l'instant)
    
    def __repr__(self):
        return (f"<User(id={self.id}, username={self.username}, "
                f"email={self.email})>")
    

