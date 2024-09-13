
from crm_project.views.widget_maker import * 
from crm_project.views import *
from crm_project.views.main_view import *
from crm_project.helpers.get_data import *
from crm_project.project.permissions import view_authenticated_user, decorate_all_methods

from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout ,QComboBox, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QGridLayout,QSpacerItem, QSizePolicy, QFormLayout


decorate_all_methods(view_authenticated_user)
class ManagementView(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.authenticated_user = controller.authenticated_user
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        layout = QVBoxLayout()

        welcome_label = QLabel(f"Management Dashboard, Welcome {self.authenticated_user.first_name} {self.authenticated_user.last_name}")
        welcome_label.setStyleSheet("font-size: 16px; font-family: Helvetica;")
        welcome_label.setObjectName("label_titre")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        grid = QGridLayout()

        self.create_contract_button = QPushButton("Create Contract")
        self.create_contract_button.clicked.connect(self.create_contract_window)

        self.update_contract_button = QPushButton('Update a Contract')
        self.update_contract_button.clicked.connect(self.open_update_contract_dialog)

        self.create_user_button = QPushButton("Creare New Employee")
        self.create_user_button.clicked.connect(self.create_user_window)

        self.update_user_button = QPushButton("Update an Employee")
        self.update_user_button.clicked.connect(self.update_user_window)

        self.delete_user_button = QPushButton("Delete an Employee")
        self.delete_user_button.clicked.connect(self.delete_user_window)



        widgets = [
            self.create_user_button, self.create_contract_button,
            self.update_user_button, self.delete_user_button,
            self.update_contract_button
        ]
        columns = 2

        mk_setup_widgets(self, layout, grid, columns, widgets)

    
    def open_update_contract_dialog(self):
        dialog = mk_create_dialog_window(self, 'Update a contract')
        update_contract_window(self, dialog)


    def create_contract_window(self):
        """
        Ouvre une fenêtre modale pour créer un contrat.
        """
        dialog = mk_create_dialog_window(self, "Create a New Contract")
        self.form_layout = QFormLayout(self)
        # Liste déroulante des clients
        customers = get_customers_list(self.controller.session)
        display_names = get_display_customer_name(customers)
        mk_create_combox_id_name(self, customers, display_names, "Customer")

        self.customer_info_label = QLabel()
        self.form_layout.addRow(self.customer_info_label) 
        self.customer_info_label.setObjectName('label_customer_info')

        self.combobox.currentIndexChanged.connect(self.on_customer_selection_changed)
        selected_customer_id = self.combobox.currentData()
        customer = self.data_dict.get(selected_customer_id)
        data = {
            'Email': customer.email,
            'Company': customer.company_name,
            'Commercial Contact': customer.commercial_contact.last_name,
        }
        mk_display_current_item(self.customer_info_label, data)

        fields_dict = {
            'amount_due': 'Amount due:',
            'remaining_amount': 'Remaining amount'
        }
        mk_create_edit_lines(self, fields_dict)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_contract(dialog, 
            
            amount_due=self.field_entries['amount_due'].text(),
            remaining_amount=self.field_entries['remaining_amount'].text()
            ))
        buttons.rejected.connect(dialog.reject)
        self.form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(self.form_layout)
        dialog.exec()
    
    def on_customer_selection_changed(self, index):
        # Récupérer l'ID du client sélectionné à partir de la combobox
        selected_customer_id = self.combobox.itemData(index)
        customer = self.data_dict.get(selected_customer_id)
        data = {
            'Email': customer.email,
            'Company': customer.company_name,
            'Commercial Contact': customer.commercial_contact.name,
        }
        if customer:
            mk_display_current_item(self.customer_info_label, data)

    
    def create_contract(self, dialog, **field_entries):
        """
        Crée un contrat avec les données fournies.
        """
        try:
            customer = customer=self.combobox.currentData()
            self.controller.create_contract(customer, **field_entries)
            QMessageBox.information(self, "Success", "Contract created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))


    def create_user_window(self):
        """
        Ouvre une fenêtre modale pour créer un utilisateur.
        """
        # Fenêtre modale pour créer un contrat
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New User")

        # Création du layout pour la fenêtre de création de contrat
        form_layout = QFormLayout()

        first_name_entry = QLineEdit()
        form_layout.addRow("First Name:", first_name_entry)

        last_name_entry = QLineEdit()
        form_layout.addRow("Last Name:", last_name_entry)
        
        password_entry = QLineEdit()
        password_entry.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", password_entry)
        confirm_password_entry = QLineEdit()
        confirm_password_entry.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Confirm Password:", confirm_password_entry)

        employee_number_entry = QLineEdit()
        form_layout.addRow("Employee Number:", employee_number_entry)

        email_entry = QLineEdit()
        form_layout.addRow("Email:", email_entry)

        roles = get_roles_without_admin()
        roles_combobox = QComboBox()
        if roles:
            for role in roles:
                roles_combobox.addItem(role)
        form_layout.addRow("Select Role:", roles_combobox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        def submit_user_data():
            if len(password_entry.text()) < 8:
                QMessageBox.warning(dialog, "Input Error", "New password must be at least 8 characters long.")
                return
            if password_entry.text() != confirm_password_entry.text():
                QMessageBox.warning(dialog, "Input Error", "Passwords do not match.")
                return
            user_data = {
                'first_name': first_name_entry.text(),
                'last_name': last_name_entry.text(),
                'password': password_entry.text(),
                'employee_number': employee_number_entry.text(),
                'email': email_entry.text(),
                'role': roles_combobox.currentText()        
            }
            self.create_user(dialog, **user_data )

       
        buttons.accepted.connect(submit_user_data)
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.exec()


    def create_user(self, dialog, **user_data):
        """
        Crée un contrat avec les données fournies.
        """
        try:
            # Logique pour créer le contrat via le contrôleur
            new_user = self.controller.create_user( **user_data)
            QMessageBox.information(self, "Success", "User created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))

    def update_user_window(self):
        """
        Ouvre une fenêtre modale pour udpate un utilisateur.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Update an Employee")
        users = self.controller.get_user_list()
        form_layout = QFormLayout()

        user_combobox = QComboBox()
        user_data_dict = {}
        for user in users:
            user_name = f"{user['first_name']} {user['last_name']} - {user['id']}"
            user_combobox.addItem(user_name, user['id'])
            user_data_dict[user['id']] = user
        form_layout.addRow("Select Customer:", user_combobox)

        first_name_entry = QLineEdit()
        form_layout.addRow("First Name:", first_name_entry)

        last_name_entry = QLineEdit()
        form_layout.addRow("Last Name:", last_name_entry)

        username_entry = QLineEdit()
        form_layout.addRow("username:", username_entry)

        employee_number_entry = QLineEdit()
        form_layout.addRow("Employee Number:", employee_number_entry)

        email_entry = QLineEdit()
        form_layout.addRow("Email:", email_entry)


                # Fonction pour mettre à jour les champs de texte avec les données du client sélectionné
        def update_fields():
            selected_user_id = user_combobox.currentData()  # Obtenir l'ID de l'utilisateur sélectionné
            selected_user = user_data_dict.get(selected_user_id, {})  # Récupérer les données de l'utilisateur

            # Préremplir les champs avec les informations de l'utilisateur
            first_name_entry.setText(selected_user.get('first_name', ''))
            last_name_entry.setText(selected_user.get('last_name', ''))
            username_entry.setText(selected_user.get('username', ''))
            employee_number_entry.setText(str(selected_user.get('employee_number', '')))
            email_entry.setText(selected_user.get('email', ''))


        # Connecter l'événement de changement de sélection de la combobox à la fonction
        user_combobox.currentIndexChanged.connect(update_fields)
        update_fields()

        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.update_user(
            dialog,
            user_combobox.currentData(),
            first_name_entry.text(),
            last_name_entry.text(),
            username_entry.text(),
            employee_number_entry.text(),
            email_entry.text()
        ))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.exec()

    def update_user(self, dialog, user_id, first_name, last_name, username,  employee_number, email ):
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username, 
            'employee_number': employee_number,
            'email': email,
        }
        try:
            updated_user = self.controller.update_user(user_id, **user_data)
            QMessageBox.information(self, "Success", f"{user_data['last_name']} updated successfully.")
            dialog.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def delete_user_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update an Employee")
        users = self.controller.get_user_list()
        authenticated_user_id = self.controller.authenticated_user.id
        form_layout = QFormLayout()

        self.user_combobox = QComboBox()
        for user in users:
            if user['id'] != authenticated_user_id:
                user_name = f"{user['first_name']} {user['last_name']} - {user['id']}"
                self.user_combobox.addItem(user_name, user['id'])
        form_layout.addRow("Select Customer:", self.user_combobox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.confirm_delete_user(dialog))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.exec()

    def confirm_delete_user(self, dialog):
        selected_user_id = self.user_combobox.currentData()
        selected_user_name = self.user_combobox.currentText()
        confirmation = QMessageBox.question(
            self,
            'Confirm Delete User',
            f"Are you sure you want to delete the user {selected_user_name} ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirmation == QMessageBox.Yes:
            self.delete_user(dialog, selected_user_id)
        else:
            QMessageBox.information(dialog, 'Cancelled', 'User deletion cancelled')

    def delete_user(self,dialog, user_id):
        try:
            result_message = self.controller.delete_user(user_id)
            QMessageBox.information(dialog, "Success", result_message)
            dialog.accept()  # Ferme la fenêtre après suppression

        except ValueError as e:
            print(e)
            # Message personnalisé pour l'erreur d'intégrité des contrats liés
            QMessageBox.warning(
                dialog,
                "Error",
                "This user is associated with existing contracts. Please reassign the contracts before deleting the user."
                )







        
  