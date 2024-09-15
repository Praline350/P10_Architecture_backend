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
from crm_project.views.sharing_view import *
from crm_project.project.permissions import view_authenticated_user, decorate_all_methods

from datetime import datetime, timedelta
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout ,QComboBox, QLineEdit, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGridLayout,
                               QSpacerItem, QSizePolicy, QFormLayout, QCheckBox,
                               QSlider, QDateEdit, QTableWidget, QTableWidgetItem,
                               QRadioButton, QTextEdit
                               )


@decorate_all_methods(view_authenticated_user)
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
            'name': 'Customer Full Name',
            'email': 'Customer Email:',
            'phone_number': 'Customer Phone Number',
            'company_name': 'Company Name:'
        }
        mk_create_edit_lines(self, fields_dict)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_customer(dialog, 
            name=self.field_entries['name'].text(),
            email=self.field_entries['email'].text(),
            phone_number=self.field_entries['phone_number'].text(),
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
            QMessageBox.information(self, "Success", f"Customer {new_customer.name} created successfully.")
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
        form_layout = QFormLayout(self)
        customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
        display_names = get_display_customer_name(customers)

        data_dict, customer_combobox = mk_create_combox_id_name(self,form_layout, customers, display_names, "Customer")

        fields_dict = {
            'name': 'Customer Full Name',
            'email': 'Customer Email',
            'phone_number': 'Customer Phone Number',
            'company_name': 'Company Name',
        }
        field_entries = mk_create_edit_lines(self, fields_dict)

        customer_combobox.currentIndexChanged.connect(lambda: mk_update_fields(self))

        # Remplir automatiquement les champs lorsque le client est sélectionné
        mk_update_fields(self, customer_combobox, data_dict, field_entries)

        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.update_customer(dialog, customer_combobox.currentData(),
            name=self.field_entries['name'].text(),
            email=self.field_entries['email'].text(),
            phone_number=self.field_entries['phone_number'].text(),
            company_name=self.field_entries['company_name'].text()
        ))
        buttons.rejected.connect(dialog.reject)
        self.form_layout.addWidget(buttons)
        dialog.setLayout(self.form_layout)
        dialog.exec()

    def update_customer(self, dialog, customer_id,  **updated_data):
        try:
            updated_customer = self.controller.update_customer(customer_id, **updated_data)
            QMessageBox.information(self, "Success", f"Customer {updated_customer.name} updated successfully.")
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
        form_layout = QFormLayout(self)

        customers = get_customers_list(self.controller.session)
        display_names = get_display_customer_name(customers)
        data_dict, customer_combobox = mk_create_combox_id_name(self, form_layout, customers, display_names, 'Customer')
        customer_combobox.addItem("All Customers", None)

        status_checkbox = mk_create_checkbox(self, form_layout, "Filter by Status (Active=Signed)", False)

        field_dict = {
            'contract_status': ['All', 'Paid', 'Not Paid']
        }
        radio_button_entries = mk_create_radio_buttons(self, form_layout, field_dict, "All")

        amount_due_min_slider, amount_due_min_lineedit = mk_create_slider_with_lineedit(self, form_layout,
        "Min Amount Due:", 0, 10000, 0)

        amount_due_max_slider, amount_due_max_lineedit = mk_create_slider_with_lineedit(self, form_layout,
        "Max Amount Due:", 0, 10000, 10000)

        creation_date_after = mk_create_dateedit(self, form_layout,
        "Contract Create After:", QDate.currentDate().addDays(-5))
    
        creation_date_before = mk_create_dateedit(self, form_layout,
        "Contract Create Before:", QDate.currentDate().addDays(5))

        # Boutons pour appliquer ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda : self.apply_filter(
            checkbox=status_checkbox,
            radio_button=radio_button_entries,
            combobox=customer_combobox,
            amount_due_min=amount_due_min_slider,
            amount_due_max=amount_due_max_slider,
            creation_date_after=creation_date_after,
            creation_date_before=creation_date_before
              ))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.exec()
    
    def apply_filter(self, **filter_data_entries):
        """
        Applique les filtres et affiche la liste des contrats filtrés.
        """
        filter_data = {}
        print(f"Checkbox état: {filter_data_entries['checkbox'].isChecked()}")
        if filter_data_entries['checkbox'].isChecked():
            filter_data['status'] = True
        else:
            filter_data['status'] = False
        selected_payment_status = get_selected_radio_value(self,filter_data_entries["radio_button"], 'contract_status')
        if selected_payment_status == "Paid":
            filter_data['paid'] = True
        elif selected_payment_status == "Not Paid":
            filter_data['paid'] = False
        else:
            filter_data['paid'] = None
        
        filter_data['customer_id'] = filter_data_entries['combobox'].currentText()
        filter_data['amount_due_min'] = filter_data_entries['amount_due_min'].value()
        filter_data['amount_due_max'] = filter_data_entries['amount_due_max'].value()
        filter_data['creation_date_before'] = filter_data_entries['creation_date_before'].date().toPython()
        filter_data['creation_date_after'] = filter_data_entries['creation_date_after'].date().toPython()

        print(filter_data)
        contracts = self.controller.contract_filter(**filter_data)
        self.show_filtered_contracts(contracts)

    def show_filtered_contracts(self, contracts):

        """
        Affiche les contrats filtrés dans une nouvelle fenêtre.
        """
        if contracts:
            for contract in contracts:
                contract.customer_name = contract.customer.name
                contract.commercial_contact_name = contract.commercial_contact.full_name
            labels_list =[
                "Contract ID", "Status", "Customer",
                "Commercial Contact", "Creation Date",
                "Last Update", "Amount Due", "Remaining Amount"
            ]
            attributes_list = [
                "id", "status", "customer_name", "commercial_contact_name",
                "creation_date", 'last_update', "amount_due", "remaining_amount"
            ]

            table = mk_create_table(labels_list, contracts, attributes_list)
            mk_create_table_window(self, "Filter Contracts", "Contract Information", table)
        else:
            QMessageBox.warning(self, "Error", "No contracts found.")

    def create_event_window(self):
        dialog = mk_create_dialog_window(self, 'Create a New Event')
        self.form_layout = QFormLayout(self)

        customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
        display_name = get_display_customer_name(customers)

        mk_create_combox_id_name(self, customers, display_name, 'Customer')

        self.contract_combobox = QComboBox()
        self.form_layout.addRow('Select Contract : ', self.contract_combobox)
        self.combobox.currentIndexChanged.connect(self.update_contracts_combobox)
        self.update_contracts_combobox()
        self.support_combobox = QComboBox()

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