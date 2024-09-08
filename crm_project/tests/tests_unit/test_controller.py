from controllers import *
from controllers.authentication_controller import *
from models import *
from tests.tests_unit.base_test_class import *

class TestLoginController(BaseTest):
    def setUp(self):
        super().setUp()
        self.controller = AuthenticationController(self.session, self.root)



    def test_login_success(self):
        # Test d'une connexion réussie avec les bonnes informations
        self.controller.create_user(**self.user_data)
        user = self.controller.login("johndoe", 234, "securepassword")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.employee_number, 234)
        self.assertTrue(user.check_password("securepassword"))

    def test_login_wrong_password(self):
        # Test d'une connexion échouée avec un mauvais mot de passe
        self.controller.create_user(**self.user_data)
        user = self.controller.login("johndoe", 234, "wrongpassword")
        self.assertIsNone(user)

    def test_login_wrong_username(self):
        # Test d'une connexion échouée avec un mauvais nom d'utilisateur
        user = self.controller.login("wrongusername", 234, "securepassword")
        self.assertIsNone(user)

    def test_login_non_existent_user(self):
        # Test d'une connexion échouée avec un utilisateur non existant
        user = self.controller.login("nonexistent", 999, "doesntmatter")
        self.assertIsNone(user)


class TestCommercialController(BaseTest):
    """With permissions"""

    def setUp(self):
        super().setUp()
        self.login_controller = AuthenticationController(self.session, self.root)
        self.commercial_role = self.session.query(Role).filter_by(name=RoleName.COMMERCIAL.value).first()
        self.user = self.login_controller.create_user(role=self.commercial_role, **self.user_data)
        self.controller = CommercialController(self.session, self.user, self.login_controller)   

    def test_create_customer(self):
        
        new_customer =  self.controller.create_customer(**self.customer_data)
        self.assertIsNotNone(new_customer)
        self.assertEqual(new_customer.first_name, self.customer_data['first_name'])
        self.assertEqual(new_customer.last_name, self.customer_data['last_name'])
        self.assertEqual(new_customer.email,self.customer_data['email'])
        self.assertEqual(new_customer.company_name, self.customer_data['company_name'])
        self.assertEqual(new_customer.commercial_contact_id, self.user.id)
        print(f"commercial : {self.user}")
        print(f"commercial role : {self.user.role.name}")

    def test_update_customer(self):
        new_customer =  self.controller.create_customer(**self.customer_data)
        customer_id = new_customer.id
        updated_data =  {
            'first_name': 'Jeanne',
            'email': 'jean.update@contact.com',
            'company_name': 'Update event corp'
        }
        updated_customer = self.controller.update_customer(customer_id, **updated_data)

        self.assertIsNotNone(updated_customer)
        self.assertEqual(updated_customer.first_name, updated_data['first_name'])
        self.assertEqual(updated_customer.email, updated_data['email'])
        self.assertEqual(updated_customer.company_name, updated_data['company_name'])


class TestCommercialPermissionController(BaseTest):
    """Without permissions"""

    def setUp(self):
        super().setUp()
        self.login_controller = AuthenticationController(self.session, self.root)
        self.gestion_role = self.session.query(Role).filter_by(name=RoleName.MANAGEMENT.value).first()
        self.user = self.login_controller.create_user(role=self.gestion_role, **self.user_data)
        self.controller = CommercialController(self.session, self.user, self.login_controller)


    def test_create_customer_with_not_permission(self):
        with self.assertRaises(PermissionError):
            self.controller.create_customer(**self.customer_data)


class TestManagementController(BaseTest):
    """with permission"""

    def setUp(self):
        super().setUp()
        self.login_controller = AuthenticationController(self.session, self.root)
        self.admin = self.session.query(Role).filter_by(name=RoleName.ADMIN.value).first()
        self.user = self.login_controller.create_user(role=self.admin, **self.user_data)
        self.controller = CommercialController(self.session, self.user, self.login_controller)
        self.customer = self.controller.create_customer(**self.customer_data)
        self.management_controller = ManagementController(self.session, self.user, self.login_controller)


    def test_create_contract(self):
        new_contract = self.management_controller.create_contract(self.customer.id, **self.contract_data)
        self.assertIsNotNone(new_contract)
        #print(new_contract.to_dict())

    def test_update_contract(self):
        new_contract = self.management_controller.create_contract(self.customer.id, **self.contract_data)
        self.assertIsNotNone(new_contract)
        updated_data = {
            'remaining_amount': 200
        }
        updated_contract = self.controller.update_contract(self.customer.id, new_contract.id, **updated_data)
        self.assertEqual(updated_data['remaining_amount'], 200)




