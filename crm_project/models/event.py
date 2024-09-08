from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR

from project.config import Base
from models.mixin_model import BaseModelMixin

# Modèle Event
class Event(Base, BaseModelMixin):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    contract_id = Column(CHAR(36), ForeignKey('contracts.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    support_contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    location = Column(String(100), nullable=False)
    attendees = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    # Relations vers Contract, Customer, User
    contract = relationship("Contract", back_populates="events")
    client = relationship("Customer")
    support_contact = relationship("User")

    def __repr__(self):
        return f"<Event(name={self.name}, location={self.location}, attendees={self.attendees})>"