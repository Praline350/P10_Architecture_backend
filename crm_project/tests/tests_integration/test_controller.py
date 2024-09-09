from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *
from crm_project.tests.tests_integration.base_integration_test import *

class TestLoginController(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.controller = AuthenticationController(self.session, self.root)

        # Simuler une vue et un contrôleur en tant que classes
        self.view_class_mock = Mock()  
        self.controller_class_mock = Mock() 
        # Simuler l'instance du contrôleur et la vue 
        self.controller_instance_mock = Mock()
        self.controller_class_mock.return_value = self.controller_instance_mock
        self.view_instance_mock = Mock()
        self.view_class_mock.return_value = self.view_instance_mock

        self.controller.view_mapping = {
            'COMMERCIAL': (self.view_class_mock, self.controller_class_mock),
            'ADMIN': (self.view_class_mock, self.controller_class_mock)
        }



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

    def test_get_view_for_valid_role(self):
        # Appeler la méthode avec un rôle valide
        view_instance = self.controller.get_view_for_role('ADMIN')
        self.controller_class_mock.assert_called_once_with(self.controller.session, self.controller.authenticated_user, self.controller)
        self.view_class_mock.assert_called_once_with(self.controller.main_window, self.controller_instance_mock)

        # Vérifier que la méthode retourne bien l'instance de la vue
        self.assertEqual(view_instance, self.view_instance_mock)

    def test_get_view_for_invalid_role(self):
        # Test pour un rôle invalide
        view_instance = self.controller.get_view_for_role('INVALID_ROLE')
        self.controller_class_mock.assert_not_called()
        self.view_class_mock.assert_not_called()
        self.assertIsNone(view_instance)
    
    def test_show_frame_with_valid_role(self):
        # Appeler show_frame avec un utilisateur ayant un rôle valide
        self.controller.login_view = Mock()
        self.frame_mock = Mock()
        self.controller.get_view_for_role = Mock(return_value=self.frame_mock)
        result = self.controller.show_frame(self.user_mock)
        self.controller.get_view_for_role.assert_called_once_with('ADMIN')
        self.assertEqual(result, True)


class TestCommercialController(BaseIntegrationTest):
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


class TestCommercialPermissionController(BaseIntegrationTest):
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


class TestManagementController(BaseIntegrationTest):
    """with permission"""

    def setUp(self):
        super().setUp()
        self.login_controller = AuthenticationController(self.session, self.root)
        self.admin_role = self.session.query(Role).filter_by(name=RoleName.ADMIN.value).first()
        self.user = self.login_controller.create_user(role=self.admin_role, **self.user_data)
        self.controller = CommercialController(self.session, self.user, self.login_controller)
        self.customer = self.controller.create_customer(**self.customer_data)
        self.management_controller = ManagementController(self.session, self.user, self.login_controller)

        self.updated_data = {
            'username': 'Charly09',
            'email': 'charly@email.com',
            'employee_number': '1',
        }


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

    def test_create_employee(self):
        # test la creation d'employees
        user = self.management_controller.create_user(**self.user_data3)
        self.assertEqual(user.username, f"{self.user_data3['first_name']}.{self.user_data3['last_name']}")
        self.assertEqual(user.first_name, self.user_data3['first_name'])
        self.assertEqual(user.last_name, self.user_data3['last_name'])
        self.assertEqual(user.email, self.user_data3['email'])
        self.assertEqual(user.role.name.value, self.user_data3['role'])
        self.assertTrue(user.check_password(self.user_data3['password']))
        user_in_db = self.session.query(User).filter_by(email=self.user_data3['email']).one()
        self.assertEqual(user_in_db.username, user.username)

    def test_create_user_with_duplicate(self):
        # Ajouter un utilisateur existant avec le même email ou nom d'utilisateur
        self.management_controller.create_user( **self.user_data3)
        with self.assertRaises(ValueError) as context:
            self.management_controller.create_user(**self.user_data3)
        self.assertEqual(str(context.exception), "L'utilisateur avec cet email ou ce nom d'utilisateur existe déjà.")

    def test_update_employee(self):
        user = self.management_controller.create_user(**self.user_data3)
        self.assertEqual(user.username, f"{self.user_data3['first_name']}.{self.user_data3['last_name']}")

        user_updated = self.management_controller.update_user(user.id, **self.updated_data)
        self.assertEqual(user_updated.username, self.updated_data['username'])
        self.assertEqual(user.email, self.updated_data['email'])

    def test_update_employee_error(self):
        unexistent_user_id = 57
        user = self.management_controller.create_user(**self.user_data3)
        self.assertEqual(user.username, f"{self.user_data3['first_name']}.{self.user_data3['last_name']}")
        fake_data = {
            'username': None,
            'email': 'charly@email',
            'employee_number': 'HEHE',

        }
        with self.assertRaises(ValueError) as context:
            self.management_controller.update_user(unexistent_user_id, **self.updated_data)
        self.assertIn(f"user {unexistent_user_id} not found", str(context.exception))
        with self.assertRaises(ValueError) as context:
            self.management_controller.update_user(user.id, **fake_data)
        self.assertIn("Invalid username", str(context.exception))
        fake_data['username'] = 'charly09'
        with self.assertRaises(ValueError) as context:
            self.management_controller.update_user(user.id, **fake_data)
        self.assertIn("Invalid employee number", str(context.exception))









