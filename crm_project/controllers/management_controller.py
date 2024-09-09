from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from crm_project.models import *
from datetime import datetime
from crm_project.project.permissions import *


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
    def create_user(self,**user_data):
        try:
            username = f"{user_data['first_name']}.{user_data['last_name']}"
            role = self.session.query(Role).filter_by(name=user_data['role']).one()
            if not User.validate_username(username):
                raise ValueError("Invalid username")
            if not User.validate_employee_number(user_data['employee_number']):
                raise ValueError("Invalid employee number")
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

    @require_permission('update_user')
    def update_user(self, user_id, **user_data):
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            role = self.session.query(Role).filter_by(name=user_data['role']).one()
            user_data['role'] = role
            if not user:
                raise ValueError(f"user {user_id} not found")
            if not User.validate_username(user_data['username']):
                raise ValueError("Invalid username")
            if not User.validate_employee_number(user_data['employee_number']):
                raise ValueError("Invalid employee number")
            for key, value in user_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()  
            raise ValueError(f"An error occurred while updating the user: {str(e)}")
    
    @require_permission('delete_user')
    def delete_user(self, user_id):
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            self.session.delete(user)
            self.session.commit()
            return f"User {user.username} successfully deleted."
        except Exception as e:
            self.session.rollback() 
            raise ValueError(f"An error occurred while deleting the user: {str(e)}")

    @require_permission('update_user')
    def get_user_list(self):
        try:
            users = self.session.query(User).all()
            user_list = [user.to_dict() for user in users]
            return user_list
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error during get users: {e}")
            return None
