import tkinter as tk
from tkinter import messagebox
from crm_project.views import *
from crm_project.controllers import *
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AdminView(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.authenticated_user = controller.authenticated_user
        self.controller = controller
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Admin Dashboard"))
        self.setLayout(layout)







    #     tk.Label(self,
    #             text=f"Admin Dashboard, Welcome {self.authenticated_user.first_name} {self.authenticated_user.last_name}",
    #             font=("Helvetica", 16)
    #             ).grid(row=0, column=0, columnspan=3, pady=20)
    #     # Créer les boutons pour les différentes actions commerciales
    #     self.create_all_widgets()

    #     # Ajoute ici d'autres méthodes pour gérer les boutons des autres vues (Support, Management, etc.)

    # def create_all_widgets(self):
    #     """Créer les boutons pour les actions commerciales dans l'AdminView."""
    #     # Créer une instance de CommercialController et CommercialView
    #     commercial_controller = CommercialController(self.controller.session, self.authenticated_user, self.controller)
    #     commercial_view = CommercialView(self, commercial_controller) 
    #     management_controller = ManagementController(self.controller.session, self.authenticated_user, self.controller)
    #     management_view  = ManagementView(self, management_controller)


    #     commercial_view.create_widgets()
    #     management_view.create_widgets()
    
