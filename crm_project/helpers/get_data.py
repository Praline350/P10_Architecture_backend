"""
    Helper for get data
"""

from crm_project.models import *
from crm_project.project.permissions import *


@is_authenticated_user
def get_roles_list(controller):
    roles = [role.name for role in RoleName]
    return roles


@is_authenticated_user
def get_roles_without_admin(controller):
    session = controller.session
    roles = session.query(Role).filter(Role.id != 1).all()  # Admin
    return roles




@is_authenticated_user
def get_customers_commercial(controller):
    # Retourne les client lié au commercial(authenticated)
    session = controller.session
    user = controller.authenticated_user
    commercial_customers = (
        session.query(Customer).filter_by(commercial_contact_id=user.id).all()
    )
    return commercial_customers


@is_authenticated_user
def get_contract_commercial(controller, user):
    session = controller.session
    customers = session.query(Customer).filter_by(commercial_contact_id=user.id).all()
    customers_ids = [customer.id for customer in customers]
    if not customers_ids:
        return None
    contracts = (
        session.query(Contract).filter(Contract.customer_id.in_(customers_ids)).all()
    )
    return contracts


@is_authenticated_user
def get_customers_list(controller):
    session = controller.session
    customers = session.query(Customer).all()
    return customers

@is_authenticated_user
def get_events_list(controller):
    session = controller.session
    events = session.query(Event).all()
    return events

@is_authenticated_user
def get_events_support_list(controller, support_id):
    session = controller.session
    events = session.query(Event).filter_by(support_contact_id=support_id).all()
    return events


@is_authenticated_user
def get_contracts_list(controller):
    session = controller.session
    contracts = session.query(Contract).all()
    return contracts


@is_authenticated_user
def get_contract_by_customer(controller, customer_id):
    session = controller.session
    contracts = session.query(Contract).filter_by(customer_id=customer_id).all()
    return contracts


@is_authenticated_user
def get_users(controller):
    session = controller.session
    users = session.query(User).all()
    return users


@is_authenticated_user
def get_commercials(controller):
    session = controller.session
    commercials = (
        session.query(User).filter(User.role.has(name=RoleName.COMMERCIAL)).all()
    )
    return commercials


@is_authenticated_user
def get_support_user(controller):
    session = controller.session
    supports = session.query(User).filter(User.role.has(name=RoleName.SUPPORT)).all()
    return supports


@is_authenticated_user
def get_status_contract(controller, contract_id):
    session = controller.session
    contract = session.query(Contract).filter_by(id=contract_id).first()
    if contract.remaining_amount > 0:
        return False
    else:
        return True


@is_authenticated_user
def get_display_customer_name(controller, customers):
    return [f"{customer.id} - {customer.name}" for customer in customers]
