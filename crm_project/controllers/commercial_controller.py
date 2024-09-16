from datetime import datetime

from sqlalchemy.orm.attributes import flag_modified

from crm_project.controllers.main_controller import MainController
from crm_project.models import *
from crm_project.project.permissions import *
from crm_project.helpers.get_data import *


@decorate_all_methods(is_authenticated_user)
class CommercialController(MainController):
    def __init__(self, session, authenticated_user, login_controller):
        self.session = session
        self.authenticated_user = authenticated_user
        self.login_controller = login_controller


    @require_permission('create_customer')
    def create_customer(self, **customer_data):
        try:
            new_customer = Customer(
                name=customer_data['name'],
                email=customer_data['email'],
                phone_number=customer_data['phone_number'],
                company_name=customer_data['company_name'],
                commercial_contact_id=self.authenticated_user.id
            )
            self.session.add(new_customer)
            self.session.commit()
            return new_customer
        except Exception as e:
            raise ValueError(f"An error occurred while creating the customer: {str(e)}")


    @require_permission('update_customer')
    def update_customer(self,  customer_id, **updated_data):
        try:    
            customer = self.session.query(Customer).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer {customer_id} not found.")
            for key, value in updated_data.items():
                setattr(customer, key, value)
            self.session.commit()
            return customer
        except Exception as e:
            raise ValueError(f"An error occurred while updating customer: {str(e)}")
    

    @require_permission('get_contracts')
    def contract_filter(self, **filter_data):
        query = self.session.query(Contract)
        if 'status' in filter_data:
            query = query.filter_by(status=filter_data['status'])
        if filter_data['paid'] is not None:
            if filter_data['paid']:
                query = query.filter_by(remaining_amount=0)  # Contrats payés
            else:
                query = query.filter(Contract.remaining_amount > 0)  # Contrats non payés
        if filter_data['customer_id'] != 'All Customers':
            query = query.filter_by(customer_id=filter_data['customer_id'])

        query = query.filter(Contract.amount_due >= filter_data['amount_due_min'])
        query = query.filter(Contract.amount_due <= filter_data['amount_due_max'])
        query = query.filter(Contract.creation_date <= filter_data['creation_date_before'])
        query = query.filter(Contract.creation_date >= filter_data['creation_date_after'])
        return query.all()

    @require_permission('create_event')
    def create_event(self, **event_data):
        try:
            new_event = Event(
                name=event_data['name'],
                start_date=event_data['start_date'],
                end_date=event_data['end_date'],
                location=event_data['location'],
                attendees=event_data['attendees'],
                comment=event_data['comment'],
                contract_id=event_data['contract_id']
            )
            self.session.add(new_event)
            self.session.commit()
            return new_event
        except Exception as e:
            raise ValueError(f"An error occurred while create event: {str(e)}")
    

