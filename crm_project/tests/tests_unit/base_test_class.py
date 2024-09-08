import unittest
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.config import Base
from project.settings import initialize_roles_and_permissions
from controllers import *
from controllers.authentication_controller import *
from models import *


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Créer une base de données SQLite en mémoire pour les tests
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        
        # Initialiser les rôles et permissions avec la session de test
        session = cls.Session()
        initialize_roles_and_permissions(session=session)  # Passer la session de test
        session.commit()  # S'assurer que les rôles et permissions sont bien enregistrés
        session.close()


    def setUp(self):
        # Créer une nouvelle session pour chaque test
        self.session = self.Session()
        # Mock l'interface 
        self.root = Mock()
        self.user_data = {
            'first_name':"John",
            'last_name':"Doe",
            'employee_number':"234",
            'email':"john.doe@example.com",
            'username':"johndoe",
            'password':"securepassword"
        }
        self.customer_data = {
            'name': 'Jean Dupont',
            'email': 'jean@contact.com',
            'company_name': 'event corp'
        }
        self.contract_data = {
            'amount_due': 1500,
            'remaining_amount': 1500,
            'status': False,
        }

    def tearDown(self):
        # Annuler les changements après chaque test
        self.session.rollback()   
        # Suppression des données 
        self.session.query(User).delete()
        self.session.query(Customer).delete()
        self.session.query(Contract).delete()
        self.session.query(Event).delete()
        self.session.commit()
        self.session.close()


    @classmethod
    def tearDownClass(cls):
        # Supprimer les tables après tous les tests
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

