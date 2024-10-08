from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *
from crm_project.tests.tests_integration.base_integration_test import *
from crm_project.helpers.get_data import *


class TestHelpers(unittest.TestCase):
    def setUp(self):
        # Créer une base de données en mémoire
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Ajouter des données initiales à la base de données
        self._populate_data()

    def tearDown(self):
        print(f"Test OK: {self.id()}")
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def _populate_data(self):
        # Ajouter des utilisateurs, clients, contrats, etc. pour les tests
        role_admin = Role(id=1, name=RoleName.ADMIN)
        role_commercial = Role(id=2, name=RoleName.COMMERCIAL)
        role_support = Role(id=3, name=RoleName.SUPPORT)
        self.session.add_all([role_admin, role_commercial, role_support])
        self.session.commit()

        self.user_commercial = User(id=1, username="commercial", employee_number=0, role=role_commercial)
        self.user_support = User(id=2, username='support', employee_number=0, role=role_support)
        customer = Customer(id=1, name="John Doe", email="email@email.com", commercial_contact=self.user_commercial)
        self.contract = Contract(customer=customer, amount_due=100, remaining_amount=100, commercial_contact_id=self.user_commercial.id)
        event = Event(name="Mariage", contract=self.contract, start_date=datetime.now(),end_date=datetime.now() + timedelta(days=1), location="Bordeaux", attendees=100, support_contact=self.user_support)
        self.session.add_all([self.user_commercial, customer, self.contract, event])
        self.session.commit()
        self.authenticated_user = self.user_commercial

    def test_get_roles_list(self):
        roles = get_roles_list(self)
        self.assertIsNotNone(roles)
        self.assertIn('COMMERCIAL', roles)

    def test_get_roles_without_admin(self):
        roles = get_roles_without_admin(self)
        self.assertIsNotNone(roles)
        self.assertGreater(len(roles), 0)

    def test_get_customers_commercial(self):
        user = self.session.query(User).filter_by(username="commercial").one()
        self.authenticated_user = user
        customers = get_customers_commercial(self)
        self.assertIsNotNone(customers)
        self.assertGreater(len(customers), 0)

    def test_get_contract_commercial(self):
        user = self.session.query(User).filter_by(username="commercial").one()
        contracts = get_contract_commercial(self, user)
        self.assertIsNotNone(contracts)
        self.assertGreater(len(contracts), 0)

    def test_get_customers_list(self):
        customers = get_customers_list(self)
        self.assertIsNotNone(customers)
        self.assertGreater(len(customers), 0)

    def test_get_events_list(self):
        events = get_events_list(self)
        self.assertIsNotNone(events)
        self.assertGreater(len(events), 0)

    def test_get_users(self):
        users = get_users(self)
        self.assertIsNotNone(users)
        self.assertGreater(len(users), 0)

    def test_get_commercials(self):
        commercials = get_commercials(self)
        self.assertIsNotNone(commercials)
        self.assertGreater(len(commercials), 0)

    def test_get_events_spport_list(self):
        events = get_events_support_list(self, self.user_support.id)
        self.assertIsNotNone(events)
        self.assertGreater(len(events), 0)

    def test_get_contracts_list(self):
        contracts = get_contracts_list(self)
        self.assertIsNotNone(contracts)
        self.assertGreater(len(contracts), 0)

    def test_get_contracts_by_customer(self):
        contracts = get_contract_by_customer(self, 1)
        self.assertIsNotNone(contracts)
        self.assertGreater(len(contracts), 0)

    def test_get_support(self):
        supports = get_support_user(self)
        self.assertIsNotNone(supports)
        self.assertGreater(len(supports), 0)

    def test_get_status_contact(self):
        result =  get_status_contract(self, self.contract.id)
        self.assertEqual(result, False)
