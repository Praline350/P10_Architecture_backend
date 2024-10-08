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
