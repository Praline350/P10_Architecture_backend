from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import *
from datetime import datetime
from project.permissions import *


class ManagementController:
    def __init__(self, session, authenticated_user, login_controller):
        self.session = session
        self.authenticated_user = authenticated_user
        self.login_controller = login_controller
    

    @require_permission('create_contract')
    def create_contract(self, customer_id, **contract_data):
        customer = self.session.query(Customer).filter_by(id=customer_id).first()
        commercial_contact_id = customer.commercial_contact_id
        new_contract = Contract(
            amount_due=contract_data['amount_due'],
            remaining_amount=contract_data['remaining_amount'],
            customer_id=customer_id,
            commercial_contact_id=commercial_contact_id
        )
        self.session.add(new_contract)
        self.session.commit()
        return new_contract
    
    @require_permission('create_user')
    def create_user(self, **user_data):
        print(user_data)
        try:
            username = f"{user_data['first_name']}.{user_data['last_name']}"
            role = self.session.query(Role).filter_by(name=user_data['role']).one()
            new_user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                employee_number=int(user_data['employee_number']),
                email=user_data['email'],
                username=username,
                role=role
            )
            new_user.set_password(user_data['password'])  # Le hachage et le salage sont gérés ici

            self.session.add(new_user)
            self.session.commit()
            return new_user  # Retourne l'utilisateur créé

        except IntegrityError:
            self.session.rollback()
            raise ValueError("L'utilisateur avec cet email ou ce nom d'utilisateur existe déjà.")
