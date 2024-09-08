import tkinter as tk
from tkinter import messagebox, ttk
from crm_project.views import *
from crm_project.helpers.get_data import *
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout ,QComboBox, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QGridLayout,QSpacerItem, QSizePolicy, QFormLayout

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

        self.create_user_button = QPushButton("Creare New Employee")
        self.create_user_button.clicked.connect(self.create_user_window)

        widgets = [
            self.create_user_button, self.create_contract_button
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


    def create_contract_window(self):
        """
        Ouvre une fenêtre modale pour créer un contrat.
        """
        # Fenêtre modale pour créer un contrat
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Contract")

        # Création du layout pour la fenêtre de création de contrat
        form_layout = QFormLayout()

        # Liste déroulante des clients
        customers_info = get_customers_complet_name(self.controller.session)
        customer_combobox = QComboBox()
        if customers_info:
            for customer in customers_info:
                customer_combobox.addItem(customer['name'], customer['id']) 
        form_layout.addRow("Select Customer:", customer_combobox)

        # Champs de saisie pour les montants
        amount_due_entry = QLineEdit()
        form_layout.addRow("Amount due:", amount_due_entry)

        remaining_amount_entry = QLineEdit()
        form_layout.addRow("Remaining amount:", remaining_amount_entry)

        contract_data = {
            'amount_due': amount_due_entry.text(),
            'remaining_amount': remaining_amount_entry.text(),
        }

        # Boutons pour soumettre ou annuler
        customer =  customer_combobox.currentData()
        print(customer)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.create_contract(dialog, customer,**contract_data))
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        # Appliquer le layout à la fenêtre modale
        dialog.setLayout(form_layout)
        dialog.exec()

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

        employee_number_entry = QLineEdit()
        form_layout.addRow("Employee Number:", employee_number_entry)

        email_entry = QLineEdit()
        form_layout.addRow("Email:", email_entry)

        roles = get_roles_list()
        roles_combobox = QComboBox()
        if roles:
            for role in roles:
                roles_combobox.addItem(role)
        form_layout.addRow("Select Role:", roles_combobox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        def submit_user_data():
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



    def create_contract(self, dialog, customer, **contract_data):
        """
        Crée un contrat avec les données fournies.
        """
        try:
            # Logique pour créer le contrat via le contrôleur
            new_contract = self.controller.create_contract(customer, **contract_data)
            QMessageBox.information(self, "Success", "Contract created successfully.")
            dialog.accept()  # Ferme la fenêtre après succès
        except PermissionError as e:
            QMessageBox.warning(self, "Permission Denied", str(e))

        
        
        
    #     self.parent = parent
    #     authenticated_user = self.controller.authenticated_user
    #     if authenticated_user.role.name.value is not 'ADMIN':
    #         self.create_widgets(row=0, column=0)
    #         tk.Label(self,
    #                 text=f"Management Dashboard, Welcome {authenticated_user.first_name} {authenticated_user.last_name}",
    #                 font=("Helvetica", 16)
    #                 ).grid(row=1, column=0, columnspan=2, pady=10)

    
    # def create_widgets(self, row, column):
    #     # Bouton pour ouvrir la fenêtre de création de client
    #     self.create_contract_button = tk.Button(self.parent, text="Create Contract", command=self.create_contract_window)
    #     self.create_contract_button.grid(row=row, column=column)

    
    # def create_contract_window(self):
    #     window = tk.Toplevel(self)
    #     window.title("Create Contract")
    #     customers = get_customers_list(self.controller.session)
    #     customer_names = [customer["name"] for customer in customers]

    #     # Choix du client 
    #     tk.Label(window, text="Select Customer:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    #     customer_combobox = ttk.Combobox(window, values=customer_names)
    #     customer_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    #     customer_combobox.set("Select a customer")

    #     # choix montant 
    #     tk.Label(window, text="Amount due").grid(row=1, column=0, columnspan=2, pady=10)
    #     amount_due_entry = tk.Entry(window)
    #     amount_due_entry.grid(row=1, column=2, columnspan=2, pady=10)

    #     # choix montant encore due
    #     tk.Label(window, text="Remaining amount").grid(row=2, column=0, columnspan=2, pady=10)
    #     remaining_amount_entry = tk.Entry(window)
    #     remaining_amount_entry.grid(row=2, column=2, columnspan=2, pady=10)


    #     # Bouton pour soumettre les données
    #     submit_button = tk.Button(
    #         window,
    #         text="Submit", 
    #         command=lambda: self.create_contract(
    #             window,
    #             customer_combobox.get(),
    #             amount_due_entry.get(),
    #             remaining_amount_entry.get()
    #             )
    #         )
    #     submit_button.grid(row=4, column=1, columnspan=2, pady=10)

    #     window.columnconfigure(1, weight=1)

    # def create_contract(self, window, customer, amount_due, remaining_amount):
    #     contract_data = {
    #         'amount_due': amount_due,
    #         'remaining_amount': remaining_amount,
    #     }
    #     try:
    #         new_contract = self.controller.create_contract(customer, **contract_data)
    #         messagebox.showinfo("Success", f"Contract created successfully.")
    #         window.destroy()  # Fermer la fenêtre après succès
    #     except PermissionError as e:
    #         messagebox.showerror("Permission Denied", str(e))
