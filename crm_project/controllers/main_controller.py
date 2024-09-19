from crm_project.models import *
from crm_project.project.permissions import *

from sqlalchemy.exc import IntegrityError


class MainController:
    def __init__(self, session, authenticated_user):
        self.session = session
        self.authenticated_user = authenticated_user

    
    @require_permission('update_contract')
    def update_contract(self, contract_id, **contract_data):
        """Update a existent contract with his ID and contract data"""

        try:
            contract = self.session.query(Contract).filter_by(id=contract_id).one()
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
            raise ValueError(f"An error occurred while updating contract: {str(e)}")
        
    @require_permission('update_event')
    def update_event(self, event_id, **event_data):
        """Update an event with his ID and event data"""

        try:
            print(event_data['support_contact_id'])
            event = self.session.query(Event).filter_by(id=event_id).one()
            if not event:
                raise ValueError(f"Contract {event_id} not found.")
            for key, value in event_data.items():
                setattr(event, key, value)
            self.session.commit()
        except Exception as e:
            raise ValueError(f"An error occurred while updating event: {str(e)}")
        return event

    @require_permission('get_events')
    def event_filter(self, **filter_data):
        """Return event list with apply filters"""
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
        """Change current username of auth user"""

        try:
            user = self.session.query(User).filter_by(id=self.authenticated_user.id).one()
            user.username = username
            self.session.commit()
            return user
        except IntegrityError as e:
            # Annuler la transaction en cas d'erreur d'intégrité
            self.session.rollback()
            return False        
    @is_authenticated_user
    def change_user_password(self, old_password, new_password):
        """Change current password of auth user"""

        try:
            user = self.session.query(User).filter_by(id=self.authenticated_user.id).one()
            if user and user.check_password(old_password):
                user.set_password(new_password)
                self.session.commit()
                return True
        except IntegrityError as e:
            # Annuler la transaction en cas d'erreur d'intégrité
            self.session.rollback()
            raise ValueError(f"An error occurred: {e}")

