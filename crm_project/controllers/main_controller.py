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
