from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
import random
import string

from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import event
from datetime import datetime, timezone
from crm_project.project.config import Base
from crm_project.models.mixin_model import BaseModelMixin



def generate_simple_id():
    # Générer une lettre majuscule aléatoire
    letter = random.choice(string.ascii_uppercase)
    # Générer un nombre aléatoire de 4 chiffres
    number = ''.join(random.choices(string.digits, k=4))
    # Combiner la lettre et les chiffres
    return f"{letter}{number}"

# Modèle Contract
class Contract(Base, BaseModelMixin):
    __tablename__ = 'contracts'

    id = Column(CHAR(5), primary_key=True, default=generate_simple_id)
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

