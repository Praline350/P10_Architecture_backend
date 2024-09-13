from datetime import datetime

from crm_project.models import *
from crm_project.project.permissions import *
from crm_project.controllers.main_controller import MainController

@decorate_all_methods(is_authenticated_user)
class SupportController():
    def __init__(self, session, authenticated_user, login_controller):
        self.session = session
        self.authenticated_user = authenticated_user
        self.login_controller = login_controller