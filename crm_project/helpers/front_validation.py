"""
    Helper for views validation fields
"""

import re

from PySide6.QtWidgets import QMessageBox


# Validation du prénom et nom (suppression des espaces et validation des caractères)
def validate_name(field_name, value, dialog):
    value = value.strip()
    if not value:
        QMessageBox.warning(dialog, "Input Error", f"{field_name} cannot be empty.")
        return False
    if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", value):
        QMessageBox.warning(
            dialog,
            "Input Error",
            f"Invalid {field_name}. Only letters, hyphens, and spaces are allowed.",
        )
        return False
    return True


# Validation de l'email avec une regex
def validate_email(email, dialog):
    email_regex = r"^[\w\-.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        QMessageBox.warning(dialog, "Input Error", "Invalid email format.")
        return False
    return True


# Validation du numéro d'employé (doit être un nombre)
def validate_employee_number(employee_number, dialog):
    if not employee_number.isdigit():
        QMessageBox.warning(
            dialog, "Input Error", "Employee number must be a valid number."
        )
        return False
    return True


# Validation du mot de passe (vérifie la longueur et la correspondance avec la confirmation)
def validate_passwords(password, confirm_password, dialog):
    if len(password) < 8:
        QMessageBox.warning(
            dialog, "Input Error", "New password must be at least 8 characters long."
        )
        return False
    if password != confirm_password:
        QMessageBox.warning(dialog, "Input Error", "Passwords do not match.")
        return False
    return True


# Validation pour les montants (amount_due et remaining_amount) - doivent être des nombres positifs
def validate_amount(field_name, value, dialog):
    try:
        amount = float(value)
        if amount < 0:
            raise ValueError
    except ValueError:
        QMessageBox.warning(
            dialog, "Input Error", f"{field_name} must be a positive number."
        )
        return False
    return True


# Validation du nom de l'événement (ne doit pas être vide et doit respecter un format)
def validate_event_name(name, dialog):
    name = name.strip()
    if not name:
        QMessageBox.warning(dialog, "Input Error", "Event name cannot be empty.")
        return False
    if not re.match(r"^[a-zA-ZÀ-ÿ0-9' -]+$", name):
        QMessageBox.warning(
            dialog,
            "Input Error",
            "Invalid event name format. Only letters, numbers, hyphens, and spaces are allowed.",
        )
        return False
    return True


# Validation du nombre de participants (attendees) - doit être un entier positif
def validate_attendees(attendees, dialog):
    try:
        attendees = int(attendees)
        if attendees < 1:
            raise ValueError
    except (ValueError, TypeError):
        QMessageBox.warning(
            dialog, "Input Error", "Attendees must be a positive integer."
        )
        return False
    return True


# Validation de la location (ne doit pas être vide et doit respecter un format)
def validate_location(location, dialog):
    location = location.strip()
    if not location:
        QMessageBox.warning(dialog, "Input Error", "Location cannot be empty.")
        return False
    if not re.match(r"^[a-zA-ZÀ-ÿ0-9' -]+$", location):
        QMessageBox.warning(
            dialog,
            "Input Error",
            "Invalid location format. Only letters, numbers, hyphens, and spaces are allowed.",
        )
        return False
    return True


# Validation du commentaire (optionnel, mais doit respecter une longueur maximale)
def validate_comment(comment, dialog, max_length=500):
    comment = comment.strip()
    if len(comment) > max_length:
        QMessageBox.warning(
            dialog, "Input Error", f"Comment cannot exceed {max_length} characters."
        )
        return False
    return True
