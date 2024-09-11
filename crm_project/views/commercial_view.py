"""
Description : 
    Brève description du but du script, de ce qu'il fait, et de son contexte.
    Cela peut inclure un résumé des fonctionnalités principales.

Usage :
    Décrit comment utiliser le script, en fournissant des exemples de la ligne de commande ou en expliquant 
    les entrées et sorties principales.

Dépendances :
    Liste des bibliothèques externes nécessaires au fonctionnement du script (modules standard, bibliothèques tierces).
    Ex : PySide6, SQLAlchemy, etc.

Entrées :
    Décrit les paramètres ou les données nécessaires au script, si applicable.
    Ex : les paramètres d'entrée des fonctions principales ou les arguments de la ligne de commande.

"""

from crm_project.helpers.get_data import *
from crm_project.views import *
from crm_project.views.widget_maker import *
from crm_project.views.main_view import *

from datetime import datetime, timedelta
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout ,QComboBox, QLineEdit, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGridLayout,
                               QSpacerItem, QSizePolicy, QFormLayout, QCheckBox,
                               QSlider, QDateEdit, QTableWidget, QTableWidgetItem,
                               QRadioButton, QTextEdit
                               )



class CommercialView(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.authenticated_user = controller.authenticated_user
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        """
            Setup dynamiquement les widgets pour les différente fonctionnalités dans une grid
        """
        layout = QVBoxLayout()

        welcome_label = QLabel(f"Commercial Dashboard, Welcome {self.authenticated_user.first_name} {self.authenticated_user.last_name}")
        welcome_label.setStyleSheet("font-size: 16px; font-family: Helvetica;")
        welcome_label.setObjectName("label_titre")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        grid = QGridLayout()
        
        self.create_customer_button = QPushButton("Create New Customer")
        self.create_customer_button.clicked.connect(self.create_customer_window)
        self.update_customer_button = QPushButton("Update a Customer")
        self.update_customer_button.clicked.connect(self.update_customer_window)
        self.get_filter_contract_button = QPushButton("Get Filter Contracts")
        self.get_filter_contract_button.clicked.connect(self.filter_contract_window)
        self.update_contract_button = QPushButton("Update a Contract")
        self.update_contract_button.clicked.connect(self.open_update_contract_dialog)
        self.create_event_button = QPushButton("Create a New Event")
        self.create_event_button.clicked.connect(self.create_event_window)

        widgets = [
            self.create_customer_button,
            self.update_customer_button,
            self.get_filter_contract_button,
            self.update_contract_button,
            self.create_event_button
        ]

        columns = 2

        # Créer dynamiquement les cellule de la grid 
        mk_setup_widgets(self, layout, grid,  columns, widgets)

    def open_update_contract_dialog(self):
        dialog = mk_create_dialog_window(self, 'Update a contract')
        update_contract_window(self, dialog)
        
    def create_customer_window(self):
        """
        Ouvre une fenêtre modale pour créer un customer.
        """
        dialog = mk_create_dialog_window(self, 'Create a New Customer')
        self.form_layout = QFormLayout(self)

        fields_dict = {
            'first_name': 'Customer First Name:',
            'last_name': ' Customer Last Name:',
            'email': 'Customer Email:',
            'company_name': 'Company Name:'
        }
        mk_create_edit_lines(self, fields_dict)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_customer(dialog, 
            first_name=self.field_entries['first_name'].text(),
            last_name=self.field_entries['last_name'].text(),
            email=self.field_entries['email'].text(),
            company_name=self.field_entries['company_name'].text()
        ))
        buttons.rejected.connect(dialog.reject)
        self.form_layout.addWidget(buttons)
        dialog.setLayout(self.form_layout)
        dialog.exec()
    
    def create_customer(self, dialog,  **field_entries):
        """
        Appelle le contrôleur pour créer un nouveau client avec les données fournies.
        """
        try:
            new_customer = self.controller.create_customer(**field_entries)
            QMessageBox.information(self, "Success", f"Customer {new_customer.last_name} created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def update_customer_window(self):
        """
        Ouvre une fenêtre modale pour mettre à jour un client.
        """

        dialog = mk_create_dialog_window(self, "Update a Customer")
        self.form_layout = QFormLayout(self)
        customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
        display_names = get_display_customer_name(customers)

        mk_create_combox_id_name(self, customers, display_names, "Contract")

        fields_dict = {
            'first_name': 'Customer First Name',
            'last_name': 'Customer Last Name',
            'email': 'Customer Email',
            'company_name': 'Company Name',
        }
        mk_create_edit_lines(self, fields_dict)

        self.combobox.currentIndexChanged.connect(lambda: mk_update_fields(self))

        # Remplir automatiquement les champs lorsque le client est sélectionné
        mk_update_fields(self)

        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.update_customer(dialog, 
            first_name=self.field_entries['first_name'].text(),
            last_name=self.field_entries['last_name'].text(),
            email=self.field_entries['email'].text(),
            company_name=self.field_entries['company_name'].text()
        ))
        buttons.rejected.connect(dialog.reject)
        self.form_layout.addWidget(buttons)
        dialog.setLayout(self.form_layout)
        dialog.exec()

    def update_customer(self, dialog, **updated_data):
        try:
            customer_id = self.selected_id
            updated_customer = self.controller.update_customer(customer_id, **updated_data)
            QMessageBox.information(self, "Success", "Customer updated successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


    def filter_contract_window(self):
        """
            Ouvre une modale pour filtrer les contracts
        """
        dialog = mk_create_dialog_window(self, "Get Filter Contract")
        self.form_layout = QFormLayout(self)

        customers = get_customers_list(self.controller.session)
        display_names = [f"{customer.last_name} {customer.first_name} - {customer.id}" for customer in customers]
        mk_create_combox_id_name(self, customers, display_names, 'Customer')
        self.combobox.addItem("All Customers", None)

        mk_create_checkbox(self, "Filter by Status (Active=Signed)", False)

        field_dict = {
            'contract_status': ['All', 'Paid', 'Not Paid']
        }
        mk_create_radio_buttons(self, field_dict, "All")

        self.amount_due_min_slider, self.amount_due_min_lineedit = mk_create_slider_with_lineedit(self,
        "Min Amount Due:", 0, 10000, 0)

        self.amount_due_max_slider, self.amount_due_max_lineedit = mk_create_slider_with_lineedit(self,
        "Max Amount Due:", 0, 10000, 10000)

        self.creation_date_after = mk_create_dateedit(self,
        "Contract Create After:", QDate.currentDate().addDays(-5))
    
        self.creation_date_before = mk_create_dateedit(self,
        "Contract Create Before:", QDate.currentDate().addDays(5))

        # Boutons pour appliquer ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.apply_filter)
        buttons.rejected.connect(dialog.reject)
        self.form_layout.addWidget(buttons)

        dialog.setLayout(self.form_layout)
        dialog.exec()
    
    def apply_filter(self):
        """
        Applique les filtres et affiche la liste des contrats filtrés.
        """
        filter_data = {}

        if self.checkbox.isChecked():
            filter_data['status'] = True
        selected_payment_status = get_selected_radio_value(self, 'contract_status')
        if selected_payment_status == "Paid":
            filter_data['paid'] = True
        elif selected_payment_status == "Not Paid":
            filter_data['paid'] = False
        else:
            filter_data['paid'] = None
        
        # Récupérer l'ID du client sélectionné dans la combobox
        filter_data['customer_id'] = self.combobox.currentData()

        # Récupérer les valeurs des sliders pour les montants
        filter_data['amount_due_min'] = self.amount_due_min_slider.value()
        filter_data['amount_due_max'] = self.amount_due_max_slider.value()

        # Récupérer les dates de création avant et après
        filter_data['creation_date_before'] = self.creation_date_before.date().toPython()
        filter_data['creation_date_after'] = self.creation_date_after.date().toPython()

        # Appeler la méthode de filtrage des contrats avec les données collectées
        contracts = self.controller.contract_filter(filter_data)
        
        # Afficher les contrats filtrés
        self.show_filtered_contracts(contracts)

    def show_filtered_contracts(self, contracts):

        """
        Affiche les contrats filtrés dans une nouvelle fenêtre.
        """
        if contracts:
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

    def create_event_window(self):
        dialog = mk_create_dialog_window(self, 'Create a New Event')
        self.form_layout = QFormLayout(self)

        supports = get_support_user(self.controller.session)
        customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
        display_name = get_display_customer_name(customers)

        mk_create_combox_id_name(self, customers, display_name, 'Customer')

        self.contract_combobox = QComboBox()
        self.form_layout.addRow('Select Contract : ', self.contract_combobox)
        self.combobox.currentIndexChanged.connect(self.update_contracts_combobox)
        self.update_contracts_combobox()
        self.support_combobox = QComboBox()
        for support in supports:
            display_name = f"{support.last_name} {support.first_name}"
            self.support_combobox.addItem(display_name, support.id)
        self.form_layout.addRow('Select Support Contact :', self.support_combobox)

        fields_dict = {
            'name':' Name of this Event',
            'location': 'Location',
            'attendees':'Attendees',
        }
        self.field_entries = mk_create_edit_lines(self, fields_dict)
        self.comment_entry = QTextEdit()
        self.comment_entry.setFixedHeight(80)
        self.form_layout.addRow('Comment', self.comment_entry)
        self.start_date = mk_create_dateedit(self, 'Start Date', QDate.currentDate().addDays(0))
        self.end_date = mk_create_dateedit(self, 'End Date', QDate.currentDate().addDays(0))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_event(dialog, 
            name=self.field_entries['name'].text(),
            location=self.field_entries['location'].text(),
            attendees=self.field_entries['attendees'].text(),
            comment=self.comment_entry.toPlainText(),
            start_date=self.start_date.date().toPython(),
            end_date=self.end_date.date().toPython(),
            support_contact_id=self.support_combobox.currentData(),
            contract_id=self.contract_combobox.currentData()
        ))
        buttons.rejected.connect(dialog.reject)
        self.form_layout.addWidget(buttons)
        dialog.setLayout(self.form_layout)
        dialog.exec()

    def create_event(self, dialog, **event_data):
        print(event_data)
        try:
            new_event = self.controller.create_event(**event_data)
            QMessageBox.information(self, "Success", f"Event : {new_event.name} create successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            print(f'"Error", "An error occurred: {e}"')

    def update_contracts_combobox(self):
        """
        Met à jour la liste des contrats en fonction du client sélectionné.
        """
        self.selected_customer_id = self.combobox.currentData()
        self.selected_customer = self.data_dict.get(self.selected_customer_id)
        if self.selected_customer:
            self.contract_combobox.clear()
            # Récupérer et ajouter les contrats du client sélectionné dans le second ComboBox
            for contract in self.selected_customer.contracts:
                self.contract_combobox.addItem(f"Contract {contract.id}", contract.id)
        else:
          self.contract_combobox.clear()