import tkinter as tk
from tkinter import messagebox, ttk
from helpers.get_data import *
from views import *
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout ,QComboBox, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QGridLayout,QSpacerItem, QSizePolicy, QFormLayout

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

        widgets = [
            self.create_customer_button,
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
        
    # def create_widgets(self, row, column):
    #     """Créer les boutons dans la vue commerciale avec un positionnement dynamique."""

    #     # Liste des boutons et leurs commandes
    #     buttons = [
    #         ("Create Customer", self.create_customer_window),
    #         ("Update Customer", self.update_customer_window),
    #         ("Update Contract", self.update_contract_window),
    #         ("Contract Filter", self.contract_filter_window)
    #     ]

    #     for text, command in buttons:
    #         # Créer un bouton
    #         button = tk.Button(self.parent, text=text, command=command)
    #         button.grid(row=row, column=column, padx=5, pady=5)  # Placer le bouton à la position donnée
    #         column += 1
    #         if column > 3:
    #             column = 0
    #             row += 1

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



        # tk.Label(window, text="Customer Name:").grid(row=1, column=0, columnspan=2, pady=10)
        # name_entry = tk.Entry(window)
        # name_entry.grid(row=1, column=2, columnspan=2, pady=10)

        # tk.Label(window, text="Customer Email:").grid(row=2, column=0, columnspan=2, pady=10)
        # email_entry = tk.Entry(window)
        # email_entry.grid(row=2, column=2, columnspan=2, pady=10)

        # tk.Label(window, text="Company Name:").grid(row=3, column=0, columnspan=2, pady=10)
        # company_name_entry = tk.Entry(window)
        # company_name_entry.grid(row=3, column=2, columnspan=2, pady=10)

        # # Bouton pour soumettre les données
        # submit_button = tk.Button(window, text="Submit", 
        #                           command=lambda: self.create_customer(window, name_entry.get(), email_entry.get(), company_name_entry.get()))
        # submit_button.grid(row=4, column=1, columnspan=2, pady=10)

        # window.columnconfigure(1, weight=1)

    # def update_customer_window(self):
    #     window = tk.Toplevel(self)
    #     window.title = "Update Customer"
    #     customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
    #     customer_names = [customer["name"] for customer in customers]
        
    #     # Créer un label et une combobox pour les clients
    #     tk.Label(window, text="Select Customer:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    #     customer_combobox = ttk.Combobox(window, values=customer_names)
    #     customer_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    #     customer_combobox.set("Select a customer")  # Texte par défaut
        
    #     # Champ pour les informations mises à jour
    #     tk.Label(window, text="Update Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    #     email_entry = tk.Entry(window)
    #     email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    #     tk.Label(window, text="Update Company Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    #     company_name_entry = tk.Entry(window)
    #     company_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    #     # Bouton pour soumettre les changements
    #     submit_button = tk.Button(
    #         window, 
    #         text="Submit", 
    #         command=lambda: self.update_customer(
    #             window, 
    #             customer_combobox.get(), 
    #             email_entry.get(), 
    #             company_name_entry.get()
    #         )
    #     )
    #     submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    #     # S'assurer que la fenêtre est redimensionnable et que les colonnes s'ajustent
    #     window.columnconfigure(1, weight=1)

    # def update_contract_window(self):
    #     window = tk.Toplevel(self)
    #     window.title = 'Udpate Contract'

    #     customers = get_customers_commercial(self.controller.authenticated_user, self.controller.session)
    #     customer_names = [customer["name"] for customer in customers]

    #     # Créer un label et une combobox pour sélectionner un client
    #     tk.Label(window, text="Select Customer:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    #     customer_combobox = ttk.Combobox(window, values=customer_names)
    #     customer_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    #     customer_combobox.set("Select a customer")  # Texte par défaut

    #     tk.Label(window, text="Select Contract:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    #     contract_combobox = ttk.Combobox(window, values=[])
    #     contract_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    #     contract_combobox.set("Select a contract") 

    #     # Mise à jour dynamique des contrats lorsqu'un client est sélectionné
    #     def update_contracts(*args):
    #         selected_customer_name = customer_combobox.get()
    #         selected_customer = next((customer for customer in customers if customer["name"] == selected_customer_name), None)
            
    #         if selected_customer:
    #             # Récupérer les contrats pour le client sélectionné
    #             contracts = self.controller.session.query(Contract).filter_by(customer_id=selected_customer['id']).all()
    #             contract_names = [f"Contract ID: {contract.id} - Amount Due: {contract.amount_due}" for contract in contracts]
    #             contract_combobox['values'] = contract_names
    #             contract_combobox.set("Select a contract")

    #     customer_combobox.bind("<<ComboboxSelected>>", update_contracts)

    #     # Champ pour les informations mises à jour
    #     tk.Label(window, text="Update amount due:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    #     amount_due_entry = tk.Entry(window)
    #     amount_due_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    #     tk.Label(window, text="Update Remaining amount:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    #     remaining_amount_entry = tk.Entry(window)
    #     remaining_amount_entry .grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    #     tk.Label(window, text="Update Status (True/False):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    #     status_entry = tk.Entry(window)
    #     status_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    #     submit_button = tk.Button(
    #     window, 
    #     text="Submit", 
    #     command=lambda: self.update_contract(
    #         window, 
    #         contract_combobox.get(), 
    #         amount_due_entry.get(), 
    #         remaining_amount_entry.get(), 
    #         status_entry.get()
    #         )
    #     )
    #     submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    #     # S'assurer que la fenêtre est redimensionnable et que les colonnes s'ajustent
    #     window.columnconfigure(1, weight=1)


    # def contract_filter_window(self):
    #     window = tk.Toplevel(self)
    #     window.title = 'Contract filter'

    #     tk.Label(window, text="Select Filter:").grid(row=0, column=0, padx=10, pady=10)
    #     filter_options = ["status", "amount_due_greater", "amount_due_less", "remaining_amount_greater", "remaining_amount_less", "creation_date_before", "creation_date_after"]
    #     self.filter_var = tk.StringVar(value="status")  # Variable pour stocker la sélection
    #     filter_menu = ttk.Combobox(window, textvariable=self.filter_var, values=filter_options)
    #     filter_menu.grid(row=0, column=1, padx=10, pady=10)

    #     # Champ pour entrer la valeur du filtre
    #     tk.Label(window, text="Filter Value:").grid(row=1, column=0, padx=10, pady=10)
    #     self.filter_value_entry = tk.Entry(window)
    #     self.filter_value_entry.grid(row=1, column=1, padx=10, pady=10)
        
    #     # Bouton pour appliquer le filtre
    #     apply_filter_button = tk.Button(window, text="Apply Filter", command=self.apply_contract_filter)
    #     apply_filter_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # def apply_contract_filter(self):
    #     """Applique le filtre de contrat sélectionné."""
    #     filter_type = self.filter_var.get() 
    #     filter_value = self.filter_value_entry.get()  

    #     if filter_type in ["amount_due_greater", "amount_due_less", "remaining_amount_greater", "remaining_amount_less"]:
    #         try:
    #             filter_value = int(filter_value)
    #         except ValueError:
    #             messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
    #             return

    #     # Pour les dates, tu pourrais utiliser un `DatePicker` ou forcer un format particulier
    #     # On pourrait convertir la chaîne en objet date si nécessaire (par ex. datetime.strptime)
        
    #     # Applique le filtre via le contrôleur
    #     contracts = self.controller.contract_filter(filter_type, filter_value)
    #     if contracts:
    #         # Afficher le résultat dans une nouvelle fenêtre
    #         result_window = tk.Toplevel(self)
    #         result_window.title("Filtered Contracts")
    #         for i, contract in enumerate(contracts):
    #             tk.Label(result_window, text=f"Contract ID: {contract.id}, Amount Due: {contract.amount_due}, Status: {contract.status}").grid(row=i, column=0, padx=10, pady=5)
    #     else:
    #         messagebox.showinfo("No Results", "No contracts found matching the filter.")

    # def create_customer(self, window, name, email, company_name):
    #     customer_data = {
    #         'name': name,
    #         'email': email,
    #         'company_name': company_name,
    #     }
    #     try:
    #         new_customer = self.controller.create_customer(**customer_data)
    #         messagebox.showinfo("Success", f"Customer '{new_customer.name}' created successfully.")
    #         window.destroy()  # Fermer la fenêtre après succès
    #     except PermissionError as e:
    #         messagebox.showerror("Permission Denied", str(e))

    # def update_customer(self, window, customer_name, email, company_name):
    #     customer_data = {
    #         'email': email,
    #         'company_name': company_name,
    #     }
    #     try:
    #         updated_customer = self.controller.update_customer(customer_name, **customer_data)
    #         if updated_customer:
    #             messagebox.showinfo("Success", f"Customer '{updated_customer.name}' updated successfully.")
    #             window.destroy()  # Fermer la fenêtre après succès
    #         else:
    #             messagebox.showerror("Error", "Customer not found.")
    #     except PermissionError as e:
    #         messagebox.showerror("Permission Denied", str(e))

    # def update_contract(self, window, selected_contract, amount_due, remaining_amount, status):
    #     contract_id = selected_contract.split()[2]  
    #     contract = self.controller.session.query(Contract).filter_by(id=contract_id).first()
        
    #     if contract:
    #         if amount_due:
    #             contract.amount_due = int(amount_due)
    #         if remaining_amount:
    #             contract.remaining_amount = int(remaining_amount)
    #         if status:
    #             contract.status = status.lower() == 'true'
            
    #         self.controller.session.commit()
    #         messagebox.showinfo("Success", "Contract updated successfully.")
    #         window.destroy()  # Fermer la fenêtre après succès
    #     else:
    #         messagebox.showerror("Error", "Contract not found.")






    