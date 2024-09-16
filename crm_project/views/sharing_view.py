from crm_project.helpers.get_data import *
from crm_project.views import *
from crm_project.views.widget_maker import *

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QHBoxLayout ,QComboBox, QLineEdit, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGridLayout,
                               QSpacerItem, QSizePolicy, QFormLayout, QCheckBox,
                               QSlider, QDateEdit, QTableWidget, QTableWidgetItem,
                               QRadioButton
                               )



def update_contract_window(self, dialog):
    """
    Ouvre une fenêtre modale pour mettre à jour un contrat.
    """
    form_layout = QFormLayout(self)
    # Fenêtre modale pour mettre à jour un client
    if self.controller.authenticated_user.role.name == 'COMMERCIAL':
        contracts = get_contract_commercial(self.controller.authenticated_user, self.controller.session)
    else:
        contracts = get_contracts_list(self.controller.session)
    display_names = [f"{contract.id} - {contract.customer.name}" for contract in contracts]

    data_dict, contract_combobox = mk_create_combox_id_name(self, form_layout,  contracts, display_names, "Contract")

    status_checkbox = mk_create_checkbox(self, form_layout, "Filter by Status (Active=Signed)", False)

    fields_dict = {
        'amount_due': 'Amount Due:',
        'remaining_amount': 'Remaining Amount:',
    }
    field_entries = mk_create_edit_lines(self,form_layout, fields_dict)
    field_entries['status'] = status_checkbox

    # Connecter l'événement de changement de sélection de la combobox à la fonction
    contract_combobox.currentIndexChanged.connect(lambda: mk_update_fields(self, contract_combobox, data_dict, field_entries))

    # Met a jour les champ en fonction du combobox et retourne le contract selectionné
    contract_id = mk_update_fields(self, contract_combobox, data_dict, field_entries)

    print(f"Contract _ id : {contract_id}")
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(lambda: update_contract(self, dialog, contract_id,
        amount_due=field_entries['amount_due'].text(),
        remaining_amount=field_entries['remaining_amount'].text(),
        status=field_entries['status'].isChecked() 
    ))
    buttons.rejected.connect(dialog.reject)
    form_layout.addWidget(buttons)

    # Appliquer le layout à la fenêtre modale
    dialog.setLayout(form_layout)
    dialog.exec()


def update_contract(self, dialog, contract_id, **field_entries):
    print(f"field entries :{field_entries}")
    try :
        print(f"contract id : {contract_id}")
        updated_contract = self.controller.update_contract(contract_id, **field_entries)
        print(f"new contract : {updated_contract.to_dict()}")
        QMessageBox.information(self, "Success", f"Contract {updated_contract.id} updated successfully.")
        dialog.accept()  # Ferme la fenêtre après succès
    except ValueError as e:
        print(e)
        QMessageBox.warning(self, "Error", str(e))
    except Exception as e:
        print(e)
        QMessageBox.critical(self, "Error", f"An error occurred: {e}")


def update_event_window(self, dialog):
    form_layout = QFormLayout()
    user = self.controller.authenticated_user
    if user.role.name.value != 'SUPPORT':
        events = get_events_list(self.controller.session)
        supports = get_support_user(self.controller.session)
        display_support_names = [support.full_name for support in supports]
        support_data_dict, support_combobox = mk_create_combox_id_name(self, form_layout, supports, display_support_names, 'Support Contact')
    else:
        events = get_events_support_list(self.controller.session, user.id)
        support_combobox = None

    display_events_names = [f"{event.name} - {event.contract.customer.name}" for event in events]
    event_data_dict, event_combobox = mk_create_combox_id_name(self, form_layout, events, display_events_names, 'Events')

    fields_dict = {
        'location': 'Location',
        'attendees': 'Attendees Number',
        'comment': 'Comment'
    }
    field_entries = mk_create_edit_lines(self, form_layout, fields_dict)
    start_date = mk_create_dateedit(self, form_layout, "Event Start Date", QDate.currentDate().addDays(0))
    end_date = mk_create_dateedit(self, form_layout, "Event End Date", QDate.currentDate().addDays(+1))
    field_entries['start_date'] = start_date.date().toPython()
    field_entries['end_date'] = end_date.date().toPython()

    event_id = mk_update_fields(self, event_combobox, event_data_dict, field_entries)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(lambda: update_event(self, dialog, event_id,
        location=field_entries['location'].text(),
        start_date=field_entries["start_date"],
        end_date=field_entries['end_date'],
        support_contact_id=user.id if user.role.name.value == 'SUPPORT' else support_combobox.currentData(),
        attendees=field_entries['attendees'].text(),
        comment=field_entries['comment'].text()
        ))
    buttons.rejected.connect(dialog.reject)
    form_layout.addWidget(buttons)

    # Appliquer le layout à la fenêtre modale
    dialog.setLayout(form_layout)
    dialog.exec()


