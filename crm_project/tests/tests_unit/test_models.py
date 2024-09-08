import unittest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

from crm_project.models import *
from crm_project.project.config import Base
from crm_project.tests.tests_unit.base_unit_test import BaseUnitTest


class TestCustomerModel(BaseUnitTest):
    def setUp(self):
        super().setUp()

    def test_customer_creation(self):
        customer = Customer(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            company_name="Doe Corp",
            commercial_contact_id=1
        )
        self.session.add(customer)
        self.session.commit()
        saved_customer = self.session.query(Customer).first()
        self.assertIsNotNone(saved_customer)
        self.assertEqual(saved_customer.first_name, "John")
        self.assertEqual(saved_customer.last_name, "Doe")
        self.assertEqual(saved_customer.email, "john.doe@example.com")
        self.assertEqual(saved_customer.company_name, "Doe Corp")

    def test_customer_creation_date(self):
        # Tester la mise en place automatique des dates de création et de mise à jour
        customer = Customer(
            first_name="Alice",
            last_name="Wonderland",
            email="alice@example.com",
            commercial_contact_id=1)
        self.session.add(customer)
        self.session.commit()

        saved_customer = self.session.query(Customer).first()
        self.assertIsNotNone(saved_customer.creation_date)
        self.assertTrue(isinstance(saved_customer.creation_date, datetime))
        self.assertTrue(isinstance(saved_customer.last_update, datetime))
        self.assertAlmostEqual(saved_customer.creation_date, saved_customer.last_update, delta=timezone.utc)

class TestContractModel(BaseUnitTest):
    def setUp(self):
        super().setUp()
        # Créer un customer pour tester la relation avec Contract
        self.customer = Customer(first_name="John", last_name="Doe", email="john.doe@example.com", commercial_contact_id=1)
        self.session.add(self.customer)
        self.session.commit()

    def test_create_contract(self):
        contract = Contract(
            amount_due=1000,
            remaining_amount=1000,
            commercial_contact_id=1,
            customer=self.customer)
        self.session.add(contract)
        self.session.commit()

        saved_contract = self.session.query(Contract).first()
        self.assertIsNotNone(saved_contract)
        self.assertEqual(saved_contract.amount_due, 1000)
        self.assertEqual(saved_contract.remaining_amount, 1000)
        self.assertEqual(saved_contract.customer_id, self.customer.id)

    def test_contract_creation_date(self):
        # Tester la mise en place automatique des dates de création et de mise à jour
        contract = Contract(
            amount_due=2000,
            remaining_amount=1500,
            commercial_contact_id=1,
            customer=self.customer)
        self.session.add(contract)
        self.session.commit()

        saved_contract = self.session.query(Contract).first()
        self.assertIsNotNone(saved_contract.creation_date)
        self.assertTrue(isinstance(saved_contract.creation_date, datetime))
        self.assertTrue(isinstance(saved_contract.last_update, datetime))


    def test_validate_commercial_contact(self):
        # Vérifier que la méthode validate_commercial_contact lève une exception si le contact n'est pas valide
        contract = Contract(
            amount_due=1000,
            remaining_amount=1000,
            commercial_contact_id=2,
            customer=self.customer)
        self.session.add(contract)
        
        with self.assertRaises(ValueError):
            contract.validate_commercial_contact()


class TestEventModel(BaseUnitTest):
    def setUp(self):
        super().setUp()

        # Créer un client, un contrat, un utilisateur pour les tests
        self.customer = Customer(first_name="John", last_name="Doe", email="john.doe@example.com", commercial_contact_id=1)
        self.session.add(self.customer)
        self.session.commit()

        self.contract = Contract(amount_due=1000, remaining_amount=1000, commercial_contact_id=1, customer=self.customer)
        self.session.add(self.contract)
        self.session.commit()

        self.user = User(first_name="Support", last_name="Contact", email="support@example.com", username="supportuser", employee_number=123, role_id=1)
        self.session.add(self.user)
        self.session.commit()

    def test_create_event(self):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=1)

        event = Event(
            name="Test Event",
            contract=self.contract,
            start_date=start_date,
            end_date=end_date,
            support_contact=self.user,
            location="New York",
            attendees=100,
            comment="Annual Event"
        )
        self.session.add(event)
        self.session.commit()

        saved_event = self.session.query(Event).first()
        self.assertIsNotNone(saved_event)
        self.assertEqual(saved_event.name, "Test Event")
        self.assertEqual(saved_event.location, "New York")
        self.assertEqual(saved_event.attendees, 100)
        self.assertEqual(saved_event.contract_id, self.contract.id)
        self.assertEqual(saved_event.support_contact_id, self.user.id)

class TestUserModel(BaseUnitTest):
    def setUp(self):
        super().setUp()
        # Créer un rôle et des permissions pour les tests
        self.permission1 = Permission(name="view_contracts", description="Can view contracts")
        self.permission2 = Permission(name="edit_contracts", description="Can edit contracts")
        self.session.add_all([self.permission1, self.permission2])
        self.session.commit()

        self.role = Role(name=RoleName.COMMERCIAL, description="Commercial Role")
        if not self.session.query(role_permissions).filter_by(role_id=self.role.id, permission_id=self.permission1.id).count():
            self.role.permissions.append(self.permission1)
        self.session.add(self.role)
        self.session.commit()

        # Créer un utilisateur avec ce rôle
        self.user = User(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@example.com",
            employee_number=123,
            role=self.role
        )
        self.user.set_password("securepassword")
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_user_creation(self):
        saved_user = self.session.query(User).first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.username, "johndoe")
        self.assertEqual(saved_user.email, "johndoe@example.com")
        self.assertTrue(saved_user.check_password("securepassword"))

    def test_user_has_permission(self):
        # Vérifier que l'utilisateur a la permission 'view_contracts'
        self.assertTrue(self.user.has_permission("view_contracts"))
        # Vérifier que l'utilisateur n'a pas la permission 'edit_contracts'
        self.assertFalse(self.user.has_permission("edit_contracts"))


class TestRolePermissionModel(BaseUnitTest):
    def test_create_role_with_permission(self):
        # Créer une permission
        permission = Permission(name="delete_contracts", description="Can delete contracts")
        self.session.add(permission)
        self.session.commit()

        # Créer un rôle avec la permission
        role = Role(name=RoleName.ADMIN, description="Administrator Role")
        role.permissions.append(permission)
        self.session.add(role)
        self.session.commit()

        # Vérifier que le rôle et la permission sont bien créés
        saved_role = self.session.query(Role).first()
        self.assertIsNotNone(saved_role)
        self.assertEqual(saved_role.name, RoleName.ADMIN)

        saved_permission = self.session.query(Permission).first()
        self.assertEqual(saved_permission.name, "delete_contracts")
        self.assertIn(saved_permission, saved_role.permissions)
