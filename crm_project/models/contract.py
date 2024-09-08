from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import event
from datetime import datetime, timezone
from crm_project.project.config import Base
from crm_project.models.mixin_model import BaseModelMixin


# Modèle Contract
class Contract(Base, BaseModelMixin):
    __tablename__ = 'contracts'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount_due = Column(Integer, nullable=False)
    remaining_amount = Column(Integer, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    last_update = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = Column(Boolean, default=False)

    commercial_contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    commercial_contact = relationship("User")

    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship("Customer", back_populates="contracts")

    
    events = relationship("Event", back_populates="contract")

    def __repr__(self):
        return f"<Contract(id={self.id}, amount_due={self.amount_due}, status={self.status})>"
    
    def validate_commercial_contact(self):
        """Vérifie que le commercial_contact est bien celui associé au customer."""

        if self.commercial_contact_id != self.customer.commercial_contact_id:
            raise ValueError("Le commercial contact doit être le même que celui associé au client.")

@event.listens_for(Contract, 'before_insert')
def set_creation_date(mapper, connection, target):
    target.creation_date = datetime.now(timezone.utc)
    target.last_update = datetime.now(timezone.utc)

@event.listens_for(Contract, 'before_update')
def set_last_update(mapper, connection, target):
    target.last_update = datetime.now(timezone.utc)