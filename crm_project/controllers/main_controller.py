from sqlalchemy.exc import SQLAlchemyError

from crm_project.models import *
from crm_project.project.permissions import *

class MainController:
    def __init__(self, session, authenticated_user):
        self.session = session
        self.authenticated_user = authenticated_user

    
    @require_permission('update_contract')
    def update_contract(self, contract_id, **contract_data):
        try:
            contract = self.session.query(Contract).filter_by(id=contract_id).first()
            if not contract:
                raise ValueError(f"Contract {contract_id} not found.")
            for key, value in contract_data.items():
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
        
    @require_permission('update_event')
    def update_event(self, event_id, **event_data):
        try:
            print(event_data['support_contact_id'])
            event = self.session.query(Event).filter_by(id=event_id).first()
            if not event:
                raise ValueError(f"Contract {event_id} not found.")
            for key, value in event_data.items():
                setattr(event, key, value)
            self.session.commit()
        except Exception as e:
            self.session.rollback()  
            raise ValueError(f"An error occurred while updating event: {str(e)}")
        return event

    @require_permission('get_events')
    def event_filter(self, **filter_data):
        print(f" filter data : {filter_data}")
        query = self.session.query(Event)
        match self.authenticated_user.role.name.value:
            case 'SUPPORT':
                if filter_data.get('only'):
                    query = query.filter_by(support_contact_id=self.authenticated_user.id)
            case _:
                if filter_data.get('associate_support'):
                    query = query.filter(Event.support_contact_id.isnot(None))
        if filter_data['contract_id'] != None:
            query = query.filter_by(contract_id=filter_data['contract_id'])
        if filter_data.get('start_date_after'):
            query = query.filter(Event.start_date >= filter_data['start_date_after'])
        if filter_data.get('start_date_before'):
            query = query.filter(Event.start_date <= filter_data['start_date_before'])
        if filter_data['location'] != "":
            query = query.filter_by(location=filter_data["location"])
        return query.all()

    @is_authenticated_user
    def change_user_username(self, username):
        try:
            user = self.session.query(User).filter_by(id=self.authenticated_user.id).first()
            user.username = username
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()  
            raise ValueError(f"An error occurred while updating username: {str(e)}")
        
    @is_authenticated_user
    def change_user_password(self, old_password, new_password):
        try:
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
