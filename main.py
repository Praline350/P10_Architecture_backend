import sys
import os
import sentry_sdk

from cryptography.fernet import Fernet
from getpass import getpass
from dotenv import load_dotenv

from crm_project.project.settings import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from crm_project.controllers.authentication_controller import *
from crm_project.views.main_window import MainWindow

from PySide6.QtWidgets import QApplication


def generate_key():
    return Fernet.generate_key()

def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# Check password in .env and create it if not
def setup_env_file():

    load_dotenv()

    if not os.getenv('DB_PASSWORD_ENCRYPTED'):
        print("No password found, Please enter a data base password")
        db_password = getpass("DataBase password : ")  

        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            secret_key = generate_key().decode()
        encrypted_password = encrypt_password(db_password, secret_key)

        with open(".env", "w") as env_file:
            env_file.write(f"SECRET_KEY={secret_key}\n")
            env_file.write(f"DB_PASSWORD_ENCRYPTED={encrypted_password}\n")
        
        print("Encrypted password and secret key wrote in .env file")
        print("Welcome in Epic Event CRM")
    else:
        print("Welcome in Epic Event CRM")

# DB config
def configure_database():

    load_dotenv()
    encrypted_password = os.getenv('DB_PASSWORD_ENCRYPTED')
    secret_key = os.getenv('SECRET_KEY')

    db_password = decrypt_password(encrypted_password, secret_key)
    database_url = f"mysql+mysqldb://Admin:{db_password}@localhost:3306/epic_event_db"

    # SQLAclhemy setup
    engine = create_engine(database_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal()

# Initialisation de Sentry
sentry_sdk.init(
    dsn="https://1ce0d8ef9a7546ea96b3a53987d0d8b4@o4507962541998080.ingest.de.sentry.io/4507962548944976",
    traces_sample_rate=1.0,  # 100% des transactions capturées pour le tracing
    profiles_sample_rate=1.0,  # 100% des transactions profilées
)

def load_stylesheet(file_path):
    """
    Charge et renvoie le contenu du fichier QSS
    """
    with open(file_path, "r") as file:
        return file.read()

def start_application():

    session = configure_database()
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
    # 1 : Check .env with encrypted password and key
    setup_env_file()
    
    #2: Start Application 
    start_application()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Obtenir le chemin absolu du fichier style.qss
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     qss_file = os.path.join(current_dir, "crm_project/styles/main_style.qss")
    
#     # Charger et appliquer le QSS
#     stylesheet = load_stylesheet(qss_file)
#     app.setStyleSheet(stylesheet)

#     session = SessionLocal()
#     try:
#         main_window = MainWindow()
#         controller = AuthenticationController(session, main_window)
#         main_window.set_controller(controller)
#         controller.show_login_view()
#         main_window.show()
#         sys.exit(app.exec())
#     finally:
#         session.close()


