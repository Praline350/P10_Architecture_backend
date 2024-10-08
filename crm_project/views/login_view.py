import sys

import tkinter as tk
from tkinter import messagebox


from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QCalendarWidget,
    QLabel,
    QPushButton,
    QCheckBox,
    QSpinBox,
    QLCDNumber,
    QLineEdit,
    QSlider,
    QProgressBar,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFormLayout,
    QMessageBox,
)


class LoginWidget(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.main_window = main_window
        self.controller = controller

        self.setup_widgets()

    def setup_widgets(self):
        master_layout = QVBoxLayout()
        master_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        form_layout = QFormLayout()

        self.username_label = QLabel("Username :")
        self.username_entry = QLineEdit()

        self.employee_number_label = QLabel("Employee Number :")
        self.employee_number_entry = QLineEdit()

        self.password_label = QLabel("Password :")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)

        widgets = [
            self.username_label,
            self.username_entry,
            self.employee_number_label,
            self.employee_number_entry,
            self.password_label,
            self.password_entry,
            self.login_button,
        ]
        for widget in widgets:
            widget.setObjectName("login")
            form_layout.addWidget(widget)
        master_layout.addLayout(form_layout)
        master_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self.setLayout(master_layout)

    def login_user(self):
        username = self.username_entry.text()
        employee_number = self.employee_number_entry.text()
        password = self.password_entry.text()

        try:
            user = self.controller.login(username, employee_number, password)
            if user:
                print("Login successful!")
                self.controller.show_frame(user)
            else:
                QMessageBox.information(
                    self, "Error", "Username, employee number or password invalid"
                )
                print("Login failed.")
        except ValueError as e:
            QMessageBox.information(
                self, "Error", "Username, employee number or password invalid"
            )
            raise ValueError(f"Error {e}")
