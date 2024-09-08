from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import *

from views import *
from views.admin_view import AdminView
from controllers import *

class AuthenticationController:
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
            else:
                print(f"No frame found for role: {role_name}")


    def show_login_view(self):
        self.authenticated_user = None
        self.login_view = LoginWidget(self.main_window, self)
        self.main_window.setCentralWidget(self.login_view)


    def close(self):
        self.authenticated_user = None
        self.session.close()

    def create_user(self, role=None, **user_data):
        if role is None:
            role = self.session.query(Role).filter_by(name=RoleName.USER.value).first()
        try:
            new_user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                employee_number=user_data['employee_number'],
                email=user_data['email'],
                username=user_data['username'],
                role=role
            )
            new_user.set_password(user_data['password'])  # Le hachage et le salage sont gérés ici

            self.session.add(new_user)
            self.session.commit()
            return new_user  # Retourne l'utilisateur créé

        except IntegrityError:
            self.session.rollback()
            raise ValueError("L'utilisateur avec cet email ou ce nom d'utilisateur existe déjà.")