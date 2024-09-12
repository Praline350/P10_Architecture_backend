from sqlalchemy.exc import SQLAlchemyError

from crm_project.models import *
from crm_project.project.permissions import *

class MainController:
    def __init__(self, session, authenticated_user):
        self.session = session
        self.authenticated_user = authenticated_user

    
    @require_permission('update_contract')
    def update_contract(self, contract_id, **kwargs):
        try:
            contract = self.session.query(Contract).filter_by(id=contract_id).first()
            if not contract:
                raise ValueError(f"Contract {contract_id} not found.")
            for key, value in kwargs.items():
                if key in ['amount_due', 'remaining_amount']:
                    value = int(value)
                elif key == 'status':
                    value = bool(value)
                setattr(contract, key, value)
            self.session.commit()
            return contract
        except Exception as e:
            self.session.rollback()  
            raise ValueError(f"An error occurred while updating contract: {str(e)}")


    def change_user_username(self, username):
        try:
            user = self.session.query(User).filter_by(id=self.authenticated_user.id).first()
            if not User.validate_username(username):
                raise ValueError("Invalid username")
            user.username = username
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()  
            raise ValueError(f"An error occurred while updating username: {str(e)}")
        
    def change_user_password(self, old_password, new_password):
        try:
            if not User.validate_password(new_password):
                print("Password must be at least 8 characters long.")
                return False
            user = self.session.query(User).filter_by(id=self.authenticated_user.id).first()
            if user and user.check_password(old_password):
                user.set_password(new_password)
                self.session.commit()
                return True
            else:
                print("Old password is incorrect or user not found.")
                return False
        except SQLAlchemyError as db_error:
            # Gérer les erreurs liées à la base de données
            print(f"Database error occurred: {str(db_error)}")
            self.session.rollback()  # Annuler la transaction en cas d'erreur
            return False
        
        except Exception as e:
            # Gérer les autres erreurs non spécifiées
            print(f"An unexpected error occurred: {str(e)}")
            return False
