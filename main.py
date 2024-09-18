import sys
import os
import sentry_sdk

from crm_project.project.config import setup_env_file, configure_database

from crm_project.controllers.authentication_controller import AuthenticationController
from crm_project.views.main_window import MainWindow

from PySide6.QtWidgets import QApplication




# Sentry Init 
sentry_sdk.init(
    dsn="https://1ce0d8ef9a7546ea96b3a53987d0d8b4@o4507962541998080.ingest.de.sentry.io/4507962548944976",
    traces_sample_rate=1.0,  # 100% des transactions capturées pour le tracing
    profiles_sample_rate=1.0,  # 100% des transactions profilées
)


def load_stylesheet(file_path):
    """
        Load a QSS file 
    """
    with open(file_path, "r") as file:
        return file.read()


def start_application():
    """
        Setup QApp Main window(View), database and controller for Oauth
    """

    session, engine = configure_database()
    app = QApplication(sys.argv)

    # Get absolute pass of QSS style 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qss_file = os.path.join(current_dir, "crm_project/styles/main_style.qss")
    stylesheet = load_stylesheet(qss_file)
    app.setStyleSheet(stylesheet)
    
    try:
        main_window = MainWindow()
        controller = AuthenticationController(session, main_window)
        main_window.set_controller(controller)
        controller.show_login_view()
        main_window.show()
        sys.exit(app.exec())
    finally:
        session.close()
    

if __name__ == "__main__":
    # 1 : Check .env with encrypted password and key for setup database
    setup_env_file()
    
    #2: Start Application 
    start_application()
