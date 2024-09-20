import pytest
from PySide6.QtWidgets import QApplication, QLabel, QDialog, QComboBox, QLabel, QDialogButtonBox, QMessageBox, QLineEdit, QFormLayout
from PySide6.QtCore import Qt, Signal
from crm_project.views.management_view import ManagementView
from crm_project.controllers.management_controller import ManagementController
from crm_project.views.widget_maker import *
from crm_project.helpers.get_data import *
from unittest.mock import Mock, patch, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crm_project.models import *
from crm_project.project.config import Base
from crm_project.project.settings import initialize_roles_and_permissions


class TestManagementView:
    """Classe de test pour la vue ManagementView."""

    # Fixture pour initialiser une base de données SQLite en mémoire
    @pytest.fixture(scope='class')
    def db_session(self):
        """Initialise une base de données SQLite en mémoire pour les tests."""
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        session = Session()

        # Créer les tables
        Base.metadata.create_all(engine)

        # # Ajouter des données de test (utilisateurs, rôles, etc.)
        # role_commercial = Role(name='COMMERCIAL')
        # # role_support = Role(name='SUPPORT')
        # role_management = Role(name='MANAGEMENT')
        initialize_roles_and_permissions(session=session)
        # session.add_all([role_commercial, role_support])
        user = User(
            first_name='John',
            last_name='Doe',
            email='john@example.com', 
            employee_number=0,
            username='johndoe',
            role_id=5
        )
        session.add(user)
        session.commit()

        yield session

        # Nettoyage après le test
        session.close()

    # Fixture pour initialiser un contrôleur réel avec session
    @pytest.fixture
    def management_controller(self, db_session):
        """Crée une instance réelle du contrôleur avec la session de test."""
        self.user = db_session.query(User).first()
        controller = ManagementController(db_session, self.user, Mock())
        return controller

    # Fixture pour initialiser une vue réelle
    @pytest.fixture
    def management_view(self, qtbot, management_controller):
        """Initialise la vue ManagementView avec un contrôleur réel."""
        view = ManagementView(Mock(), management_controller)
        qtbot.addWidget(view)  # Ajoute la vue à l'environnement de test Qt
        return view

    # Fixture pour initialiser l'application Qt
    @pytest.fixture
    def qtbot(self, qtbot):
        """Fixture pour initialiser QApplication."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return qtbot

    # Test pour vérifier l'initialisation de la vue
    def test_initialization(self, management_view):
        """Teste l'initialisation de ManagementView et vérifie les widgets."""

        # Vérifier si le label de bienvenue est correctement configuré
        welcome_label = management_view.findChild(QLabel, "label_titre")
        assert welcome_label is not None
        assert welcome_label.text() == "Management Dashboard, Welcome John Doe"
        assert welcome_label.alignment() == Qt.AlignCenter

    def test_initialization(self, management_view):
        """Teste l'initialisation de ManagementView et vérifie les widgets."""
        # Vérifier si le label de bienvenue est correctement configuré
        welcome_label = management_view.findChild(QLabel, "label_titre")
        assert welcome_label is not None
        assert welcome_label.text() == "Management Dashboard, Welcome John Doe"
        assert welcome_label.alignment() == Qt.AlignCenter

    def test_buttons_initialization(self, management_view):
        """Teste si les boutons sont bien initialisés avec le texte correct."""
        assert management_view.create_contract_button.text() == "Create Contract"
        assert management_view.update_contract_button.text() == "Update a Contract"
        assert management_view.create_user_button.text() == "Creare New Employee"
        assert management_view.update_user_button.text() == "Update an Employee"
        assert management_view.delete_user_button.text() == "Delete an Employee"
        assert management_view.filter_event_button.text() == "Filter Event" 
    
    def test_create_contract_window_initialization(qtbot, management_view, db_session):
        """Teste si la fenêtre de création de contrat est bien initialisée."""

        # Ajouter des clients dans la base de données
        customer1 = Customer(name='Alice Wonder', email='alice@wonder.com', company_name='Wonder Corp', commercial_contact=management_view.controller.authenticated_user)
        customer2 = Customer(name='Charlie Brown', email='charlie@brown.com', company_name='Brown Co', commercial_contact=management_view.controller.authenticated_user)

        db_session.add(customer1)
        db_session.add(customer2)
        db_session.commit()

        # Appeler la méthode pour ouvrir la fenêtre de création de contrat
        management_view.create_contract_window()

        # Récupérer la fenêtre modale
        dialog = management_view.findChild(QDialog)
        assert dialog is not None, "Le QDialog n'a pas été trouvé."

        # Vérifier l'existence de la combobox pour les clients

        customer_combobox = dialog.findChild(QComboBox, "Customer_combobox")
        assert customer_combobox is not None, "La combobox des clients n'a pas été trouvée."

        # Vérifier qu'il y a bien deux clients dans la combobox
        assert customer_combobox.count() == 2, "Le nombre de clients dans la combobox est incorrect."

        # Vérifier que les clients sont bien dans la combobox
        assert customer_combobox.itemText(0) == "1 - Alice Wonder"
        assert customer_combobox.itemText(1) == "2 - Charlie Brown"

        # Vérifier les informations du client sélectionné
        customer_info_label = dialog.findChild(QLabel, "label_customer_info")
        assert customer_info_label is not None, "Le label d'information du client n'a pas été trouvé."
        
        # Simuler la sélection du premier client dans la combobox
        customer_combobox.setCurrentIndex(0)
        
        # Vérifier les informations du client affichées dans le label
        assert "alice@wonder.com" in customer_info_label.text(), "Les informations du client ne sont pas correctes."

    @patch('crm_project.views.management_view.mk_display_current_item')
    def test_on_customer_selection_changed(self, mock_display, qtbot, management_view):
        """Test pour la méthode on_customer_selection_changed."""
        # Créer un label et une combobox pour le test
        label = QLabel()
        combobox = QComboBox()

        # Simuler l'ajout de clients dans la combobox
        data_dict = {
            1: Mock(email="alice@wonder.com", company_name="Wonder Corp", commercial_contact=Mock(full_name="Bob")),
            2: Mock(email="charlie@brown.com", company_name="Brown Co", commercial_contact=Mock(full_name="David"))
        }

        # Ajouter les IDs des clients comme data dans la combobox
        combobox.addItem("Alice Wonder", 1)
        combobox.addItem("Charlie Brown", 2)

        # Simuler le changement de sélection
        index = 1  # Simuler que l'utilisateur sélectionne "Charlie Brown"
        management_view.on_customer_selection_changed(label, combobox, data_dict, index)

        # Vérifier que les bonnes données ont été extraites
        customer = data_dict[2]
        expected_data = {
            'Email': customer.email,
            'Company': customer.company_name,
            'Commercial Contact': customer.commercial_contact.full_name,
        }

        # Vérifier que mk_display_current_item a été appelé avec les bonnes données
        mock_display.assert_called_once_with(label, expected_data)
        
    def test_create_user_window(self, qtbot, management_view, db_session):
        """Test de la fonctionnalité de création d'utilisateur avec des données réelles."""

        # Appeler la méthode pour ouvrir la fenêtre de création d'utilisateur
        
        management_view.controller.authenticated_user = self.user
        print(self.user.role.name.value)
        management_view.create_user_window()

        # Récupérer la fenêtre modale
        dialog = management_view.findChild(QDialog)
        assert dialog is not None, "Le QDialog n'a pas été trouvé."

        # Récupérer les champs de texte (QLineEdit)
        first_name_field = dialog.findChild(QLineEdit, "first_name")
        last_name_field = dialog.findChild(QLineEdit, "last_name")
        email_field = dialog.findChild(QLineEdit, "email")
        employee_number_field = dialog.findChild(QLineEdit, "employee_number")
        password_field = dialog.findChild(QLineEdit, "password")
        confirm_password_field = dialog.findChild(QLineEdit, "confirm_password")
        roles_combobox = dialog.findChild(QComboBox, "Role_combobox")

        # Vérifier que les champs existent
        assert first_name_field is not None, "Le champ 'First Name' n'a pas été trouvé."
        assert last_name_field is not None, "Le champ 'Last Name' n'a pas été trouvé."
        assert email_field is not None, "Le champ 'Email' n'a pas été trouvé."
        assert employee_number_field is not None, "Le champ 'Employee Number' n'a pas été trouvé."
        assert password_field is not None, "Le champ 'Password' n'a pas été trouvé."
        assert confirm_password_field is not None, "Le champ 'Confirm Password' n'a pas été trouvé."
        assert roles_combobox is not None, "La combobox des rôles n'a pas été trouvée."

        # Simuler la saisie des données
        qtbot.keyClicks(first_name_field, "Mike")
        qtbot.keyClicks(last_name_field, "Doe")
        qtbot.keyClicks(email_field, "Mike.doe@example.com")
        qtbot.keyClicks(employee_number_field, "0")
        qtbot.keyClicks(password_field, "Password1234")
        qtbot.keyClicks(confirm_password_field, "Password1234")

        # Sélectionner un rôle
        roles_combobox.setCurrentIndex(0)

    def test_update_user_window(self, qtbot, management_view, db_session):
        """Test de la fonctionnalité de mise à jour d'un utilisateur."""

        # Ajouter un utilisateur dans la base de données pour le test
        user = User(first_name='alice', last_name='wonder', username='alice', email='alice@example.com', employee_number=0, role_id=5)
        db_session.add(user)
        db_session.commit()
        
        print("Utilisateur ajouté dans la base de données:", user.first_name, user.last_name)

        # Ouvrir la fenêtre de mise à jour d'utilisateur
        management_view.update_user_window()

        # Récupérer la fenêtre de dialogue
        dialog = management_view.findChild(QDialog)
        assert dialog is not None, "La fenêtre de mise à jour n'a pas été trouvée."

        print("Fenêtre de mise à jour ouverte.")

        # Sélectionner un utilisateur dans la combobox
        user_combobox = dialog.findChild(QComboBox)
        assert user_combobox is not None, "La combobox des utilisateurs n'a pas été trouvée."
        print("Combobox utilisateur récupérée.")

        # Vérification de la liste des utilisateurs dans la combobox
        print("Nombre d'utilisateurs dans la combobox:", user_combobox.count())
        print("Valeur actuelle de la combobox:", user_combobox.currentText())

        user_combobox.setCurrentIndex(0)
        print("Sélection de l'utilisateur:", user_combobox.currentText())

        # Récupérer les champs de texte
        first_name_field = dialog.findChild(QLineEdit, "first_name")
        last_name_field = dialog.findChild(QLineEdit, "last_name")
        email_field = dialog.findChild(QLineEdit, "email")
        assert first_name_field is not None, "Le champ 'first_name' n'a pas été trouvé."
        assert last_name_field is not None, "Le champ 'last_name' n'a pas été trouvé."
        assert email_field is not None, "Le champ 'email' n'a pas été trouvé."

        print("Champs récupérés :", first_name_field.text(), last_name_field.text(), email_field.text())

        # Effacer les champs avant de les remplir avec de nouvelles valeurs
        first_name_field.clear()
        last_name_field.clear()
        email_field.clear()

        # Simuler la mise à jour des champs
        qtbot.keyClicks(first_name_field, "alice")
        qtbot.keyClicks(last_name_field, "wonderup")
        qtbot.keyClicks(email_field, "alice@email.com")

        print("Champs mis à jour :", first_name_field.text(), last_name_field.text(), email_field.text())

        # Récupérer la combobox des rôles et sélectionner un rôle
        roles_combobox = dialog.findChild(QComboBox, "Role_combobox")
        assert roles_combobox is not None, "La combobox des rôles n'a pas été trouvée."
        
        print("Combobox des rôles récupérée. Nombre de rôles:", roles_combobox.count())
        roles_combobox.setCurrentIndex(3)  # Sélectionner un rôle particulier
        print("Rôle sélectionné:", roles_combobox.currentText())
        print("Rôle_id sélectionné:", roles_combobox.currentData())


    def test_create_user(self, management_view):
        """Test de la méthode create_user de ManagementView."""
        # Simuler les données d'utilisateur
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'Password1234',
            'employee_number': '12345',
            'email': 'john.doe@example.com',
            'role': 'COMMERCIAL'
        }
        # Simuler un dialog
        mock_dialog = MagicMock()
        # Mock de la méthode create_user du contrôleur
        with patch.object(management_view.controller, 'create_user', return_value=MagicMock(first_name='John', last_name='Doe')) as mock_create_user, \
            patch.object(QMessageBox, 'information') as mock_info, \
            patch.object(QMessageBox, 'warning') as mock_warning:
            # Appeler la méthode create_user
            management_view.create_user(mock_dialog, **user_data)
            # Vérifier que la méthode create_user du contrôleur a été appelée avec les bonnes données
            mock_create_user.assert_called_once_with(
                first_name='John',
                last_name='Doe',
                password='Password1234',
                employee_number='12345',
                email='john.doe@example.com',
                role='COMMERCIAL'
            )
            # Vérifier que QMessageBox.information a été appelée
            mock_info.assert_called_once_with(
                management_view,
                "Success",
                "User Doe John created successfully."
            )
            # Vérifier que le dialog a été accepté
            mock_dialog.accept.assert_called_once()
            # Vérifier que QMessageBox.warning n'a pas été appelée
            mock_warning.assert_not_called()

    def test_create_contract_success(self, management_view):
        """Test de la méthode create_contract de ManagementView avec succès."""
        
        # Simuler les données de contrat
        field_entries = {
            'contract_name': 'Important Contract',
            'contract_value': '50000',
            'start_date': '2024-01-01',
            'end_date': '2025-01-01',
        }
        
        # Simuler un customer_id
        customer_id = 1

        # Simuler un dialog
        mock_dialog = MagicMock()

        # Mock de la méthode create_contract du contrôleur
        with patch.object(management_view.controller, 'create_contract') as mock_create_contract, \
            patch.object(QMessageBox, 'information') as mock_info, \
            patch.object(QMessageBox, 'warning') as mock_warning:

            # Appeler la méthode create_contract
            management_view.create_contract(mock_dialog, customer_id, **field_entries)

            # Vérifier que la méthode create_contract du contrôleur a été appelée avec les bonnes données
            mock_create_contract.assert_called_once_with(
                customer_id,
                contract_name='Important Contract',
                contract_value='50000',
                start_date='2024-01-01',
                end_date='2025-01-01'
            )

            # Vérifier que QMessageBox.information a été appelée avec le message de succès
            mock_info.assert_called_once_with(
                management_view,
                "Success",
                "Contract created successfully."
            )

            # Vérifier que le dialog a été accepté
            mock_dialog.accept.assert_called_once()


    
    def test_delete_user_window_success(self, qtbot, management_view):
        """Test de la méthode delete_user_window de ManagementView avec succès."""

        # Simuler la liste des utilisateurs
        users = [
            {'id': 1, 'first_name': 'John', 'last_name': 'Doe'},
            {'id': 2, 'first_name': 'Alice', 'last_name': 'Wonder'}
        ]

        # Simuler l'utilisateur authentifié
        authenticated_user = MagicMock(id=1)
        management_view.controller.authenticated_user = authenticated_user

        # Mock de la méthode get_user_list du contrôleur
        with patch.object(management_view.controller, 'get_user_list', return_value=users) as mock_get_user_list, \
            patch.object(management_view, 'confirm_delete_user') as mock_confirm_delete_user, \
            patch.object(QDialog, 'exec', return_value=QDialog.Accepted):

            # Appeler la méthode delete_user_window
            management_view.delete_user_window()

            # Vérifier que la méthode get_user_list a été appelée
            mock_get_user_list.assert_called_once()

            # Vérifier que la combobox contient le bon utilisateur (celui qui n'est pas l'utilisateur authentifié)
            user_combobox = management_view.findChild(QComboBox)
            assert user_combobox is not None, "La combobox des utilisateurs n'a pas été trouvée."
            assert user_combobox.count() == 1, "La combobox ne contient pas le bon nombre d'utilisateurs."
            assert user_combobox.itemText(0) == "Alice Wonder - 2", "Le mauvais utilisateur est dans la combobox."

            # Simuler la sélection de l'utilisateur et le clic sur OK
            user_combobox.setCurrentIndex(0)
            ok_button = management_view.findChild(QDialogButtonBox).button(QDialogButtonBox.Ok)
            qtbot.mouseClick(ok_button, Qt.LeftButton)

            # Vérifier que confirm_delete_user a été appelée avec le bon utilisateur
            mock_confirm_delete_user.assert_called_once_with(
                management_view.findChild(QDialog), user_combobox
            )