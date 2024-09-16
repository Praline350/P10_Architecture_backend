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


# Methods de création de fenêtres

def mk_setup_widgets(parent, layout, grid, columns, widgets):
    """
        Setup widgets on the layout's grid
        args :
            parent : Fenêtre parent (QWidget)
            layout : Object QLayout (or child)
            grid : Object QGrid
            widgets: List of widgets
    """
    for index, widget in enumerate(widgets):
        row = index // columns
        column = index % columns
        grid.addWidget(widget, row, column)
        widget.setObjectName('management_buttons')
        layout.addLayout(grid)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        parent.setLayout(layout)

def mk_create_dialog_window(parent, title):
    """
        Create a dialog window on the parent window
        args :
            parent : Objects QWidget
            title : String : 
        return :
            Object QDialog    
    """
    # Créer la fenêtre modale
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    return dialog


def mk_create_combox_id_name(parent, layout, items, display_names, obj_name):
    """
        Make a combobox of items and add it to the layout
        args:
            layout: Object Qlayout
            items: Objects List
            display_names : String List
            obj_name: String
        return:
            data_dict : Dict of field, value to the selected item
            combobox: Object Qcombobox
    """
    data_dict = {}
    combobox = QComboBox()
    for item, display_name in zip(items, display_names):
        combobox.addItem(display_name, item.id)
        data_dict[item.id] = item 
    layout.addRow(f"Select {obj_name}:", combobox)
    return data_dict, combobox

def mk_display_current_item(label, item):
    """
        Display values of item in a label
    """
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
        Create a dynamic multi edit line fields
        args:
            fields_dict : dict : {'field_name':'Field Label'}
        return:
            Dict of field_name and entries of editline 
    """
    field_entries = {}
    for field_name, field_label in fields_dict.items():
        entry = QLineEdit()
        layout.addRow(field_label, entry)
        field_entries[field_name] = entry
    return field_entries


def mk_create_dateedit(self, layout, label, initial_date):
    """
        Create a QDateEdit
    """
    date_edit = QDateEdit()
    date_edit.setCalendarPopup(True) 
    date_edit.setDate(initial_date)
    layout.addRow(label, date_edit)

    return date_edit 


def mk_create_checkbox(self, layout, title, checked):
    """
        Create a checkbox
    """
    checkbox = QCheckBox()
    checkbox.setChecked(checked)
    layout.addRow(title, checkbox)
    return checkbox


def mk_update_fields(parent, combobox, data_dict, field_entries):
    """
        Update fields of parent form with selected item_combobox values 
        args:
            combobox : obj Qcombobox with items who want select
            data_dict : dict with fields, values of item, return of combobox maker
            field_entries: dict of fields to update
        return :
            ID of selected item
    """

    selected_id = combobox.currentData()
    selected_data = data_dict.get(selected_id)

    for field_name, entry in field_entries.items():
        # process according to object type
        if isinstance(entry, QLineEdit):
            value = getattr(selected_data, field_name, '')
            entry.setText(str(value))
        elif isinstance(entry, QCheckBox):
            value = getattr(selected_data, field_name, False)
            if not isinstance(value, bool):
                value = bool(value)
            entry.setChecked(value)
        elif isinstance(entry, QDateEdit):
            # Msut be`datetime.date` or `datetime.datetime` object)
            value = getattr(selected_data, field_name, None)
            if value:
                entry.setDate(value)
            else:

                entry.setDate(QDate.currentDate())
        elif isinstance(entry, QComboBox):
            value = getattr(selected_data, field_name, '')
            if value:
                index = entry.findText(str(value))  # Get index by the text
                if index >= 0:
                    entry.setCurrentIndex(index)
                else:
                    print(f"Value '{value}' not found in QComboBox {field_name}")
            else:
                entry.setCurrentIndex(-1)
    return selected_id


def mk_create_radio_buttons(self, layout,  field_dict, checked_key=None):
    """
        Create group of radio buttons
        args:
            field_dict: dict : {'field_name': ['option1', 'option2']}
        return:
            : dict : 
    """
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
        Get value of radio buttons
        args:
            radio_buttons_entrie: dict :
            field_name: str : field name for radio buttons access
        return:
            : str : selected button text
    """
    radio_group = radio_button_entries[field_name]
    checked_button = radio_group.checkedButton() 
    if checked_button:
        return checked_button.text()  
    return None
        

def mk_create_slider_with_lineedit(self, layout,  label, min_value, max_value, initial_value):
    """
        Create a slider with his line edit & connect their values to each other
        return:
            obj QSlider, obj QLineEdit
    """
    slider = QSlider(Qt.Horizontal)
    slider.setRange(min_value, max_value)
    slider.setValue(initial_value)

    lineedit = QLineEdit(str(initial_value))
    lineedit.setFixedWidth(60)

    slider_layout = QHBoxLayout()
    slider_layout.addWidget(slider)
    slider_layout.addWidget(lineedit)
    layout.addRow(label, slider_layout)

    def update_slider_from_lineedit():
        try:
            value = int(lineedit.text())
            slider.setValue(value)
        except ValueError:
            lineedit.setText(str(slider.value()))  

    def update_lineedit_from_slider(value):
        lineedit.setText(str(value))
    slider.valueChanged.connect(update_lineedit_from_slider)
    lineedit.textChanged.connect(update_slider_from_lineedit)
    return slider, lineedit

def mk_create_table(labels_list, items, attributes_list):
    """
        Create a QTable for item
        args:
            labels_list: str list : Name of tabel
            items: obj list : 
            attributes_list: str list: name of field to want display
        return 
            obj QTable
    """
    table = QTableWidget()
    table.setColumnCount(len(labels_list))
    table.setHorizontalHeaderLabels(labels_list)
    table.setRowCount(len(items))
    for row_idx, item in enumerate(items):
        for col_idx, attribute in enumerate(attributes_list):
            value = getattr(item, attribute, "")
            if isinstance(value, (datetime.date, datetime.datetime)):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(value, object) and hasattr(value, 'first_name') and hasattr(value, 'last_name'):
                value = f"{value.first_name} {value.last_name}"

            table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    table.resizeColumnsToContents()
    return table

def mk_create_table_window(self, title, header, table):
    """
        Create dialog window for obj QTable
        args:
            title: str : title of dialog window
            header: str : title of a table
            table: obj QTable : 
        return: 
            obj QDialog
    """
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

