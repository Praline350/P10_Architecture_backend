# Methods for create windows, dialog and widgets :

import datetime

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout ,QComboBox, QLineEdit, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGridLayout,
                               QSpacerItem, QSizePolicy, QFormLayout, QCheckBox,
                               QSlider, QDateEdit, QTableWidget, QTableWidgetItem,
                               QRadioButton, QButtonGroup, QGroupBox
                               )


def mk_setup_widgets(self, layout, grid, columns, widgets):
    for index, widget in enumerate(widgets):
        row = index // columns
        column = index % columns
        grid.addWidget(widget, row, column)
        widget.setObjectName('management_buttons')
        layout.addLayout(grid)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

def mk_create_dialog_window(parent, title):
    # Créer la fenêtre modale
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    return dialog


def mk_create_combox_id_name(self, items, display_names, obj_name):
    """
        Créer une combobox avec le nom et l'id de l'objet.
        L'ajoute au layout, retourne l'id dans current_data()
        :self.data_dict:  associe les id au items
    """
    self.data_dict = {}
    self.combobox = QComboBox()
    for item, display_name in zip(items, display_names):
        self.combobox.addItem(display_name, item.id)
        self.data_dict[item.id] = item 
    self.form_layout.addRow(f"Select {obj_name}:", self.combobox)

def mk_display_current_item(label, item):
    info_text = "<ul>"
    if item:
        for key, value in item.items():
            info_text += f"<li><b><u>{key}</u>:</b>     {value}</li>"
        info_text += f"</ul>"
    else:
        info_text = f"{item} Info: No {item} selected"
    label.setText(info_text)

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
    return self.field_entries


def mk_create_dateedit(self, label, initial_date):
    """
    Crée un QDateEdit pour un champ de date.
    :param date_value: Valeur de date initiale (datetime).
    :return: QDateEdit widget.
    """
    date_edit = QDateEdit()
    date_edit.setCalendarPopup(True)  # Permet d'afficher un calendrier
    date_edit.setDate(initial_date)

    # Ajouter au formulaire avec le label
    self.form_layout.addRow(label, date_edit)

    # Retourner le QDateEdit pour une utilisation future
    return date_edit # Définit la date actuelle par défaut


def mk_create_checkbox(self, title, checked):
    """
    Crée un QCheckBox pour un champ booléen (statut).
    """
    self.checkbox = QCheckBox()
    self.checkbox.setChecked(checked)
    self.form_layout.addRow(title, self.checkbox)


def mk_update_fields(self):
    # Fonction pour mettre à jour les champs de texte avec les données de l'élément sélectionné

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


def mk_create_radio_buttons(self, field_dict, checked_key=None):
    self.radio_button_entries = {}
    for field_name, options in field_dict.items():
        radio_group = QButtonGroup(self)
        radio_layout = QVBoxLayout()
        group_box = QGroupBox(field_name.capitalize())
        group_box.setLayout(radio_layout)

        for option in options:
            radio_button = QRadioButton(option)
            radio_group.addButton(radio_button)

            if option == checked_key:
                radio_button.setChecked(True)
            radio_layout.addWidget(radio_button)
        self.form_layout.addRow(group_box)
        self.radio_button_entries[field_name] = radio_group
        print(self.radio_button_entries)

def get_selected_radio_value(self, field_name):
    """
    Récupère la valeur sélectionnée dans un groupe de boutons radio.
    :param field_name: Nom du champ pour accéder au groupe de boutons radio.
    :return: Le texte du bouton sélectionné.
    """
    radio_group = self.radio_button_entries[field_name]
    checked_button = radio_group.checkedButton()  # Récupérer le bouton sélectionné
    if checked_button:
        return checked_button.text()  # Retourne le texte du bouton sélectionné
    return None
        

def mk_create_slider_with_lineedit(self, label, min_value, max_value, initial_value):
    # Créer le slider
    slider = QSlider(Qt.Horizontal)
    slider.setRange(min_value, max_value)
    slider.setValue(initial_value)

    # Créer le QLineEdit associé
    lineedit = QLineEdit(str(initial_value))
    lineedit.setFixedWidth(60)

    # Layout pour le slider et le QLineEdit
    slider_layout = QHBoxLayout()
    slider_layout.addWidget(slider)
    slider_layout.addWidget(lineedit)

    # Ajouter le label et le layout au formulaire
    self.form_layout.addRow(label, slider_layout)

    # Connecter le slider et le QLineEdit
    def update_slider_from_lineedit():
        try:
            value = int(lineedit.text())
            slider.setValue(value)
        except ValueError:
            lineedit.setText(str(slider.value()))  # Remettre la valeur actuelle si la saisie est incorrecte

    def update_lineedit_from_slider(value):
        lineedit.setText(str(value))

    slider.valueChanged.connect(update_lineedit_from_slider)
    lineedit.textChanged.connect(update_slider_from_lineedit)

    # Retourner le slider et le QLineEdit pour une gestion future
    return slider, lineedit

def mk_create_table(labels_list, items, attributes_list):
    table = QTableWidget()
    table.setColumnCount(len(labels_list))
    table.setHorizontalHeaderLabels(labels_list)
    table.setRowCount(len(items))
        # Remplir le tableau avec les données des objets
    for row_idx, item in enumerate(items):
        for col_idx, attribute in enumerate(attributes_list):
            # Utiliser getattr pour obtenir la valeur de l'attribut
            value = getattr(item, attribute, "")
            
            # Si c'est un objet de type date, on le formate
            if isinstance(value, (datetime.date, datetime.datetime)):
                value = value.strftime('%Y-%m-%d')

            # Si c'est un objet lié (comme commercial_contact), on gère différemment
            elif isinstance(value, object) and hasattr(value, 'first_name') and hasattr(value, 'last_name'):
                value = f"{value.first_name} {value.last_name}"

            # Ajouter l'élément au tableau
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    table.resizeColumnsToContents()
    return table

def mk_create_table_window(self, title, header, table):
    self.dialog = QDialog(self)
    self.dialog.setWindowTitle(title)
    layout = QVBoxLayout()
    header = QLabel(header)
    header.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(header)
    layout.addWidget(table)
    close_button = QPushButton("Close")
    close_button.clicked.connect(self.dialog.accept)
    layout.addWidget(close_button)
    self.dialog.setLayout(layout)
    self.dialog.resize(850,400)  # Dimensionner la fenêtre à 600x400 pixels
    self.dialog.exec()

