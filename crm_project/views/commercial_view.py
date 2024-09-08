

from crm_project.helpers.get_data import *
from crm_project.views import *

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

        widgets = [
            self.create_customer_button,
            self.update_customer_button,
            self.get_filter_contract_button
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
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Customer")

        # Création du layout pour la fenêtre de création de contrat
        form_layout = QFormLayout()

        # Ajouter des champs à la fenêtre de création
        first_name_entry = QLineEdit()
        form_layout.addRow("Customer First_Name:", first_name_entry)

        last_name_entry = QLineEdit()
        form_layout.addRow("Customer Last_Name:", last_name_entry)

        # Champs pour l'email du client
        email_entry = QLineEdit()
        form_layout.addRow("Customer Email:", email_entry)

        # Champs pour le nom de la société
        company_name_entry = QLineEdit()
        form_layout.addRow("Company Name:", company_name_entry)

        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_customer(dialog, first_name_entry.text(), last_name_entry.text(), email_entry.text(), company_name_entry.text()))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.exec()
    
    def create_customer(self, dialog, first_name, last_name, email, company_name):
        """
        Appelle le contrôleur pour créer un nouveau client avec les données fournies.
        """
        # Préparation des données du client
        customer_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'company_name': company_name,
        }

        # Appel au contrôleur pour créer le client
        try:
            new_customer = self.controller.create_customer(**customer_data)
            QMessageBox.information(self, "Success", "Customer created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def update_customer_window(self):
        """
        Ouvre une fenêtre modale pour mettre à jour un client.
        """
        # Fenêtre modale pour mettre à jour un client
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Customer")
        form_layout = QFormLayout()

        customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
        customer_combobox = QComboBox()
        customer_data_dict = {}  # Dictionnaire pour stocker les données des clients avec leur ID

        for customer in customers:
            customer_display = f"{customer['id']} - {customer['first_name']} {customer['last_name']}"
            customer_combobox.addItem(customer_display, customer['id'])
            customer_data_dict[customer['id']] = customer  # Stocker les données des clients par ID

        form_layout.addRow("Customer:", customer_combobox)
        first_name_entry = QLineEdit()
        form_layout.addRow("Customer First Name:", first_name_entry)

        last_name_entry = QLineEdit()
        form_layout.addRow("Customer Last Name:", last_name_entry)

        email_entry = QLineEdit()
        form_layout.addRow("Customer Email:", email_entry)

        company_name_entry = QLineEdit()
        form_layout.addRow("Company Name:", company_name_entry)

        # Fonction pour mettre à jour les champs de texte avec les données du client sélectionné
        def update_fields():
            selected_customer_id = customer_combobox.currentData()
            selected_customer = customer_data_dict.get(selected_customer_id, {})

            # Préremplir les champs avec les informations du client
            first_name_entry.setText(selected_customer.get('first_name', ''))
            last_name_entry.setText(selected_customer.get('last_name', ''))
            email_entry.setText(selected_customer.get('email', ''))
            company_name_entry.setText(selected_customer.get('company_name', ''))

        # Connecter l'événement de changement de sélection de la combobox à la fonction
        customer_combobox.currentIndexChanged.connect(update_fields)

        # Remplir automatiquement les champs lorsque le client est sélectionné
        update_fields()

        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.update_customer(
            dialog,
            customer_combobox.currentData(),
            first_name_entry.text(),
            last_name_entry.text(),
            email_entry.text(),
            company_name_entry.text()
        ))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.exec()

    def update_customer(self, dialog, customer_id, first_name, last_name, email, company_name):
        customer_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'company_name': company_name,
        }
            # Appel au contrôleur pour mettre à jour le client
        try:
            updated_customer = self.controller.update_customer(customer_id, **customer_data)
            QMessageBox.information(self, "Success", "Customer updated successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


    def filter_contract_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Get Contract List by Filter")
        customers = get_customers_list(self.controller.session)

        form_layout = QFormLayout()

        self.customer_combobox = QComboBox()
        self.customer_combobox.addItem("All Customers", None)
        for customer in customers:
            customer_name = f"{customer['first_name']} {customer['last_name']}"
            self.customer_combobox.addItem(customer_name, customer['id'])
        form_layout.addRow("Select Customer:", self.customer_combobox)

        self.status_checkbox = QCheckBox()
        form_layout.addRow("Filter by Status (Active=Signed)", self.status_checkbox)

        # Créer un groupe de boutons radio pour le filtre sur le paiement
        self.paid_all_radio = QRadioButton("All")
        self.paid_radio = QRadioButton("Paid")
        self.not_paid_radio = QRadioButton("Not Paid")
        self.paid_all_radio.setChecked(True)

        paid_layout = QHBoxLayout()
        paid_layout.addWidget(self.paid_all_radio)
        paid_layout.addWidget(self.paid_radio)
        paid_layout.addWidget(self.not_paid_radio)
        form_layout.addRow("Filter by Payment Status:", paid_layout)
            
        # Min Amount Due Slider and Label
        self.amount_due_min_slider = QSlider(Qt.Horizontal)
        self.amount_due_min_slider.setRange(0, 10000)
        self.amount_due_min_slider.setValue(0)
        self.amount_due_min_lineedit = QLineEdit("0")
        self.amount_due_min_lineedit.setFixedWidth(60)

        amount_due_min_layout = QHBoxLayout()
        amount_due_min_layout.addWidget(self.amount_due_min_slider)
        amount_due_min_layout.addWidget(self.amount_due_min_lineedit)
        form_layout.addRow("Min Amount Due:", amount_due_min_layout)

        # Max Amount Due Slider and Label
        self.amount_due_max_slider = QSlider(Qt.Horizontal)
        self.amount_due_max_slider.setRange(0, 10000)
        self.amount_due_max_slider.setValue(10000)
        self.amount_due_max_lineedit = QLineEdit("10000")
        self.amount_due_max_lineedit.setFixedWidth(60)

        amount_due_max_layout = QHBoxLayout()
        amount_due_max_layout.addWidget(self.amount_due_max_slider)
        amount_due_max_layout.addWidget(self.amount_due_max_lineedit)
        form_layout.addRow("Max Amount Due:", amount_due_max_layout)

        # Creation contract Date filter
        self.creation_date_after = QDateEdit()
        self.creation_date_after.setCalendarPopup(True)
        self.creation_date_after.setDate(QDate.currentDate().addDays(-5))
        form_layout.addRow("Contract Create After:", self.creation_date_after)

        self.creation_date_before = QDateEdit()
        self.creation_date_before.setCalendarPopup(True)
        self.creation_date_before.setDate(QDate.currentDate().addDays(5))
        form_layout.addRow("Contract Create Before:", self.creation_date_before)
        
        def update_slider_from_lineedit(slider, lineedit):
            # Fonction de mise à jour dynamique entre les sliders et les LineEdits
            try:
                value = int(lineedit.text())
                slider.setValue(value)
            except ValueError:
                lineedit.setText(str(slider.value()))  # Remet la valeur actuelle si la saisie est incorrecte

        def update_lineedit_from_slider(slider, lineedit):
            lineedit.setText(str(slider.value()))

        # Connecte les sliders et les LineEdits 
        self.amount_due_min_slider.valueChanged.connect(lambda value: update_lineedit_from_slider(self.amount_due_min_slider, self.amount_due_min_lineedit))
        self.amount_due_min_lineedit.textChanged.connect(lambda: update_slider_from_lineedit(self.amount_due_min_slider, self.amount_due_min_lineedit))

        self.amount_due_max_slider.valueChanged.connect(lambda value: update_lineedit_from_slider(self.amount_due_max_slider, self.amount_due_max_lineedit))
        self.amount_due_max_lineedit.textChanged.connect(lambda: update_slider_from_lineedit(self.amount_due_max_slider, self.amount_due_max_lineedit))


        # Boutons pour appliquer ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.apply_filter)
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.exec()
    
    def apply_filter(self):
        """
        Applique les filtres et affiche la liste des contrats filtrés.
        """
        filter_data = {}

        # Récupérer les checkbox
        if self.status_checkbox.isChecked():
            filter_data['status'] = True
        if self.paid_radio.isChecked():
            filter_data['paid'] = True
        elif self.not_paid_radio.isChecked():
            filter_data['paid'] = False
        else:
            filter_data['paid'] = None
        
        filter_data['customer_id'] = self.customer_combobox.currentData()
        filter_data['amount_due_min'] = self.amount_due_min_slider.value()
        filter_data['amount_due_max'] = self.amount_due_max_slider.value()
        filter_data['creation_date_before'] = self.creation_date_before.date().toPython()
        filter_data['creation_date_after'] = self.creation_date_after.date().toPython()

        contracts = self.controller.contract_filter(filter_data)
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