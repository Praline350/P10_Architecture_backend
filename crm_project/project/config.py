import os

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

    return SessionLocal(), engine


# Declarativa Base for SqlAlchemy models
Base = declarative_base()