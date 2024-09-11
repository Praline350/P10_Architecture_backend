# Methods for create windows, dialog and widgets :

from datetime import datetime, timedelta

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout ,QComboBox, QLineEdit, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGridLayout,
                               QSpacerItem, QSizePolicy, QFormLayout, QCheckBox,
                               QSlider, QDateEdit, QTableWidget, QTableWidgetItem,
                               QRadioButton
                               )


def mk_create_dialog_window(self, title):
    # Créer la fenêtre modale
    self.dialog = QDialog(self)
    self.dialog.setWindowTitle(title)
    self.form_layout = QFormLayout()


def mk_create_combox_id_name(self, items, display_names, obj_name):
    """
        Créer une combobox avec le nom et l'id de l'objet.
        L'ajoute au layout, retourne l'id dans current_data()
    """
    self.data_dict = {}
    self.combobox = QComboBox()
    for item, display_name in zip(items, display_names):
        self.combobox.addItem(display_name, item.id)
        self.data_dict[item.id] = item 
    self.form_layout.addRow(f"Select {obj_name}:", self.combobox)



def mk_create_edit_lines(self, fields_dict):
    """
        Créer dynamiquement des lineEdit avec le label
        fields_dict : Nom du champ et son label à afficher   
    """
    self.field_entries = {}
    for field_name, field_label in fields_dict.items():
        entry = QLineEdit()
        self.form_layout.addRow(field_label, entry)
        self.field_entries[field_name] = entry


def mk_create_date(self, date_value):
    """
    Crée un QDateEdit pour un champ de date.
    :param date_value: Valeur de date initiale (datetime).
    :return: QDateEdit widget.
    """
    self.date_edit = QDateEdit()
    self.date_edit.setCalendarPopup(True)  # Affiche le calendrier popup
    if isinstance(date_value, datetime.datetime):
        self.date_edit.setDate(date_value.date())  # Définit la date si valide
    else:
        self.date_edit.setDate(QDate.currentDate())  # Définit la date actuelle par défaut


def mk_create_checkbox(self, title, checked):
    """
    Crée un QCheckBox pour un champ booléen (statut).
    """
    self.checkbox = QCheckBox()
    self.checkbox.setChecked(checked)
    self.form_layout.addRow(title, self.checkbox)




    # Fonction pour mettre à jour les champs de texte avec les données de l'élément sélectionné
def mk_update_fields(self):
    self.selected_id = self.combobox.currentData()
    selected_data = self.data_dict.get(self.selected_id)
    # Debug
    print("Selected contract ID:", self.selected_id)
    print("Selected contract:", selected_data)
    print("Field entries:", self.field_entries)
    # Préremplir les champs avec les informations du client
    for field_name, entry in self.field_entries.items():
        # Utiliser getattr pour accéder aux attributs de l'objet
        if isinstance(entry, QLineEdit):
            value = getattr(selected_data, field_name, '')
            print(f"Updating field {field_name} with value:", value)  # Debug
            entry.setText(str(value))
        elif isinstance(entry, QCheckBox):
            # Utiliser getattr pour obtenir un booléen
            value = getattr(selected_data, field_name, False)
            if not isinstance(value, bool):
                value = bool(value)  # Convertir en bool si nécessaire
            print(f"Updating checkbox {field_name} with value:", value)  # Debug
            entry.setChecked(value)  # Mettre à jour les QCheckBox


def mk_create_dialog_button(self, method, **data):
    self.button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    self.button.accepted.connect(lambda: method(**data))
    self.button.rejected.connect(self.dialog.reject)
    self.form_layout.addWidget(self.button)