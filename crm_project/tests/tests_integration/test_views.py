import pytest
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
from crm_project.views.management_view import ManagementView
from unittest.mock import Mock


@pytest.fixture
def qtbot(qtbot):
    """Fixture pour initialiser QApplication."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return qtbot

@pytest.fixture
def management_view(qtbot):
    """Fixture pour initialiser ManagementView avec un contrôleur mocké."""
    main_window = Mock()  # Simuler la fenêtre principale
    controller = Mock()   # Simuler le contrôleur
    controller.authenticated_user.first_name = "John"
    controller.authenticated_user.last_name = "Doe"
    view = ManagementView(main_window, controller)
    qtbot.addWidget(view)  # Ajoute le widget à l'environnement de test Qt
    print('VIEWS OOOK ')
    return view

class TestManagementView:
    """Classe de test pour la vue ManagementView."""

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