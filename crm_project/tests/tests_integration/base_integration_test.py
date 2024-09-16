import unittest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from datetime import datetime, timedelta

from crm_project.project.config import Base
from crm_project.project.settings import initialize_roles_and_permissions
from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *


class BaseIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Créer une base de données SQLite en mémoire pour les tests
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        # Créer une sessionmaker avec l'engine comme bind
        session_factory = sessionmaker(bind=cls.engine)

        # Utiliser scoped_session avec la factory
        cls.Session = scoped_session(session_factory)
        
        # Initialiser les rôles et permissions avec la session de test
        session = cls.Session()
        initialize_roles_and_permissions(session=session)  # Passer la session de test
        session.commit()  # S'assurer que les rôles et permissions sont bien enregistrés
        session.close()


    def setUp(self):

        # Récupère la session de classe
        self.session = self.__class__.Session()

        # Mock l'interface 
        self.main_window_mock = Mock()
        self.central_widget_mock = Mock()
        self.main_window_mock.centralWidget.return_value = self.central_widget_mock
        self.root = Mock()
        self.user_mock = Mock()
        self.user_mock.role.name.value = 'ADMIN'
        self.login_view_mock = Mock()

        # Données Statiques
        self.customer_data = {
            'name': 'Jean Bon',
            'email': 'jean@contact.com',
            "phone_number": "068796058",
            'company_name': 'event corp'
        }
        self.contract_data = {
            'id': "C1234",
            'amount_due': 1500,
            'remaining_amount': 1500,
            'status': False,
        }
        self.event_data = {
            'name': 'Mariage',
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=1),
            'location': 'Paris',
            'attendees': 100,
            'comment': 'Cérémonie dans un grand hall',
            'contract_id': self.contract_data['id']
        }

    def tearDown(self):
        # Annuler les changements après chaque test
        self.session.rollback()   
        # # Suppression des données 
        # self.session.query(User).delete()
        self.session.query(Customer).delete()
        self.session.query(Contract).delete()
        self.session.query(Event).delete()
        self.session.commit()
        self.session.close()


    @classmethod
    def tearDownClass(cls):
        # Fermer la session et supprimer les tables après tous les tests
        cls.Session.remove()
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def create_users(cls, session):
        cls.commercial_user = User(
            first_name="John",
            last_name="Doe",
            employee_number=450,
            email="johndoe@email.com",
            username="commercial",
            role_id=2 # Commercial
        )
        cls.commercial_user.set_password("securepassword")
        session.add(cls.commercial_user)

        cls.management_user = User(
            first_name="Alice",
            last_name="Dye",
            employee_number=000,
            email="alice@email.com",
            username="management",
            role_id=5 # Management
        )
        cls.commercial_user.set_password("securepassword")
        session.add(cls.management_user)

        cls.support_user = User(
            first_name="Greg",
            last_name="Dae",
            employee_number=321,
            email="greg@email.com",
            username="support",
            role_id=3 # Support
        )
        cls.commercial_user.set_password("securepassword")
        session.add(cls.support_user)
        session.commit()