def update_event(self, dialog, event_id, **field_entries):
    print(field_entries)
    try:
        updated_event = self.controller.update_event(event_id,**field_entries)
        QMessageBox.information(self, "Success", f"Event {updated_event.name} updated successfully.")
        dialog.accept()  # Ferme la fenêtre après succès
    except ValueError as e:
        print(e)
        QMessageBox.warning(self, "Error", str(e))
    except Exception as e:
        print(e)
        QMessageBox.critical(self, "Error", f"An error occurred: {e}")


def filter_event_window(self, dialog):
    """
        Ouvre une fenêtre modale pour update un evenement 
    """
    form_layout = QFormLayout()
    contracts = get_contracts_list(self.controller.session)
    display_names = [f"{contract.id} - {contract.customer.name}" for contract in contracts]
    data_dict, contract_combobox = mk_create_combox_id_name(self, form_layout, contracts, display_names, 'Contract')
    contract_combobox.addItem("All Contracts", None)
    if self.controller.authenticated_user.role.name.value == 'SUPPORT':
        support_checkbox = mk_create_checkbox(self, form_layout,
            "Only your associate events(Active=Yes)", checked=True)
    else:
        support_checkbox = mk_create_checkbox(self, form_layout,
            "Filter by associate support (Active=with associate Support)", checked=False)
    start_date_after = mk_create_dateedit(self, form_layout,
        "Event Start Date After:", QDate.currentDate().addDays(-5))
    start_date_before = mk_create_dateedit(self, form_layout,
        "Event Start Date Before:", QDate.currentDate().addDays(5))
    location_entry = QLineEdit()
    form_layout.addRow("Location :", location_entry)


    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(lambda : apply_event_filter(self, 
        combobox=contract_combobox,
        checkbox=support_checkbox,
        start_date_after=start_date_after,
        start_date_before=start_date_before,
        location=location_entry,
    ))
    buttons.rejected.connect(dialog.reject)
    form_layout.addWidget(buttons)

    dialog.setLayout(form_layout)
    dialog.exec()

def apply_event_filter(self, **filter_data_entries):
    """
        Applique les filtres et affiche la liste des events filtrés.
    """
    filter_data = {}
    if self.controller.authenticated_user.role.name.value == 'SUPPORT':
        if filter_data_entries['checkbox'].isChecked():
            filter_data['only'] = True
        else:
            filter_data['only'] = False
    else:
        if filter_data_entries['checkbox'].isChecked():
            filter_data['associate_support'] = True
        else :
            filter_data['associate_support'] = False
    filter_data['contract_id'] = filter_data_entries['combobox'].currentData()
    filter_data['start_date_after'] = filter_data_entries['start_date_after'].date().toPython()
    filter_data['start_date_before'] = filter_data_entries['start_date_before'].date().toPython()
    filter_data['location'] = filter_data_entries['location'].text()

    events = self.controller.event_filter(**filter_data)
    show_filtered_events(self, events)

def show_filtered_events(self, events):

    """
    Affiche les contrats filtrés dans une nouvelle fenêtre.
    """
    if events:
        for event in events:
            if event.contract and event.contract.customer:
                event.customer_name = event.contract.customer.name
        labels_list =  ["Event ID","contract ID", "Name", "Support Contact",
                        "Customer Name", "Start Date","End Date", "Location",
                        "Attendees", "Comment"]
        attributes_list = ["id", "contract_id", "name", "support_contact", "customer_name",
                            "start_date", "end_date", "location", "attendees", "comment"]
        table = mk_create_table(labels_list, events, attributes_list)
        mk_create_table_window(self, "Events Table", "Event Informations", table)

    else:
        QMessageBox.warning(self, "Error", "No Event found.")



