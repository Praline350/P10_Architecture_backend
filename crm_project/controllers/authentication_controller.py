from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from crm_project.project.config import SessionLocal
from crm_project.models import *
from crm_project.views import *
from crm_project.views.admin_view import AdminView
from crm_project.controllers import *
from crm_project.controllers.main_controller import MainController


class AuthenticationController(MainController):
    def __init__(self, session ,main_window):
        self.session = session
        self.authenticated_user = None
        self.views = {}
        self.main_window = main_window
        self.login_view = None

        self.view_mapping = {
            'ADMIN': (AdminView, AdminController),
            'COMMERCIAL': (CommercialView, CommercialController),
            'SUPPORT': (SupportView, SupportController),
            'MANAGEMENT': (ManagementView, ManagementController)
        }

    def get_view_for_role(self, role_name):
        """Créer et retourner la vue correspondant au rôle si elle n'existe pas déjà"""
        view_class, controller_class = self.view_mapping.get(role_name, (None, None))
        if view_class and controller_class:
            controller = controller_class(self.session, self.authenticated_user, self)
            return view_class(self.main_window, controller)  # Retourne une nouvelle instance de la vue
        else:
            print(f"Role '{role_name}' not found.")
            return None


    def login(self, username, employee_number, password):
        # if not User.validate_username(username):
        #     print("Invalid username format.")
        #     return None
        # if not User.validate_employee_number(employee_number):
        #     print("Invalid employee number format.")
        #     return None
        # if not User.validate_password(password):
        #     print("Password must be at least 8 characters long.")
        #     return None
        user = self.session.query(User).filter_by(username=username, employee_number=employee_number).first()
        if user and user.check_password(password):
            print(f"Login successful. User role: {user.role.name}")
            self.authenticated_user = user
            return user
        return None

    def show_frame(self, user):
        # self.setup_views()
        role_name = user.role.name.value
        if role_name:
            if hasattr(self, 'login_view'):
                self.main_window.centralWidget().deleteLater()
            # Afficher la frame correspondant au rôle
            frame = self.get_view_for_role(role_name)
            if frame:
                self.main_window.menuBar().show()
                self.main_window.setCentralWidget(frame)
                print("Frame shown successfully.")
                return True
            else:
                print(f"No frame found for role: {role_name}")
                return False

    def show_login_view(self):
        if self.authenticated_user:
            self.authenticated_user = None
        if self.session:
            self.session.close()
        self.session = SessionLocal()
        self.login_view = LoginWidget(self.main_window, self)
        self.main_window.setCentralWidget(self.login_view)
