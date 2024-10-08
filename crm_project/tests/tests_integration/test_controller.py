from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *
from crm_project.tests.tests_integration.base_integration_test import *
from PySide6.QtWidgets import QApplication


class TestCommercialController(BaseIntegrationTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        session = cls.Session()
        cls.create_users(cls, session)
        session.close()

    def setUp(self):
        super().setUp()
        self.commercial_user = self.session.query(User).filter_by(username='commercial').one()
        self.support_user = self.session.query(User).filter_by(username='support').one()
        self.management_user = self.session.query(User).filter_by(username='management').one()

        self.commercial_controller = CommercialController(self.session, Mock(), Mock())

        self.updated_data = {
            'name': 'Karl',
            'email': 'karl@email.com',
            'company_name': 'lets Go'
        }
        self.invalid_customer_data = {
            'name': self.customer_data['name'],
            'email': None,
            'phone_number': self.customer_data['phone_number'],
            'company_name': None, 
        }
        self.invalid_event_data = {
            'name': 'Mariage',
            'start_date': None,
            'end_date': datetime.now() + timedelta(days=1),
            'location': None,
            'attendees': 100,
            'comment': 'Cérémonie dans un grand hall',
            'contract_id': None
        }

    def tearDown(self):
        super().tearDown()


    def test_create_customer(self):
        # Test la création d'un customer avec permission

        self.commercial_controller.authenticated_user = self.commercial_user
        new_customer = self.commercial_controller.create_customer(**self.customer_data)
        self.assertIsNotNone(new_customer)
        self.assertEqual(new_customer.name, self.customer_data['name'])
        self.assertEqual(new_customer.email, self.customer_data['email'])
        self.assertEqual(new_customer.phone_number, self.customer_data['phone_number'])
        self.assertEqual(new_customer.company_name, self.customer_data['company_name'])
    
    def test_except_create_customer(self):
        # Test bloc except avec des information invalid

        self.commercial_controller.authenticated_user = self.commercial_user
        with self.assertRaises(ValueError) as context:
            self.commercial_controller.create_customer(**self.invalid_customer_data)
        self.assertIn('An error occurred while creating the customer', str(context.exception))
        

    def test_permission_create_customer(self):
        # Test la création d'un customer sans permission

        self.commercial_controller.authenticated_user = self.support_user
        with self.assertRaises(PermissionError):
            new_customer = self.commercial_controller.create_customer(**self.customer_data)
            self.assertIsNone(new_customer)

    def test_update_customer(self):
        # Test la mise à jour des données d'un customer

        self.commercial_controller.authenticated_user = self.commercial_user
        new_customer = self.commercial_controller.create_customer(**self.customer_data)
        self.assertIsNotNone(new_customer)

        customer_id = new_customer.id
        updated_customer = self.commercial_controller.update_customer(customer_id, **self.updated_data)
        self.assertIsNotNone(updated_customer)
        self.assertEqual(updated_customer.name, self.updated_data['name'])
        self.assertEqual(updated_customer.email, self.updated_data['email'])
        self.assertEqual(updated_customer.company_name, self.updated_data['company_name'])
        

    def test_except_update_customer(self):
        # Test le bloc except avec des données invalides

        self.commercial_controller.authenticated_user = self.commercial_user
        new_customer = self.commercial_controller.create_customer(**self.customer_data)
        self.assertIsNotNone(new_customer)
        with  self.assertRaises(ValueError) as context:
            self.commercial_controller.update_customer(new_customer.id, **self.invalid_customer_data)
        self.assertIn('An error occurred while updating customer', str(context.exception))


    def test_permission_update_customer(self):
        # Test la mise a jour customer sans permission

        # Utilise d'abord le commercial user pour créer le customer
        self.commercial_controller.authenticated_user = self.commercial_user
        new_customer = self.commercial_controller.create_customer(**self.customer_data)

        # Passe ensuite sur le support user pour levé la permission
        self.commercial_controller.authenticated_user = self.support_user
        with self.assertRaises(PermissionError):
            self.commercial_controller.update_customer(new_customer.id, **self.updated_data)

    def test_create_event(self):
        # Test la création d'un événement

        self.commercial_controller.authenticated_user = self.commercial_user
        new_event = self.commercial_controller.create_event(**self.event_data)
        self.assertIsNotNone(new_event)

    def test_except_create_event(self):
        # Test le bloc except avec des données invalid 

        self.commercial_controller.authenticated_user = self.commercial_user
        with self.assertRaises(ValueError):
            self.commercial_controller.create_event(**self.invalid_event_data)

    
    def test_permission_create_event(self):
        # Test la création d'un event sans la permission

        self.commercial_controller.authenticated_user = self.support_user
        with self.assertRaises(PermissionError):
            new_event = self.commercial_controller.create_event(**self.event_data)
            self.assertIsNone(new_event)

    def test_update_event(self):
        self.commercial_controller.authenticated_user = self.commercial_user
        new_event = self.commercial_controller.create_event(**self.event_data)
        self.assertIsNotNone(new_event)
        updated_data = {
            'name': 'Dj',
            'attendees': 70,
            'support_contact_id': self.support_user.id
        }
        self.commercial_controller.authenticated_user = self.management_user
        updated_event = self.commercial_controller.update_event(new_event.id, **updated_data)
        self.assertIsNotNone(updated_event)

        with self.assertRaises(ValueError) as context:
            self.commercial_controller.update_event(event_id=999, **updated_data)
        self.assertIn("An error occurred while updating event:", str(context.exception))


    def test_event_filter(self):
        self.commercial_controller.authenticated_user = self.commercial_user
        new_event = self.commercial_controller.create_event(**self.event_data)
        self.assertIsNotNone(new_event)
        filter_data = {
            'only': False,  # Pour SUPPORT, on filtre par support_contact_id
            'contract_id': 'C1234',
            'location': 'Paris'
        }
        self.commercial_controller.authenticated_user = self.management_user
        filter_events = self.commercial_controller.event_filter(**filter_data)
        self.assertIsNotNone(filter_events)
        self.assertEqual(len(filter_events), 1)  # Vérifie qu'il y a bien 1 événement retourné
        self.assertEqual(filter_events[0].location, 'Paris')

    def test_init_controllers(self):
        main_controller = MainController(self.session, self.commercial_user)
        suppport_controller = SupportController(self.session, self.commercial_user, AuthenticationController)
        self.assertIsNotNone(main_controller)
        self.assertIsNotNone(suppport_controller)


    def test_contract_filter(self):
        # Test le filtre de contrat

        self.commercial_controller.authenticated_user = self.commercial_user
        new_customer = self.commercial_controller.create_customer(**self.customer_data)
        contract = Contract(customer_id=new_customer.id, commercial_contact_id=self.commercial_user.id, **self.contract_data)
        self.session.add(contract)
        self.session.commit()
        self.assertIsNotNone(contract)
        filter_data = {
            'status': False,
            'paid': None,  
            'customer_id': 'All Customers',  # Tous les clients
            'amount_due_min': 0,
            'amount_due_max': 5000,
            'creation_date_after': datetime.now() + timedelta(days=-1),
            'creation_date_before': datetime.now() + timedelta(days=+1)
        }
        contracts = self.commercial_controller.contract_filter(**filter_data)
        self.assertEqual(len(contracts), 1)

        # Test sans permission 
        self.commercial_controller.authenticated_user = self.support_user
        with self.assertRaises(PermissionError):
            self.commercial_controller.contract_filter(**filter_data)

    def test_change_username(self):
        self.commercial_controller.authenticated_user = self.commercial_user
        user = self.commercial_controller.change_user_username('commercial')
        self.assertEqual(user.username, 'commercial')

        with self.assertRaises(ValueError) as context:
            self.commercial_controller.change_user_username('ERROR ERROR')
        self.assertIn("Invalid username format", str(context.exception))

    def test_change_password(self):
        self.commercial_controller.authenticated_user = self.commercial_user
        old_password = 'securepassword'
        new_password = 'password'
        result = self.commercial_controller.change_user_password(old_password, new_password)
        self.assertTrue(result)


class TestManagementController(BaseIntegrationTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        session = cls.Session()
        cls.create_users(cls, session)
        session.close()

    def setUp(self):
        super().setUp()
        self.commercial_user = self.session.query(User).filter_by(username='commercial').first()
        self.support_user = self.session.query(User).filter_by(username='support').first()
        self.management_user = self.session.query(User).filter_by(username='management').first()

        self.management_controller = ManagementController(self.session, Mock(), Mock())
        self.customer = Customer(commercial_contact_id=self.commercial_user.id, **self.customer_data)
        self.session.add(self.customer)
        self.session.commit()
        self.user_data = {
            'first_name' : 'user',
            'last_name': 'test',
            'employee_number': '000',
            'password': 'passpass',
            'email': 'test@email.com',
            'role': 'USER',
        }
        self.user_invalid_data = {
            'first_name' : 'user',
            'last_name': 'test',
            'employee_number': 'abc', # field error
            'password': '000',
            'role': 'USER',
        }

        self.contract_data_2 = {
            'amount_due': 1500,
            'remaining_amount': 1500,
            'status': False,
        }

    def test_create_user(self):
        # Test la création d'un employé par un employé du pole management

        self.management_controller.authenticated_user = self.management_user
        new_user = self.management_controller.create_user(**self.user_data)
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.first_name, self.user_data['first_name'])
        self.assertEqual(new_user.username, "user.test")
        self.assertEqual(new_user.role.name.value, self.user_data['role'])

    def test_validate_field_create_user(self):
        # Test les validation de champ avant la créationd d'un employé

        self.management_controller.authenticated_user = self.management_user
        with self.assertRaises(ValueError) as context:
            other_user = self.management_controller.create_user(**self.user_invalid_data)
            self.assertIsNone(other_user)

    def test_except_create_user(self):
        # Test le bloc except de create_user

        self.management_controller.authenticated_user = self.management_user
        self.user_invalid_data['employee_number'] = 123
        self.user_invalid_data['email'] = 'test@email.com' # même email que new_user
        with self.assertRaises(ValueError) as context:
            other_user = self.management_controller.create_user(**self.user_invalid_data)
            self.assertIsNone(other_user)
        self.assertEqual(str(context.exception), "L'utilisateur avec cet email ou ce nom d'utilisateur existe déjà.")
        
    def test_permission_create_user(self):
        self.management_controller.authenticated_user = self.commercial_user
        with self.assertRaises(PermissionError):
            other_user = self.management_controller.create_user(**self.user_data)
            self.assertIsNone(other_user)

    def test_update_user(self):
        self.management_controller.authenticated_user = self.management_user
        updated_data = {
            'username': 'username',
            'email': 'email@email.com',
            'role_id': 2   # Commercial
        }
        
        updated_user = self.management_controller.update_user(self.support_user.id, **updated_data)
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.username, updated_data['username'])
        self.assertEqual(updated_user.role.name.value, "COMMERCIAL")
        self.assertEqual(updated_user.email, updated_data['email'])

    def test_invalid_update_user(self):
        self.management_controller.authenticated_user  = self.management_user
        updated_data = {
            'username': 124
        }
        with self.assertRaises(ValueError):
            invalid_updated_user = self.management_controller.update_user(self.support_user.id, **updated_data)
            self.assertIsNone(invalid_updated_user)

    def test_permission_update_user(self):
        self.management_controller.authenticated_user = self.commercial_user
        updated_data = {
            'username': 'username',
            'email': 'email@email.com',
            'role_id': 2   # Commercial
        }
        with self.assertRaises(PermissionError):
            other_user = self.management_controller.update_user(self.support_user.id, **updated_data)
            self.assertIsNone(other_user)
            
    def test_create_contract(self):
        self.management_controller.authenticated_user = self.management_user
        new_contract = self.management_controller.create_contract(self.customer.id, **self.contract_data_2)
        self.assertIsNotNone(new_contract)
        self.assertEqual(new_contract.customer_id, self.customer.id)
        self.assertEqual(new_contract.customer.commercial_contact_id, self.customer.commercial_contact_id)
    
    def test_invalid_contract(self):
        self.management_controller.authenticated_user = self.management_user
        customer_id = 9876 # 
        with self.assertRaises(ValueError) as context:
            new_contract = self.management_controller.create_contract(customer_id, **self.contract_data_2)
            self.assertIsNone(new_contract)
        self.assertIn("Customer with id", str(context.exception))

    def test_update_contract(self):
        self.management_controller.authenticated_user = self.management_user
        new_contract = self.management_controller.create_contract(self.customer.id, **self.contract_data_2)
        self.assertIsNotNone(new_contract)
        updated_data = {
            'amount_due': 4000,
            'remaining_amount' : 0,
            'status': True
        }
        updated_contract = self.management_controller.update_contract(new_contract.id, **updated_data)
        self.assertIsNotNone(updated_contract)

        with self.assertRaises(ValueError) as context:
            self.management_controller.update_contract(contract_id="F4567", **updated_data)
        self.assertIn("An error occurred while updating contract:", str(context.exception))

    def test_get_user_list(self):
        # test la récupération des user par les manageurs

        self.management_controller.authenticated_user = self.management_user
        user_list = self.management_controller.get_user_list()
        self.assertIsNotNone(user_list)
        self.assertTrue(len(user_list) > 0)
        self.assertTrue(isinstance(user_list[0], dict))

    def test_get_user_list_with_sqlalchemy_error(self):
        # Simuler une exception SQLAlchemy lors de la requête

        with patch('sqlalchemy.orm.query.Query.all', side_effect=SQLAlchemyError("DB error")):
            user_list = self.management_controller.get_user_list()
        self.assertIsNone(user_list)

    def test_get_user_without_auth_user(self):

        self.management_controller.authenticated_user = self.management_user
        user_list_without = self.management_controller.get_users_without_authenticated_user()
        self.assertIsNotNone(user_list_without)
        self.assertTrue(len(user_list_without) > 0)

    def test_get_user_withou_with_sqlalchemy_error(self):
        # Simuler une exception SQLAlchemy lors de la requête 

        with patch('sqlalchemy.orm.query.Query.all', side_effect=SQLAlchemyError("DB error")):
            user_list = self.management_controller.get_users_without_authenticated_user()
        self.assertIsNone(user_list)
    
    def test_delete_user(self):
        # Vérifie le bloc Try/Except de delete user

        user_data = {
            'first_name' : 'userr',
            'last_name': 'testt',
            'employee_number': '000',
            'password': 'passpass',
            'email': 'testt@email.com',
            'role': 'USER',

        }
        self.management_controller.authenticated_user = self.management_user
        delete_user = self.management_controller.create_user(**user_data)
        message = self.management_controller.delete_user(delete_user.id)
        self.assertEqual(message, f"User {delete_user.username} successfully deleted."  )
        deleted_user = self.session.query(User).filter_by(id=delete_user.id).first()
        self.assertIsNone(deleted_user)

        with self.assertRaises(ValueError)as context:
            self.management_controller.delete_user(9999)
        self.assertIn(f"User with ID 9999 not found.", str(context.exception))

        with patch.object(self.session, 'delete', side_effect=SQLAlchemyError("DB error")):
            with self.assertRaises(ValueError) as context:
                self.management_controller.delete_user(delete_user.id)
        self.assertIn("An error occurred while deleting the user", str(context.exception))


