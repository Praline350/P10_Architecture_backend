from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *
from crm_project.tests.tests_integration.base_integration_test import *


class TestCommercialController(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.create_users()
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


class TestManagementController(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        

        