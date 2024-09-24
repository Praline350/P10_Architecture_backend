import subprocess
import os
import sys
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from crm_project.project.config import  Base, configure_database
from crm_project.models import *
from crm_project.controllers import *


session, engine = configure_database()



def create_db():
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès.")

def drop_db():
    confirmation = input("Êtes-vous sûr de vouloir supprimer la base de données ? Cette action est irréversible. Tapez 'OUI' pour confirmer : ")
    if confirmation == 'OUI':
        # Obtenir une connexion à partir de l'engine
        with engine.connect() as connection:
            try:
                # Désactiver les vérifications des clés étrangères
                connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
                
                # Supprimer les tables dans un ordre spécifique
                # D'abord, les tables qui dépendent d'autres tables (enfants)
                connection.execute(text("DROP TABLE IF EXISTS customers;"))
                connection.execute(text("DROP TABLE IF EXISTS contracts;"))
                connection.execute(text("DROP TABLE IF EXISTS events;"))
                
                # Ensuite, les tables parentales
                connection.execute(text("DROP TABLE IF EXISTS role_permissions;"))
                connection.execute(text("DROP TABLE IF EXISTS permissions;"))
                connection.execute(text("DROP TABLE IF EXISTS roles;"))
                connection.execute(text("DROP TABLE IF EXISTS users;"))
                
                print("Base de données supprimée avec succès.")
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")
            finally:
                # Réactiver les vérifications des clés étrangères
                connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    else:
        print("Action annulée.")


def create_user(role=None):
    if role is None:
        role = input("Choississez le role (minuscule): ")
    match role:
        case 'admin':
            role = session.query(Role).filter_by(name=RoleName.ADMIN.value).first()
            user_data = {
                'first_name':"admin",
                'last_name':"admin",
                'employee_number':"0",
                'email':"email0@email.com",
                'username':"admin",
                'password':"pass"
            }
        case 'commercial':
            role = session.query(Role).filter_by(name=RoleName.COMMERCIAL.value).first()
            user_data = {
                'first_name':"commercial",
                'last_name':"commercial",
                'employee_number':"0",
                'email':"email1@email.com",
                'username':"commercial",
                'password':"pass"
            }
        case 'support':
            role = session.query(Role).filter_by(name=RoleName.SUPPORT.value).first()
            user_data = {
                'first_name':"support",
                'last_name':"support",
                'employee_number':"0",
                'email':"email2@email.com",
                'username':"support",
                'password':"pass"
            }
        case 'management':
            role = session.query(Role).filter_by(name=RoleName.MANAGEMENT.value).first()
            user_data = {
                'first_name':"management",
                'last_name':"management",
                'employee_number':"0",
                'email':"email3@email.com",
                'username':"management",
                'password':"pass"
            }
    try:
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            employee_number=user_data['employee_number'],
            email=user_data['email'],
            username=user_data['username'],
            role=role
        )

        new_user.set_password(user_data['password'])
        session.add(new_user)
        session.commit()
        print("Utilisateur créé avec succès.")

    except IntegrityError:
        session.rollback()
        print("L'utilisateur avec cet email ou ce nom d'utilisateur existe déjà.")