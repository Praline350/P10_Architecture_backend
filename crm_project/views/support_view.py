from crm_project.views.widget_maker import *
from crm_project.views import *
from crm_project.views.sharing_view import (
    filter_event_window,
    update_event_window,
)
from crm_project.helpers.get_data import *
from crm_project.project.permissions import (
    view_authenticated_user,
    decorate_all_methods,
)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
)


@decorate_all_methods(view_authenticated_user)
class SupportView(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.authenticated_user = controller.authenticated_user
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        layout = QVBoxLayout()

        welcome_label = QLabel(
            f"Support Dashboard, Welcome {self.authenticated_user.full_name}"
        )
        welcome_label.setStyleSheet("font-size: 16px; font-family: Helvetica;")
        welcome_label.setObjectName("label_titre")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        grid = QGridLayout()

        self.update_event_button = QPushButton("Update an Event")
        self.update_event_button.clicked.connect(self.open_update_event_dialog)

        self.filter_event_button = QPushButton("Filter Events")
        self.filter_event_button.clicked.connect(self.open_filter_event_dialog)

        widgets = [self.update_event_button, self.filter_event_button]
        columns = 2

        mk_setup_widgets(self, layout, grid, columns, widgets)

    def open_update_event_dialog(self):
        dialog = mk_create_dialog_window(self, "Update an Event")
        update_event_window(self, dialog)

    def open_filter_event_dialog(self):
        dialog = mk_create_dialog_window(self, "Filter Events")
        filter_event_window(self, dialog)
