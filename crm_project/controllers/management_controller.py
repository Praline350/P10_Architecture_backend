from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from crm_project.models import *
from crm_project.project.permissions import *
from crm_project.controllers.main_controller import MainController


@decorate_all_methods(is_authenticated_user)
class ManagementController(MainController):
    def __init__(self, session, authenticated_user, login_controller):
        self.session = session
        self.authenticated_user = authenticated_user
        self.login_controller = login_controller

    @require_permission("create_contract")
    def create_contract(self, customer_id, **contract_data):
        """Create a new Contract associate to customer ID with contract data"""
        try:
            customer = self.session.query(Customer).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer with id {customer_id} not found.")
            commercial_contact_id = customer.commercial_contact_id
            new_contract = Contract(
                amount_due=contract_data["amount_due"],
                remaining_amount=contract_data["remaining_amount"],
                customer_id=customer_id,
                commercial_contact_id=commercial_contact_id,
            )
            self.session.add(new_contract)
            self.session.commit()
            return new_contract
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"An error occurred while create the contract: {str(e)}")

    @require_permission("create_user")
    def create_user(self, **user_data):
        """Create a new employee with user data"""

        try:
            username = f"{user_data['first_name']}.{user_data['last_name']}"
            role = self.session.query(Role).filter_by(name=user_data["role"]).one()
            if role and username:
                new_user = User(
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    employee_number=int(user_data["employee_number"]),
                    email=user_data["email"],
                    username=username,
                    role=role,
                )
                new_user.set_password(
                    user_data["password"]
                )  # Le hachage et le salage sont gérés ici

                self.session.add(new_user)
                self.session.commit()
                return new_user
            else:
                return None
        except IntegrityError:
            self.session.rollback()
            raise ValueError(
                "L'utilisateur avec cet email ou ce nom d'utilisateur existe déjà."
            )

    @require_permission("update_user")
    def update_user(self, user_id, **user_data):
        """Update an Employee with his ID and user data"""

        try:
            print(f"ID de l'utilisateur à mettre à jour: {user_id}")
            user = self.session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"user {user_id} not found")
            print(f"Utilisateur trouvé: {user.first_name} {user.last_name}")

            for key, value in user_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                    print(f"Champ mis à jour {key} : {value}")

            self.session.commit()
            print("Mise à jour de l'utilisateur réussie")
            return user
        except Exception:
            self.session.rollback()
            raise ValueError("error")

    @require_permission("delete_user")
    def delete_user(self, user_id):
        """Delete an employee with his ID"""

        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            else:
                self.session.delete(user)
                self.session.commit()
                return f"User {user.username} successfully deleted."
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"An error occurred while deleting the user: {str(e)}")

    @require_permission("update_user")
    def get_user_list(self):
        """Return a list of all users"""

        try:
            users = self.session.query(User).all()
            user_list = [user.to_dict() for user in users]
            return user_list
        except SQLAlchemyError as e:
            self.session.rollback()
            # print(f"Error during get users: {e}")
            return None

    @require_permission("update_user")
    def get_users_without_authenticated_user(self):
        """Return list of user without current authenticated user"""

        try:
            users = (
                self.session.query(User)
                .filter(User.id != self.authenticated_user.id)
                .all()
            )
            return users
        except SQLAlchemyError as e:
            self.session.rollback()
            # print(f"Error during get users: {e}")
            return None
