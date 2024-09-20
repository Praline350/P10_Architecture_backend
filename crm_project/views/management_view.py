
from crm_project.views.widget_maker import * 
from crm_project.views import *
from crm_project.views.sharing_view import update_contract_window, filter_event_window, update_event_window
from crm_project.helpers.get_data import *
from crm_project.project.permissions import view_authenticated_user, decorate_all_methods

from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout ,QComboBox, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QGridLayout,QSpacerItem, QSizePolicy, QFormLayout


# @decorate_all_methods(view_authenticated_user)
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

        self.filter_event_button = QPushButton("Filter Event")
        self.filter_event_button.clicked.connect(self.open_filter_event_dialog)

        self.update_event_button = QPushButton("Update an Event")
        self.update_event_button.clicked.connect(self.open_update_event_dialog)

        widgets = [
            self.create_user_button, self.create_contract_button,
            self.update_user_button, self.delete_user_button,
            self.update_contract_button, self.update_event_button,
            self.filter_event_button
        ]
        columns = 2

        mk_setup_widgets(self, layout, grid, columns, widgets)

    
    def open_update_contract_dialog(self):
        dialog = mk_create_dialog_window(self, 'Update a contract')
        update_contract_window(self, dialog)

    def open_filter_event_dialog(self):
        dialog = mk_create_dialog_window(self, "Filter Events")
        filter_event_window(self,  dialog)

    def open_update_event_dialog(self):
        dialog = mk_create_dialog_window(self, "Update an Event")
        update_event_window(self, dialog)


    def create_contract_window(self):
        """
        Ouvre une fenêtre modale pour créer un contrat.
        """
        dialog = mk_create_dialog_window(self, "Create a New Contract")
        form_layout = QFormLayout(self)
        # Liste déroulante des clients
        customers = get_customers_list(self.controller)
        display_names = get_display_customer_name(self.controller, customers)
        data_dict, customer_combobox = mk_create_combox_id_name(self,form_layout,  customers, display_names, "Customer")

        customer_info_label = QLabel()
        form_layout.addRow(customer_info_label) 
        customer_info_label.setObjectName('label_customer_info')

        customer_combobox.currentIndexChanged.connect(lambda index : self.on_customer_selection_changed(customer_info_label, customer_combobox, data_dict, index))
        selected_customer_id = customer_combobox.currentData()
        customer = data_dict.get(selected_customer_id)
        data = {
            'Email': customer.email,
            'Company': customer.company_name,
            'Commercial Contact': customer.commercial_contact.last_name,
        }
        mk_display_current_item(customer_info_label, data)

        fields_dict = {
            'amount_due': 'Amount due:',
            'remaining_amount': 'Remaining amount'
        }

        field_entries = mk_create_edit_lines(self,form_layout, fields_dict)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_contract(dialog, customer_combobox.currentData(),
            amount_due=field_entries['amount_due'].text(),
            remaining_amount=field_entries['remaining_amount'].text()
            ))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.open()
    
    def on_customer_selection_changed(self, label,  combobox, data_dict, index):
        # Récupérer l'ID du client sélectionné à partir de la combobox
        selected_customer_id = combobox.itemData(index)
        customer = data_dict.get(selected_customer_id)
        data = {
            'Email': customer.email,
            'Company': customer.company_name,
            'Commercial Contact': customer.commercial_contact.full_name,
        }
        if customer:
            mk_display_current_item(label, data)

    
    def create_contract(self, dialog, customer_id, **field_entries):
        """
        Crée un contrat avec les données fournies.
        """
        try:
            self.controller.create_contract(customer_id, **field_entries)
            QMessageBox.information(self, "Success", "Contract created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))


    def create_user_window(self):
        """
        Ouvre une fenêtre modale pour créer un utilisateur.
        """

        dialog = mk_create_dialog_window(self, "Create an New Employee")
        form_layout = QFormLayout()
        
        fields_dict = {
            'first_name':'First Name',
            'last_name': 'Last Name',
            'employee_number': 'Employee Number',
            'email': 'Email Contact',
        }
        field_entries = mk_create_edit_lines(self, form_layout, fields_dict)

        password_entry = QLineEdit()
        password_entry.setEchoMode(QLineEdit.Password)
        password_entry.setObjectName('password')
        form_layout.addRow("Password:", password_entry)
        confirm_password_entry = QLineEdit()
        confirm_password_entry.setEchoMode(QLineEdit.Password)
        confirm_password_entry.setObjectName('confirm_password')
        form_layout.addRow("Confirm Password:", confirm_password_entry)

        roles = get_roles_without_admin(self.controller)
        display_role_names = [role.name.value for role in roles]
        data_role_dict, roles_combobox = mk_create_combox_id_name(self, form_layout, roles, display_role_names, "Role")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setObjectName('buttons')

        def submit_user_data():
            if len(password_entry.text()) < 8:
                QMessageBox.warning(dialog, "Input Error", "New password must be at least 8 characters long.")
                return
            if password_entry.text() != confirm_password_entry.text():
                QMessageBox.warning(dialog, "Input Error", "Passwords do not match.")
                return
            user_data = {
                'first_name': field_entries['first_name'].text(),
                'last_name': field_entries['last_name'].text(),
                'password': password_entry.text(),
                'employee_number': field_entries['employee_number'].text(),
                'email': field_entries['email'].text(),
                'role': roles_combobox.currentText()        
            }
            self.create_user(dialog, **user_data )

       
        buttons.accepted.connect(submit_user_data)
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.open()

    def create_user(self, dialog, **user_data):
        """
        Crée un contrat avec les données fournies.
        """
        try:
            new_user = self.controller.create_user( **user_data)
            QMessageBox.information(self, "Success", f"User {new_user.last_name} {new_user.first_name} created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))

    def update_user_window(self):
        """
        Ouvre une fenêtre modale pour udpate un utilisateur.
        """
        dialog = mk_create_dialog_window(self, "Update an Employee")
        form_layout = QFormLayout()

        users = self.controller.get_users_without_authenticated_user()
        display_names = [user.full_name for user in users]
        data_dict, user_combobox = mk_create_combox_id_name(self, form_layout, users, display_names, "User")
        print(f"Utilisateurs disponibles pour la mise à jour: {display_names}")
        fields_dict = {
            'first_name':'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'employee_number': 'Employee Number',
            'email': 'Email Contact',
        }
        field_entries = mk_create_edit_lines(self, form_layout, fields_dict)
        roles = get_roles_without_admin(self.controller)
        display_role_names = [role.name.value for role in roles]
        print(f"Rôles disponibles: {display_role_names}")
        data_role_dict, roles_combobox = mk_create_combox_id_name(self, form_layout, roles, display_role_names, "Role")
        field_entries['role'] = roles_combobox

        user_combobox.currentIndexChanged.connect(lambda : mk_update_fields(self, user_combobox, data_dict, field_entries))
        user_id = mk_update_fields(self, user_combobox, data_dict, field_entries)
        
        # Boutons pour soumettre ou annuler
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setObjectName('buttons_updated')
        buttons.accepted.connect(lambda: self.update_user(
            dialog,
            user_combobox.currentData(),
            first_name=field_entries['first_name'].text(),
            last_name=field_entries['last_name'].text(),
            username=field_entries['username'].text(),
            employee_number=field_entries['employee_number'].text(),
            email=field_entries['email'].text(),
            role_id=field_entries['role'].currentData()
        ))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.open()

    def update_user(self, dialog, user_id, **user_data):
        try:
            updated_user = self.controller.update_user(user_id, **user_data)
            QMessageBox.information(self, "Success", f"{updated_user.last_name} {updated_user.first_name} updated successfully.")
            dialog.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))


    def delete_user_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update an Employee")
        users = self.controller.get_user_list()
        authenticated_user_id = self.controller.authenticated_user.id
        form_layout = QFormLayout()

        user_combobox = QComboBox()
        for user in users:
            if user['id'] != authenticated_user_id:
                user_name = f"{user['first_name']} {user['last_name']} - {user['id']}"
                user_combobox.addItem(user_name, user['id'])
        form_layout.addRow("Select Customer:", user_combobox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.confirm_delete_user(dialog, user_combobox))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        dialog.setLayout(form_layout)
        dialog.exec()

    def confirm_delete_user(self, dialog, combobox):
        selected_user_id = combobox.currentData()
        selected_user_name = combobox.currentText()
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







        
  