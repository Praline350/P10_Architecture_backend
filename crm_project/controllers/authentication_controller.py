from crm_project.models import *
from crm_project.views import *
from crm_project.views.commercial_view import CommercialView
from crm_project.views.admin_view import AdminView
from crm_project.controllers import *
from crm_project.controllers.commercial_controller import CommercialController
from crm_project.controllers.main_controller import MainController


class AuthenticationController(MainController):
    def __init__(self, session ,main_window):
        self.session = session
        self.authenticated_user = None
        self.views = {}
        self.main_window = main_window
        self.login_view = None

        # Map views with controllers
        self.view_mapping = {
            'ADMIN': (AdminView, AdminController),
            'COMMERCIAL': (CommercialView, CommercialController),
            'SUPPORT': (SupportView, SupportController),
            'MANAGEMENT': (ManagementView, ManagementController)
        }

    def get_view_for_role(self, role_name):
        """Return view associate to the role"""

        try:
            view_class, controller_class = self.view_mapping.get(role_name, (None, None))
            if not view_class or not controller_class:
                raise ValueError(f"Role '{role_name}' not found in view mapping.")
            controller = controller_class(self.session, self.authenticated_user, self)
            return view_class(self.main_window, controller)  # Retourne une nouvelle instance de la vue
        except Exception as e:
            raise ValueError(f"Failed to get view for role '{role_name}': {str(e)}")


    def login(self, username, employee_number, password):
        """login user with his employee number, username and password"""

        try:
            user = self.session.query(User).filter_by(username=username, employee_number=employee_number).one()
            if user and user.check_password(password):
                # print(f"Login successful. User role: {user.role.name}")
                self.authenticated_user = user
                return user
        except Exception as e:
            raise ValueError(f"An error occurred during login: {str(e)}")


    def show_frame(self, user):
        """Select a fram associate to the role"""

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
        """Return to the login view"""
        
        if self.authenticated_user:
            self.authenticated_user = None
        self.login_view = LoginWidget(self.main_window, self)
        self.main_window.setCentralWidget(self.login_view)
