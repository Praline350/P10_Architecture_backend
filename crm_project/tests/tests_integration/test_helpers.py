from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *
from crm_project.tests.tests_integration.base_integration_test import *
from crm_project.helpers.get_data import *


class TestHelpers(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.login_controller = AuthenticationController(self.session, self.root)
        self.commercial_role = self.session.query(Role).filter_by(name=RoleName.COMMERCIAL.value).first()
        self.management_role = self.session.query(Role).filter_by(name=RoleName.MANAGEMENT.value).first()
        self.user_commercial = self.login_controller.create_user(role=self.commercial_role, **self.user_data)
        self.user_management = self.login_controller.create_user(role=self.management_role, **self.user_data2)
        self.controller = CommercialController(self.session, self.user_commercial, self.login_controller)   
        self.new_customer =  self.controller.create_customer(**self.customer_data)


    def test_get_customer_by_commercial(self):
        customers = get_customers_commercial(self.user_commercial, self.session)
        self.assertIsNotNone(customers)
        self.assertEqual(customers[0]['first_name'], self.customer_data['first_name'])


    def test_get_customers_list(self):
        customers = get_customers_list(self.session)
        self.assertIsNotNone(customers)
        self.assertEqual(customers[0]['first_name'], self.customer_data['first_name'])

    def test_get_roles_list(self):
        roles = get_roles_list()
        self.assertEqual(roles[0], 'ADMIN')
        self.assertEqual(roles[1], 'USER')
        self.assertEqual(roles[2], 'COMMERCIAL')
        self.assertEqual(roles[3], 'SUPPORT')
        self.assertEqual(roles[4], 'MANAGEMENT')

    def test_get_contract_commercial(self):
        contracts = get_contract_commercial(self.user_commercial, self.session)
        print(contracts)



