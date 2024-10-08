from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.mysql import CHAR

import re
from datetime import datetime

from crm_project.project.config import Base
from crm_project.models.mixin_model import BaseModelMixin


# Modèle Event
class Event(Base, BaseModelMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=False)
    attendees = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    contract_id = Column(CHAR(36), ForeignKey("contracts.id"), nullable=False)
    contract = relationship("Contract", back_populates="events")

    support_contact_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    support_contact = relationship("User")

    @validates("contract_id")
    def validate_contract_id(self, key, contract_id):
        if contract_id is None or contract_id == "":
            raise ValueError("Contract ID cannot be null or empty")
        return contract_id

    @validates("name")
    def validate_name(self, key, name):
        # Supprimer les espaces superflus
        name = name.strip()
        if not name:
            raise ValueError("Event name cannot be empty")
        # Accepter les lettres, chiffres, accents, et caractères spéciaux comme @, #, &, etc.
        if not re.match(r"^[\wÀ-ÿ'@#&\s\-]+$", name):
            raise ValueError("Invalid event name format")
        return name

    @validates("attendees")
    def validate_attendees(self, key, attendees):
        try:
            attendees = int(attendees)
        except (ValueError, TypeError):
            raise ValueError("Attendees must be a positive integer")

        # Vérifier que le nombre de participants est positif
        if attendees < 1:
            raise ValueError("Attendees must be a positive integer")

        return attendees

    @validates("start_date", "end_date")
    def validate_dates(self, key, date):
        if key == "end_date" and self.start_date and date <= self.start_date:
            raise ValueError("End date must be after start date")

        return date

    @validates("location")
    def validate_location(self, key, location):
        location = location.strip()
        if not location:
            raise ValueError("Event location cannot be empty")
        # Accepter les lettres, accents, tirets, apostrophes, espaces, et certains caractères spéciaux
        if not re.match(r"^[\wÀ-ÿ'@#&\s\-]+$", location):
            raise ValueError("Invalid location format")
        return location

    def __repr__(self):
        return f"<Event(name={self.name}, location={self.location}, attendees={self.attendees})>"
