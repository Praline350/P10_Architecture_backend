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


def mk_create_combox_id_name(self, layout, items, display_names, obj_name):
    """
        Créer une combobox avec le nom et l'id de l'objet.
        L'ajoute au layout, retourne l'id dans current_data()
        :self.data_dict:  associe les id au items
    """
    data_dict = {}
    combobox = QComboBox()
    for item, display_name in zip(items, display_names):
        combobox.addItem(display_name, item.id)
        data_dict[item.id] = item 
    layout.addRow(f"Select {obj_name}:", combobox)
    return data_dict, combobox

def mk_display_current_item(label, item):
    info_text = "<ul>"
    if item:
        for key, value in item.items():
            info_text += f"<li><b><u>{key}</u>:</b>     {value}</li>"
        info_text += f"</ul>"
    else:
        info_text = f"{item} Info: No {item} selected"
    label.setText(info_text)

def mk_create_edit_lines(self, layout, fields_dict):
    """
        Créer dynamiquement des lineEdit avec le label
        fields_dict : Nom du champ et son label à afficher   
    """
    field_entries = {}
    for field_name, field_label in fields_dict.items():
        entry = QLineEdit()
        layout.addRow(field_label, entry)
        field_entries[field_name] = entry
    return field_entries


def mk_create_dateedit(self, layout, label, initial_date):
    """
    Crée un QDateEdit pour un champ de date.
    :param date_value: Valeur de date initiale (datetime).
    :return: QDateEdit widget.
    """
    date_edit = QDateEdit()
    date_edit.setCalendarPopup(True)  # Permet d'afficher un calendrier
    date_edit.setDate(initial_date)

    # Ajouter au formulaire avec le label
    layout.addRow(label, date_edit)

    # Retourner le QDateEdit pour une utilisation future
    return date_edit # Définit la date actuelle par défaut


def mk_create_checkbox(self, layout, title, checked):
    """
    Crée un QCheckBox pour un champ booléen (statut).
    """
    checkbox = QCheckBox()
    checkbox.setChecked(checked)
    layout.addRow(title, checkbox)
    return checkbox


def mk_update_fields(self, combobox, data_dict, field_entries):
    # Fonction pour mettre à jour les champs de texte avec les données de l'élément sélectionné

    selected_id = combobox.currentData()
    selected_data = data_dict.get(selected_id)
    # Debug
    print("Selected contract ID:", selected_id)
    print("Selected contract:", selected_data)
    print("Field entries:", field_entries)
    # Préremplir les champs avec les informations du client
    for field_name, entry in field_entries.items():
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
        elif isinstance(entry, QDateEdit):
            # Utiliser getattr pour obtenir une date (doit être un objet `datetime.date` ou `datetime.datetime`)
            value = getattr(selected_data, field_name, None)
            if value:
                print(f"Updating QDateEdit {field_name} with value:", value)  # Debug
                entry.setDate(value)
            else:
                print(f"Resetting QDateEdit {field_name} to current date")  # Debug
                entry.setDate(QDate.currentDate())  # Remettre à la date actuelle si pas de valeur

        elif isinstance(entry, QComboBox):
            # Utiliser getattr pour obtenir la valeur à sélectionner dans la QComboBox
            value = getattr(selected_data, field_name, '')
            print(f"Updating QComboBox {field_name} with value:", value)  # Debug
            if value:
                index = entry.findText(str(value))  # Rechercher l'index basé sur le texte
                if index >= 0:
                    entry.setCurrentIndex(index)
                else:
                    print(f"Value '{value}' not found in QComboBox {field_name}")
            else:
                entry.setCurrentIndex(-1)
    return selected_id


def mk_create_dialog_button(self, method, **data):
    self.button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    self.button.accepted.connect(lambda: method(**data))
    self.button.rejected.connect(self.dialog.reject)
    self.form_layout.addWidget(self.button)


def mk_create_radio_buttons(self, layout,  field_dict, checked_key=None):
    radio_button_entries = {}
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
        layout.addRow(group_box)
        radio_button_entries[field_name] = radio_group
    return radio_button_entries

def get_selected_radio_value(self, radio_button_entries, field_name):
    """
    Récupère la valeur sélectionnée dans un groupe de boutons radio.
    :param field_name: Nom du champ pour accéder au groupe de boutons radio.
    :return: Le texte du bouton sélectionné.
    """
    radio_group = radio_button_entries[field_name]
    checked_button = radio_group.checkedButton()  # Récupérer le bouton sélectionné
    if checked_button:
        return checked_button.text()  # Retourne le texte du bouton sélectionné
    return None
        

def mk_create_slider_with_lineedit(self, layout,  label, min_value, max_value, initial_value):
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
    layout.addRow(label, slider_layout)

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
    dialog = QDialog(self)
    dialog.setMinimumSize(900, 400)  # Taille minimale
    dialog.setMaximumSize(1200, 800) 
    dialog.setWindowTitle(title)
    layout = QVBoxLayout()
    header = QLabel(header)
    header.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(header)
    layout.addWidget(table)
    close_button = QPushButton("Close")
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)
    dialog.setLayout(layout)
    dialog.resize(950,400)  # Dimensionner la fenêtre à 600x400 pixels
    dialog.exec()
    return dialog

