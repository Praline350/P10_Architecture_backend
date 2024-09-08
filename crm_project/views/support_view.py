import tkinter as tk
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SupportView(tk.Frame):
    def __init__(self, main_window, controller):
        super().__init__()
        self.controller = controller
        self.authenticated_user = controller.authenticated_user
        self.controller = controller
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Support Dashboard"))
        self.setLayout(layout)
        tk.Label(self, text="Support Dashboard", font=("Helvetica", 16)).pack(pady=20)
