import tkinter as tk
from tkinter import messagebox
from helpers.get_data import *

import sys

import tkinter as tk
from tkinter import messagebox


from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QAction, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QCalendarWidget, QLabel, \
                              QPushButton, QCheckBox, QSpinBox, QLCDNumber, QLineEdit, \
                              QSlider, QProgressBar, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QScrollArea, QDialog


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
        customers = get_customers_list(self.controller.session)
        if customers:
            # Créer une nouvelle boîte de dialogue pour afficher les clients
            dialog = QDialog(self)
            dialog.setWindowTitle("Customer List")

            # Layout principal
            layout = QVBoxLayout()

            # Créer un en-tête pour les informations des clients
            header = QLabel("Customer Information")
            header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(header)

            # Utiliser un QScrollArea pour pouvoir faire défiler la liste des clients si elle est longue
            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()

            # Afficher les informations de chaque client
            for customer in customers:
                customer_info = (
                    f"ID: {customer['id']}<br>"
                    f"Name: {customer['first_name']} - {customer['last_name']}<br>"
                    f"Email: {customer['email']}<br>"
                    f"Company: {customer['company_name']}<br>"
                    f"Creation Date: {customer['creation_date']}<br>"
                    f"Last Update: {customer['last_update']}<br>"
                    f"Commercial Contact ID: {customer['commercial_contact_id']}<br>"
                    "---------------------------------------<br>"
                )

                # Créer un QLabel pour afficher les informations du client
                customer_label = QLabel(customer_info)
                customer_label.setTextFormat(Qt.RichText)  # Pour gérer les sauts de ligne et HTML
                scroll_layout.addWidget(customer_label)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            scroll_area.setWidgetResizable(True)
            
            # Ajouter le scroll area au layout principal
            layout.addWidget(scroll_area)

            # Appliquer le layout à la boîte de dialogue
            dialog.setLayout(layout)
            dialog.resize(400, 400)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No customers found.")

    def view_events(self):
        events = get_events_list(self.controller.session)
        if events:
            # Créer une nouvelle boîte de dialogue pour afficher les événements
            dialog = QDialog(self)
            dialog.setWindowTitle("Events List")

            # Layout principal
            layout = QVBoxLayout()

            # Créer un en-tête pour les informations des événements
            header = QLabel("Events Information")
            header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(header)

            # Utiliser un QScrollArea pour permettre de faire défiler les événements
            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()

            # Afficher les informations de chaque événement
            for event in events:
                event_info = f"Event Name: {event.name}<br>" \
                            f"Date: {event.date}<br>" \
                            "---------------------------------------<br>"
                event_label = QLabel(event_info)
                event_label.setTextFormat(Qt.RichText)  # Pour gérer les sauts de ligne et HTML
                scroll_layout.addWidget(event_label)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            scroll_area.setWidgetResizable(True)

            # Ajouter le QScrollArea au layout principal
            layout.addWidget(scroll_area)

            # Appliquer le layout à la boîte de dialogue
            dialog.setLayout(layout)
            dialog.resize(400, 400)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No events found.")
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

            # Utiliser un QScrollArea pour permettre de faire défiler les contrats
            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()

            # Afficher les informations de chaque contrat
            for contract in contracts:
                contract_info = f"Contract ID: {contract.id}<br>" \
                                f"Amount Due: {contract.amount_due}<br>" \
                                f"Remaining Amount: {contract.remaining_amount}<br>" \
                                "---------------------------------------<br>"
                contract_label = QLabel(contract_info)
                contract_label.setTextFormat(Qt.RichText)  # Pour gérer les sauts de ligne et HTML
                scroll_layout.addWidget(contract_label)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            scroll_area.setWidgetResizable(True)

            # Ajouter le QScrollArea au layout principal
            layout.addWidget(scroll_area)

            # Appliquer le layout à la boîte de dialogue
            dialog.setLayout(layout)
            dialog.resize(400, 400)
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

