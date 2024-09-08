import sys

from crm_project.helpers.get_data import *

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



        file_menu.addAction(exit_action)
        file_menu.addAction(logout_action)
        report_menu.addAction(customer_list_action)
        report_menu.addAction(contract_list_action)
        report_menu.addAction(event_list_action)

    
    def view_customers(self):
        customers = self.controller.session.query(Customer).all()
        if customers:
            # Créer une nouvelle boîte de dialogue pour afficher les contrats
            dialog = QDialog(self)
            dialog.setWindowTitle("Customers List")

            # Layout principal
            layout = QVBoxLayout()

            # Créer un en-tête pour les informations des contrats
            header = QLabel("Customers Information")
            header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(header)

            # Tableau pour afficher les contrats 
            table = QTableWidget()
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels(["Customer ID",
                                             "First Name",
                                             "Last Name",
                                             "Email",
                                             "Company Name",
                                             "Commercial Contact",
                                             "Creation Date",
                                             "Last Update"
                                             ])
            table.setRowCount(len(customers)) 
            for i, customer in enumerate(customers):
                table.setItem(i, 0, QTableWidgetItem(str(customer.id)))
                table.setItem(i, 1, QTableWidgetItem(str(customer.first_name)))
                table.setItem(i, 2, QTableWidgetItem(str(customer.last_name)))
                table.setItem(i, 3, QTableWidgetItem(str(customer.email)))
                table.setItem(i, 4, QTableWidgetItem(str(customer.company_name)))
                table.setItem(i, 5, QTableWidgetItem(
                    str(f"{customer.commercial_contact.first_name} - {customer.commercial_contact.last_name}"
                        )))
                table.setItem(i, 6, QTableWidgetItem(customer.creation_date.strftime('%Y-%m-%d')))
                table.setItem(i, 7, QTableWidgetItem(customer.last_update.strftime('%Y-%m-%d')))

            table.resizeColumnsToContents()
            # Ajouter le tableau et le bouton de fermeture au layout
            layout.addWidget(table)
            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.accept)
            layout.addWidget(close_button)

            # Appliquer le layout à la boîte de dialogue et l'afficher
            dialog.setLayout(layout)
            dialog.resize(850,400 )  # Dimensionner la fenêtre à 600x400 pixels
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No customers found.")

    def view_events(self):
        events = get_events_list(self.controller.session)
        if events:
            # Créer une nouvelle boîte de dialogue pour afficher les contrats
            dialog = QDialog(self)
            dialog.setWindowTitle("Event List")

            # Layout principal
            layout = QVBoxLayout()

            # Créer un en-tête pour les informations des contrats
            header = QLabel("Event Information")
            header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(header)

            # Tableau pour afficher les contrats 
            table = QTableWidget()
            table.setColumnCount(10)
            table.setHorizontalHeaderLabels(["Event ID",
                                             "contract ID",
                                             "Name",
                                             "Support Contact",
                                             "Customer",
                                             "Start Date",
                                             "End Date",
                                             "Location",
                                             "Attendees",
                                             "Comment"
                                             ])
            table.setRowCount(len(events))
            for i, event in enumerate(events):
                table.setItem(i, 0, QTableWidgetItem(str(event.id)))
                table.setItem(i, 1, QTableWidgetItem(str(event.contract_id)))
                table.setItem(i, 2, QTableWidgetItem(str(event.name)))
                table.setItem(i, 3, QTableWidgetItem(str(event.support_contact.last_name)))
                table.setItem(i, 4, QTableWidgetItem(str(event.customer.name)))
                table.setItem(i, 5, QTableWidgetItem(event.start_date.strftime('%Y-%m-%d')))
                table.setItem(i, 6, QTableWidgetItem(event.end_date.strftime('%Y-%m-%d')))
                table.setItem(i, 7, QTableWidgetItem(str(event.location)))
                table.setItem(i, 8, QTableWidgetItem(str(event.attendees)))
                table.setItem(i, 9, QTableWidgetItem(str(event.comment)))

            table.resizeColumnsToContents()
            # Ajouter le tableau et le bouton de fermeture au layout
            layout.addWidget(table)
            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.accept)
            layout.addWidget(close_button)

            # Appliquer le layout à la boîte de dialogue et l'afficher
            dialog.setLayout(layout)
            dialog.resize(800,400 )  # Dimensionner la fenêtre à 600x400 pixels
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No Event found.")

    def view_contracts(self):
        contracts = get_contracts_list(self.controller.session)
        if contracts:
            # Créer une nouvelle boîte de dialogue pour afficher les contrats
            dialog = QDialog(self)
            dialog.setWindowTitle("Contracts List")

            # Layout principal
            layout = QVBoxLayout()

            # Créer un en-tête pour les informations des contrats
            header = QLabel("Contracts Information")
            header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(header)

            # Tableau pour afficher les contrats 
            table = QTableWidget()
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels(["Contract ID",
                                             "Status",
                                             "Customer",
                                             "Commercial Contact",
                                             "Creation Date",
                                             "Last Update",
                                             "Amount Due",
                                             "Remaining Amount"
                                             ])
            table.setRowCount(len(contracts))
            for i, contract in enumerate(contracts):
                table.setItem(i, 0, QTableWidgetItem(str(contract.id)))
                table.setItem(i, 1, QTableWidgetItem("Active" if contract.status else "Inactive"))
                table.setItem(i, 2, QTableWidgetItem(str(f"{contract.customer.last_name} - {contract.customer.first_name}")))
                table.setItem(i, 3, QTableWidgetItem(str(f"{contract.commercial_contact.last_name}- {contract.commercial_contact.first_name}")))
                table.setItem(i, 4, QTableWidgetItem(contract.creation_date.strftime('%Y-%m-%d')))
                table.setItem(i, 5, QTableWidgetItem(contract.last_update.strftime('%Y-%m-%d')))
                table.setItem(i, 6, QTableWidgetItem(str(contract.amount_due)))
                table.setItem(i, 7, QTableWidgetItem(str(contract.remaining_amount)))
            table.resizeColumnsToContents()
            # Ajouter le tableau et le bouton de fermeture au layout
            layout.addWidget(table)
            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.accept)
            layout.addWidget(close_button)

            # Appliquer le layout à la boîte de dialogue et l'afficher
            dialog.setLayout(layout)
            dialog.resize(850,400 )  # Dimensionner la fenêtre à 600x400 pixels
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No contracts found.")

    def logout(self):
        result = self.messagebox_template(
        title="Logout",
        message="Do you really want to logout?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        icon=QMessageBox.NoIcon  # Peut aussi être QMessageBox.NoIcon si tu ne veux pas d'icône
        )
        if result:
            self.menuBar().hide()  
            self.controller.show_login_view()
 

    def messagebox_template(self, title, message, buttons=QMessageBox.Ok, icon=QMessageBox.NoIcon):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(buttons)
        msg_box.setIcon(icon)

        # Affiche la boîte de dialogue et renvoie le résultat
        result = msg_box.exec()
        return result

