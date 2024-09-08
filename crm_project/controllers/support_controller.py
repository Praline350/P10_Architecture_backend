from crm_project.models import *
from datetime import datetime
from crm_project.project.permissions import *


class SupportController:
    def __init__(self, session, authenticated_user, login_controller):
        self.session = session
        self.authenticated_user = authenticated_user
        self.login_controller = login_controller