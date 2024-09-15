import unittest
from unittest.mock import Mock
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from crm_project.project.config import Base
from crm_project.project.settings import initialize_roles_and_permissions
from crm_project.controllers import *
from crm_project.controllers.authentication_controller import *
from crm_project.models import *
from crm_project.models.user import role_permissions, BaseModelMixin



class BaseUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Créer une base de données SQLite en mémoire pour les tests
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        # Créer une nouvelle session pour chaque test
        self.session = self.Session()
 
    def tearDown(self):
        # Annuler les changements après chaque test   
        self.session.query(role_permissions).delete()
        self.session.query(User).delete()
        self.session.query(Role).delete()
        self.session.query(Permission).delete()
        self.session.query(Contract).delete()
        self.session.query(Customer).delete()     
        self.session.query(Event).delete()
        self.session.commit()
        self.session.close()


    @classmethod
    def tearDownClass(cls):
        # Supprimer les tables après tous les tests
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()


"""
   : Test pour le BaseModelMixin :
"""

class TestModel(Base, BaseModelMixin):
    __tablename__ = 'test_model'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class TestBaseModelMixin(BaseUnitTest):
    def test_tablename(self):
        # Vérifier que le nom de la table est correctement généré
        self.assertEqual(TestModel.__tablename__, 'test_model')

    def test_to_dict(self):
        # Ajouter une instance de TestModel et la convertir en dictionnaire
        test_model = TestModel(id=1, name="Test Name")
        self.session.add(test_model)
        self.session.commit()

        # Appeler la méthode to_dict
        result_dict = test_model.to_dict()

        # Vérifier que le dictionnaire est correct
        expected_dict = {
            'id': 1,
            'name': "Test Name"
        }
        self.assertEqual(result_dict, expected_dict)
