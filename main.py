import sys
import os
import sentry_sdk

from crm_project.project.config import SessionLocal
from crm_project.controllers.authentication_controller import *
from crm_project.views.main_window import MainWindow
from PySide6.QtWidgets import QApplication



# Initialisation de Sentry
sentry_sdk.init(
    dsn="https://1ce0d8ef9a7546ea96b3a53987d0d8b4@o4507962541998080.ingest.de.sentry.io/4507962548944976",
    traces_sample_rate=1.0,  # 100% des transactions capturées pour le tracing
    profiles_sample_rate=1.0,  # 100% des transactions profilées
)

# Test Sentry
# division_by_zero = 1 / 0



def load_stylesheet(file_path):
    """
    Charge et renvoie le contenu du fichier QSS
    """
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Obtenir le chemin absolu du fichier style.qss
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qss_file = os.path.join(current_dir, "crm_project/styles/main_style.qss")
    
    # Charger et appliquer le QSS
    stylesheet = load_stylesheet(qss_file)
    app.setStyleSheet(stylesheet)

    session = SessionLocal()
    try:
        main_window = MainWindow()
        controller = AuthenticationController(session, main_window)
        main_window.set_controller(controller)
        controller.show_login_view()
        main_window.show()
        sys.exit(app.exec())
    finally:
        session.close()


