

from crm_project.helpers.get_data import *
from crm_project.views import *
from crm_project.views.widget_maker import *

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout ,QComboBox, QLineEdit, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGridLayout,
                               QSpacerItem, QSizePolicy, QFormLayout, QCheckBox,
                               QSlider, QDateEdit, QTableWidget, QTableWidgetItem,
                               QRadioButton
                               )



class CommercialView(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.authenticated_user = controller.authenticated_user
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
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
        self.update_contract_button.clicked.connect(self.update_contract_window)

        widgets = [
            self.create_customer_button,
            self.update_customer_button,
            self.get_filter_contract_button,
            self.update_contract_button
        ]

        columns = 2

        for index, widget in enumerate(widgets):
            row = index // columns
            column = index % columns
            grid.addWidget(widget, row, column)
            widget.setObjectName('management_buttons')
        layout.addLayout(grid)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)
        

    def create_customer_window(self):
        """
        Ouvre une fenêtre modale pour créer un customer.
        """
        # Fenêtre modale pour créer un contrat
        mk_create_dialog_window(self, 'Create a New Customer')

        fields_dict = {
            'first_name': 'Customer First Name:',
            'last_name': ' Customer Last Name:',
            'email': 'Customer Email:',
            'company_name': 'Company Name:'
        }
        mk_create_edit_lines(self, fields_dict)

        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_customer(
            first_name=self.field_entries['first_name'].text(),
            last_name=self.field_entries['last_name'].text(),
            email=self.field_entries['email'].text(),
            company_name=self.field_entries['company_name'].text()
        ))
        buttons.rejected.connect(self.dialog.reject)
        self.form_layout.addWidget(buttons)
        self.dialog.setLayout(self.form_layout)
        self.dialog.exec()
    
    def create_customer(self, **field_entries):
        """
        Appelle le contrôleur pour créer un nouveau client avec les données fournies.
        """
        try:
            new_customer = self.controller.create_customer(**field_entries)
            QMessageBox.information(self, "Success", f"Customer {new_customer.last_name} created successfully.")
            self.dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def update_customer_window(self):
        """
        Ouvre une fenêtre modale pour mettre à jour un client.
        """
        mk_create_dialog_window(self, "Update a Customer")
        customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
        display_names = [f"{customer.id} - {customer.last_name}" for customer in customers]

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
        buttons.accepted.connect(lambda: self.update_customer(
            first_name=self.field_entries['first_name'].text(),
            last_name=self.field_entries['last_name'].text(),
            email=self.field_entries['email'].text(),
            company_name=self.field_entries['company_name'].text()
        ))
        buttons.rejected.connect(self.dialog.reject)
        self.form_layout.addWidget(buttons)
        self.dialog.setLayout(self.form_layout)
        self.dialog.exec()

    def update_customer(self, **field_entries):
        print(field_entries)
        try:
            customer_id = self.selected_id
            updated_customer = self.controller.update_customer(customer_id, **field_entries)
            QMessageBox.information(self, "Success", "Customer updated successfully.")
            self.dialog.accept()  # Ferme la fenêtre après succès
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


    def filter_contract_window(self):
        mk_create_dialog_window(self, "Get Filter Contract")
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
        buttons.rejected.connect(self.dialog.reject)
        self.form_layout.addWidget(buttons)

        self.dialog.setLayout(self.form_layout)
        self.dialog.exec()
    
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


    def update_contract_window(self):
        """
        Ouvre une fenêtre modale pour mettre à jour un contrat.
        """
        # Fenêtre modale pour mettre à jour un client
        mk_create_dialog_window(self, 'Update a contract')
        contracts = get_contract_commercial(self.controller.authenticated_user, self.controller.session)
        display_names = [f"{contract.id} - {contract.customer.last_name}" for contract in contracts]

        mk_create_combox_id_name(self, contracts, display_names, "Contract")

        mk_create_checkbox(self, "Filter by Status (Active=Signed)", False)

        fields_dict = {
            'amount_due': 'Amount Due:',
            'remaining_amount': 'Remaining Amount:',
        }
        mk_create_edit_lines(self, fields_dict)
        self.field_entries['status'] = self.checkbox

        # Connecter l'événement de changement de sélection de la combobox à la fonction
        self.combobox.currentIndexChanged.connect(lambda: mk_update_fields(self))

        # Met a jour les champ en fonction du combobox et retourne le contract selectionné
        mk_update_fields(self)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.update_contract(
            amount_due=self.field_entries['amount_due'].text(),
            remaining_amount=self.field_entries['remaining_amount'].text(),
            status=self.field_entries['status'].isChecked() 
        ))
        buttons.rejected.connect(self.dialog.reject)
        self.form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        self.dialog.setLayout(self.form_layout)
        self.dialog.exec()


    def update_contract(self,**field_entries):
        print(f"F E :{field_entries}")
        try :
            contract_id = self.selected_id
            print(f"contract id : {contract_id}")
            updated_contract = self.controller.update_contract(contract_id, **field_entries)
            print(f"new contract : {updated_contract.to_dict()}")
            QMessageBox.information(self, "Success", f"Contract {updated_contract.id} updated successfully.")
            self.dialog.accept()  # Ferme la fenêtre après succès
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        



