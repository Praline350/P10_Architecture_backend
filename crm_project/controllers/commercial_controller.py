from models import *
from datetime import datetime
from project.permissions import *
from helpers.get_data import *


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
    def update_customer(self,  customer_name, **kwargs):
        customer = self.session.query(Customer).filter_by(name=customer_name).first()
        if not customer:
            raise ValueError(f"Customer {customer_name} not found.")
        for key, value in kwargs.items():
            setattr(customer, key, value)
        self.session.commit()
        return customer
    
    @require_permission('update_contract')
    def update_contract(self, customer_name, contract_id, **kwargs):
        customer = self.session.query(Customer).filter_by(name=customer_name).first()
        if not customer:
            raise ValueError(f"Customer {customer_name} not found.")
        contract = self.session.query(Contract).filter_by(id=contract_id,customer_id=customer.id).first()
        if not contract:
            raise ValueError(f"Contract {contract_id} for customer {customer_name} not found.")
        for key, value in kwargs.items():
            setattr(contract, key, value)
        self.session.commit()
        return contract
    

    def contract_filter(self, filter_type, filter_value):
        query = self.session.query(Contract)
        
        # Applique le filtre en fonction de la clé
        match filter_type:
            case 'status':
                query = query.filter_by(status=filter_value)
            case 'amount_due_greater':
                query = query.filter(Contract.amount_due > filter_value)
            case 'amount_due_less':
                query = query.filter(Contract.amount_due < filter_value)
            case 'remaining_amount_greater':
                query = query.filter(Contract.remaining_amount > filter_value)
            case 'remaining_amount_less':
                query = query.filter(Contract.remaining_amount < filter_value)
            case 'creation_date_before':
                query = query.filter(Contract.creation_date < filter_value)
            case 'creation_date_after':
                query = query.filter(Contract.creation_date > filter_value)


        return query.all()
