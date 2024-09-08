from crm_project.models import *
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from crm_project.project.permissions import *




def get_roles_list():
    try:
        # Récupérer tous les rôles de l'enum RoleName
        roles = [role.name for role in RoleName]
        return roles
    except Exception as e:
        print(f"Error while retrieving roles: {e}")
        return None


def get_customers_commercial(user, session):
    # Retourne les client lié au commercial(user)
    try:
        commercial_customers = session.query(Customer).filter_by(commercial_contact_id=user.id).all()
        customer_list = [customer.to_dict() for customer in commercial_customers]
        return customer_list
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during get customers: {e}")
        return None

def get_contract_commercial(user, session):
    try:
        customers = session.query(Customer).filter_by(commercial_contact_id=user.id).all()
        customers_ids = [customer.id  for customer in customers]
        if not customers_ids:
            return None
        contracts = session.query(Contract).filter(Contract.customer_id.in_(customers_ids)).all()
        contract_list = [contract.to_dict() for contract in contracts]
        return contract_list
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during get contracts: {e}")
        return None

def get_customers_list(session):
    try:
        customers = session.query(Customer).all()
        customers_list = [customer.to_dict() for customer in customers]
        return customers_list
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during get customers: {e}")
        return None
    
def get_customers_complet_name(session):
    try:
        customers = session.query(Customer).all()
        customers_info = [{"id": customer.id, "name": f"{customer.first_name} {customer.last_name}"} for customer in customers]
        return customers_info
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during get customers' names: {e}")
        return None

def get_events_list(session):
    try:
        events = session.query(Event).all()
        return events
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during get events: {e}")
        return None

def get_contracts_list(session):
    try:
        contracts = session.query(Contract).all()
        return contracts
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during get contracts: {e}")
        return None
    

    
