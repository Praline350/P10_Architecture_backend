import os

from pathlib import Path
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from getpass import getpass
from dotenv import load_dotenv

from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()


def setup_env_file():
    env_file_path = Path(".env")

    # Si le fichier .env n'existe pas
    if not env_file_path.exists():
        print("No .env file found, Please enter a database password")
        db_password = getpass("Database password: ")

        # Toujours générer une clé secrète si elle n'existe pas dans l'environnement
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            secret_key = generate_key().decode()

        # Chiffrer le mot de passe
        encrypted_password = encrypt_password(db_password, secret_key)

        # Écriture dans le fichier .env
        with open(".env", "w") as env_file:
            env_file.write(f"SECRET_KEY={secret_key}\n")
            env_file.write(f"DB_PASSWORD_ENCRYPTED={encrypted_password}\n")
        print("Welcome to Epic Event CRM")
        load_dotenv()

    else:
        load_dotenv()
        if not os.getenv("DB_PASSWORD_ENCRYPTED"):
            print("No password found in .env, Please enter a database password")
            db_password = getpass("Database password: ")

            secret_key = os.getenv("SECRET_KEY")
            if not secret_key:
                secret_key = generate_key().decode()

            encrypted_password = encrypt_password(db_password, secret_key)

            with open(
                ".env", "a"
            ) as env_file:  # Ouvrir le fichier en mode ajout si déjà existant
                env_file.write(f"DB_PASSWORD_ENCRYPTED={encrypted_password}\n")
            print("Encrypted password written in .env file")
            print("Welcome to Epic Event CRM")


def configure_database():

    os.environ.pop("DB_PASSWORD_ENCRYPTED", None)
    os.environ.pop("SECRET_KEY", None)

    load_dotenv()

    encrypted_password = os.getenv("DB_PASSWORD_ENCRYPTED")
    secret_key = os.getenv("SECRET_KEY")

    db_password = decrypt_password(encrypted_password, secret_key)
    database_url = f"mysql+mysqldb://Admin:{db_password}@localhost:3306/epic_event_crm"

    # SQLAlchemy setup
    engine = create_engine(database_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal(), engine


# Declarativa Base for SqlAlchemy models
Base = declarative_base()