class TestLoginController(BaseIntegrationTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        session = cls.Session()
        cls.create_users(cls, session)
        session.close()
        cls.app = QApplication([])

    def setUp(self):
        super().setUp()
        self.commercial_user = self.session.query(User).filter_by(username='commercial').one()
        self.support_user = self.session.query(User).filter_by(username='support').one()
        self.management_user = self.session.query(User).filter_by(username='management').one()
        self.main_window = MainWindow()
        self.controller = AuthenticationController(self.session,self.main_window_mock)

    def test_login(self):
        user = self.controller.login('commercial', 450, 'securepassword')
        self.assertEqual(self.controller.authenticated_user, user)

    

    def test_login_raises_exception(self):
        
        with self.assertRaises(ValueError) as context:
            user = self.controller.login('commerciall', 450, 'securepassword')
        self.assertIn("An error occurred during login: ", str(context.exception))


    def test_get_view_for_commercial(self):
        # Test le mapping de la vue avec son controller

        self.controller.authenticated_user = self.commercial_user
        view = self.controller.get_view_for_role('COMMERCIAL')

        self.assertIsInstance(view, CommercialView)
        self.assertIsInstance(view.controller, CommercialController)

        # check session & Oauth user
        self.assertEqual(view.controller.session, self.session)
        self.assertEqual(view.controller.authenticated_user, self.commercial_user)

    def test_except_view_role(self):
        # Test l'exception en cas de role invalid 

        self.controller.authenticated_user = self.commercial_user
        with self.assertRaises(ValueError) as context:
            self.controller.get_view_for_role('INVALID_ROLE')
        self.assertIn("Role 'INVALID_ROLE' not found", str(context.exception))


    def test_show_frame_for_commercial(self):
        # test l'affichage de la bonne vue pour le bon role

        self.controller.authenticated_user = self.commercial_user
        result = self.controller.show_frame(self.commercial_user)

        self.assertTrue(result)
        central_widget = self.main_window.centralWidget()
        self.assertIsNotNone(central_widget)

    def test_show_login_view(self):
        # Appeler show_login_view
        self.controller.show_login_view()

        # Vérifier que login_view a été défini
        self.assertIsNotNone(self.controller.login_view)

        # Vérifier que le widget central de la fenêtre principale est maintenant LoginWidget
        central_widget = self.main_window.centralWidget()
