import sys

from crm_project.helpers.get_data import *
from crm_project.views.widget_maker import *
from crm_project.project.permissions import view_authenticated_user

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QAction, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QCalendarWidget, QLabel, \
                              QPushButton, QCheckBox, QSpinBox, QLCDNumber, QLineEdit, \
                              QSlider, QProgressBar, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QScrollArea, QDialog, QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Epic Event - Customer Relational Management")
        self.setWindowIcon(QIcon("D:\openclassroom\projets\projet_10\Epic_Event_CRM\crm_project\images\logo.png"))

        self.resize(600, 600)
        self.setMaximumSize(800, 600)
        self.setMinimumSize(600, 400)

        self.setup_menu_bar()
        self.menuBar().hide()  

        statusBar = self.statusBar()
        statusBar.showMessage(self.windowTitle())

        central_area = QWidget()
        self.setCentralWidget(central_area)
    
    def set_controller(self, controller):
        self.controller = controller
        controller.show_login_view()

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        report_menu = menu_bar.addMenu('&Report')
        profil_menu = menu_bar.addMenu('&Profil')

        # File Menu
        logout_action = QAction("Logout", self)
        exit_action = QAction("Exit", self)
        logout_action.triggered.connect(self.logout)
        exit_action.triggered.connect(self.close) 
        
        # Report Menu
        customer_list_action = QAction("Customers List", self)
        contract_list_action = QAction("Contract List", self)
        event_list_action = QAction("Event List", self)
        customer_list_action.triggered.connect(self.view_customers)
        contract_list_action.triggered.connect(self.view_contracts)
        event_list_action.triggered.connect(self.view_events)

        # profil Menu*
        change_username_action = QAction("Change your username", self)
        change_password_action = QAction("Change your password", self)
        change_username_action.triggered.connect(self.change_username_dialog)
        change_password_action.triggered.connect(self.change_password_dialog)

        file_menu.addAction(exit_action)
        file_menu.addAction(logout_action)
        report_menu.addAction(customer_list_action)
        report_menu.addAction(contract_list_action)
        report_menu.addAction(event_list_action)
        profil_menu.addAction(change_username_action)
        profil_menu.addAction(change_password_action)

    @view_authenticated_user
    def change_username_dialog(self):
        dialog = mk_create_dialog_window(self, "Change your Username")
        form_layout = QFormLayout()
        username_entry = QLineEdit()
        form_layout.addRow('Choose a New Username', username_entry)

        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.change_username(dialog, username_entry.text()))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.exec()

    @view_authenticated_user
    def change_username(self, dialog, username):
        try :
            self.controller.change_user_username(username)
            QMessageBox.information(self, "Success", "username Updated successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))

    @view_authenticated_user
    def change_password_dialog(self):
        dialog = mk_create_dialog_window(self, "Change your Password")
        form_layout = QFormLayout()
        old_password_entry = QLineEdit()
        form_layout.addRow('Enter your old password', old_password_entry)
        new_password_entry = QLineEdit()
        validation_password_entry = QLineEdit()
        form_layout.addRow('Enter a New password', new_password_entry)
        form_layout.addRow('Confirm password', validation_password_entry)
        old_password_entry.setEchoMode(QLineEdit.Password)
        new_password_entry.setEchoMode(QLineEdit.Password)
        validation_password_entry.setEchoMode(QLineEdit.Password)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.change_password(
            dialog,
            old_password_entry.text(),
            new_password_entry.text(),
            validation_password_entry.text()
            ))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.exec()

    @view_authenticated_user
    def change_password(self, dialog, old_password, new_password, validation_password):
        if not old_password:
            QMessageBox.warning(dialog, "Input Error", "Old password cannot be empty.")
            return
        if len(new_password) < 8:
            QMessageBox.warning(dialog, "Input Error", "New password must be at least 8 characters long.")
            return
        if new_password != validation_password:
            QMessageBox.warning(dialog, "Input Error", "New passwords do not match.")
            return
        try:
            self.controller.change_user_password(old_password, new_password)
            QMessageBox.information(self, "Success", "Password update successfully.")
            dialog.accept()
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))


    @view_authenticated_user
    def view_customers(self):
        customers = self.controller.session.query(Customer).all()
        if customers:
            # Préparer les list à afficher
            labels_list = ["Customer ID", "Name", "Email", "Phone Contact","Company Name", 
                        "Commercial Contact", "Creation Date", "Last Update"]
            attributes_list = ["id", "name", "email","phone_number" ,"company_name", 
                            "commercial_contact", "creation_date", "last_update"]
            # Créer la table
            table = mk_create_table(labels_list, customers, attributes_list)
            # Affiche la fenêtre avec le tableau
            mk_create_table_window(self, "Customer tabel", 'Customer Informations', table)
        else:
            QMessageBox.warning(self, "Error", "No customers found.")

    @view_authenticated_user
    def view_events(self):
        events = get_events_list(self.controller)
        if events:
            for event in events:
                if event.contract and event.contract.customer:
                    event.customer_name = event.contract.customer.name
            labels_list =  ["Event ID","contract ID", "Name", "Support Contact",
                            "Customer Name", "Start Date","End Date", "Location",
                            "Attendees", "Comment"]
            attributes_list = ["id", "contract_id", "name", "support_contact", "customer_name",
                               "start_date", "end_date", "location", "attendees", "comment"]
            table = mk_create_table(labels_list, events, attributes_list)
            mk_create_table_window(self, "Events Table", "Event Informations", table)

        else:
            QMessageBox.warning(self, "Error", "No Event found.")

    @view_authenticated_user
    def view_contracts(self):
        contracts = get_contracts_list(self.controller)
        if contracts:
            for contract in contracts:
                contract.customer_name = contract.customer.name
                contract.customer_contact = f"{contract.customer.email} - {contract.customer.phone_number}"
            labels_list = ["Contract ID", "Status", "Customer", "Customer Contact",
                           "Commercial Contact", "Creation Date", "Last Update",
                           "Amount Due", "Remaining Amount"]
            attributes_list = ['id', 'status', 'customer_name', 'customer_contact','commercial_contact',
                               'creation_date', 'last_update', 'amount_due',
                               'remaining_amount']
            table = mk_create_table(labels_list, contracts, attributes_list)
            mk_create_table_window(self, "Contract Table", "Contract Informations", table)
        else:
            QMessageBox.warning(self, "Error", "No contracts found.")

    def logout(self):
        # Créer et afficher une boîte de dialogue
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Logout")
        msg_box.setText("Do you really want to logout?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setIcon(QMessageBox.Question)
        result = msg_box.exec()
        if result == QMessageBox.Yes:
            self.menuBar().hide()
            self.controller.show_login_view()
            success_msg_box = QMessageBox(self)
            success_msg_box.setWindowTitle("Logout Success")
            success_msg_box.setText("You have been successfully logged out.")
            success_msg_box.setIcon(QMessageBox.Information)
            success_msg_box.setStandardButtons(QMessageBox.Ok)
            success_msg_box.exec()

