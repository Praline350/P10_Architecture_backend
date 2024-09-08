from controllers import *
from controllers.authentication_controller import *
from models import *
from tests.tests_unit.base_test_class import *
from helpers.get_data import *


class TestHelpers(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_controller = AuthenticationController(self.session, self.root)
        self.commercial_role = self.session.query(Role).filter_by(name=RoleName.COMMERCIAL.value).first()
        self.user = self.login_controller.create_user(role=self.commercial_role, **self.user_data)
        self.controller = CommercialController(self.session, self.user)   
        self.new_customer =  self.controller.create_customer(**self.customer_data)


    def test_get_customer_by_commercial(self):
        customers = get_customers_commercial(self.user, self.session)
        self.assertIsNotNone(customers)
        self.assertEqual(customers[0]['name'], self.customer_data['name'])


    def test_get_customers_list(self):
        customers = get_customers_list(self.session)
        self.assertIsNotNone(customers)
        self.assertEqual(customers[0]['name'], self.customer_data['name'])

