from datetime import datetime

from sqlalchemy.orm.attributes import flag_modified

from crm_project.models import *
from crm_project.project.permissions import *
from crm_project.helpers.get_data import *


class CommercialController:
    def __init__(self, session, authenticated_user, login_controller):
        self.session = session
        self.authenticated_user = authenticated_user
        self.login_controller = login_controller

    @require_permission('create_customer')
    def create_customer(self, **customer_data):
        new_customer = Customer(
            first_name=customer_data['first_name'],
            last_name=customer_data['last_name'],
            email=customer_data['email'],
            company_name=customer_data['company_name'],
            commercial_contact_id=self.authenticated_user.id
        )
        self.session.add(new_customer)
        self.session.commit()
        return new_customer
    
    @require_permission('update_customer')
    def update_customer(self,  customer_id, **kwargs):
        try:    
            customer = self.session.query(Customer).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer {customer_id} not found.")
            for key, value in kwargs.items():
                setattr(customer, key, value)
            self.session.commit()
            return customer
        except Exception as e:
            self.session.rollback()  
            raise ValueError(f"An error occurred while updating customer: {str(e)}")
    
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
        if filter_data['customer_id'] is not None:
            query = query.filter_by(customer_id=filter_data['customer_id'])
            
        query = query.filter(Contract.amount_due >= filter_data['amount_due_min'])
        query = query.filter(Contract.amount_due <= filter_data['amount_due_max'])
        query = query.filter(Contract.creation_date <= filter_data['creation_date_before'])
        query = query.filter(Contract.creation_date >= filter_data['creation_date_after'])

        return query.all()