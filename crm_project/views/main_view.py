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
    self.form_layout = QFormLayout(self)
    # Fenêtre modale pour mettre à jour un client
    if self.controller.authenticated_user.role.name == 'COMMERCIAL':
        contracts = get_contract_commercial(self.controller.authenticated_user, self.controller.session)
    else:
        contracts = get_contracts_list(self.controller.session)
    display_names = [f"{contract.id} - {contract.customer.last_name}" for contract in contracts]

    mk_create_combox_id_name(self, contracts, display_names, "Contract")

    mk_create_checkbox(self, "Filter by Status (Active=Signed)", False)

    fields_dict = {
        'amount_due': 'Amount Due:',
        'remaining_amount': 'Remaining Amount:',
    }
    mk_create_edit_lines(self, fields_dict)
    self.field_entries['status'] = self.checkbox

    # Connecter l'événement de changement de sélection de la combobox à la fonction
    self.combobox.currentIndexChanged.connect(lambda: mk_update_fields(self))

    # Met a jour les champ en fonction du combobox et retourne le contract selectionné
    mk_update_fields(self)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(lambda: update_contract(self, dialog, 
        amount_due=self.field_entries['amount_due'].text(),
        remaining_amount=self.field_entries['remaining_amount'].text(),
        status=self.field_entries['status'].isChecked() 
    ))
    buttons.rejected.connect(dialog.reject)
    self.form_layout.addWidget(buttons)

    # Appliquer le layout à la fenêtre modale
    dialog.setLayout(self.form_layout)
    dialog.exec()


def update_contract(self, dialog, **field_entries):
    try :
        contract_id = self.selected_id
        print(f"contract id : {contract_id}")
        updated_contract = self.controller.update_contract(contract_id, **field_entries)
        print(f"new contract : {updated_contract.to_dict()}")
        QMessageBox.information(self, "Success", f"Contract {updated_contract.id} updated successfully.")
        dialog.accept()  # Ferme la fenêtre après succès
    except ValueError as e:
        QMessageBox.warning(self, "Error", str(e))
    except Exception as e:
        QMessageBox.critical(self, "Error", f"An error occurred: {e}")


