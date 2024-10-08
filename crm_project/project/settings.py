import subprocess
import os
import sys
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from crm_project.project.config import Base, configure_database
from crm_project.models import *
from crm_project.controllers import *


session, engine = configure_database()


def run_coverage(test_path=None, use_pytest=False):
    """Exécuter les tests avec coverage, avec support pour pytest et unittest."""
    # Ajouter crm_project au PYTHONPATH
    project_root = os.path.dirname(os.path.abspath(__file__))
    crm_project_path = os.path.join(project_root, "crm_project")

    if crm_project_path not in sys.path:
        sys.path.insert(0, crm_project_path)

    if use_pytest:
        config_file = ".coveragerc_views"
        data_file = ".coverage_views"
        pytest_file_path = os.path.join(
            "crm_project", "tests", "tests_integration", "test_views.py"
        )
        test_command = [
            "coverage",
            "run",
            f"--rcfile={config_file}",
            "--source=crm_project",
            f"--data-file={data_file}",
            "-m",
            "pytest",
            pytest_file_path,
        ]

    else:
        # With unittest
        data_file = ".coverage_controllers"
        config_file = ".coveragerc_controllers"
        if test_path:
            # Si un chemin de tests est fourni, exécute les tests sur ce chemin avec unittest
            if os.path.isdir(test_path):
                test_command = [
                    "coverage",
                    "run",
                    f"--rcfile={config_file}",
                    "--source=crm_project",
                    f"--data-file={data_file}",
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    test_path,
                ]
            else:
                test_command = [
                    "coverage",
                    "run",
                    f"--rcfile={config_file}",
                    "--source=crm_project",
                    f"--data-file={data_file}",
                    "-m",
                    "unittest",
                    test_path,
                ]
        else:
            # Si aucun chemin n'est spécifié, exécuter tous les tests avec unittest
            test_dir = os.path.join(project_root, "crm_project", "tests")
            test_command = [
                "coverage",
                "run",
                f"--rcfile={config_file}",
                "--source=crm_project",
                f"--data-file={data_file}",
                "-m",
                "unittest",
                "discover",
                "-s",
                test_dir,
            ]

    # Exécuter la commande de test
    subprocess.run(test_command)

    # Générer les rapports de couverture spécifiques
    subprocess.run(
        ["coverage", "report", f"--data-file={data_file}"]
    )  # Générer le rapport dans le terminal
    subprocess.run(
        ["coverage", "html", f"--data-file={data_file}"]
    )  # Générer un rapport HTML


def run_tests(test_path=None):
    if test_path:
        # Si le chemin spécifié est un dossier, utilisez unittest discover pour exécuter tous les tests dans ce dossier
        if os.path.isdir(test_path):
            test_command = [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                test_path,
            ]
        else:
            # Si c'est un fichier spécifique, exécutez ce fichier de test
            test_command = [sys.executable, "-m", "unittest", test_path]
    else:
        # Si aucun chemin n'est spécifié, exécuter les tests par défaut dans le répertoire 'tests'
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "tests"
        )
        test_command = [sys.executable, "-m", "unittest", "discover", "-s", test_dir]

    subprocess.run(test_command)


def initialize_roles_and_permissions(session=None):
    own_session = False
    if session is None:
        # Si aucune session n'est fournie, créer une nouvelle session locale(POUR LES TESTS)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        own_session = True

    try:
        # Liste des permissions par rôle
        permissions_by_role = {
            RoleName.ADMIN: [
                {"name": "create_user", "description": "Can create a user"},
                {"name": "delete_user", "description": "Can delete a user"},
                {"name": "create_customer", "description": "Can create a client"},
                {
                    "name": "update_customer",
                    "description": "Can edit client information",
                },
                {
                    "name": "update_contract",
                    "description": "Can edit contract information",
                },
                {"name": "create_event", "description": "Can create event"},
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
                {"name": "get_events", "description": "Can view a list of events"},
                {"name": "update_event", "description": "Can edit a event"},
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
                {"name": "create_user", "description": "Can create a user"},
                {"name": "delete_user", "description": "Can delete a user"},
                {"name": "update_user", "description": "Can update a user"},
                {"name": "create_contract", "description": "Can create a contract"},
                {"name": "update_contract", "description": "Can update a contract"},
                {"name": "get_events", "description": "Can view a list of events"},
                {"name": "update_event", "description": "Can edit a event"},
                {
                    "name": "get_contracts",
                    "description": "Can view a list of contracts",
                },
            ],
            RoleName.COMMERCIAL: [
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
                {"name": "get_events", "description": "Can view a list of events"},
                {
                    "name": "get_contracts",
                    "description": "Can view a list of contracts",
                },
                {"name": "create_customer", "description": "Can create a client"},
                {
                    "name": "update_customer",
                    "description": "Can edit client information",
                },
                {
                    "name": "update_contract",
                    "description": "Can edit contract information",
                },
                {"name": "create_event", "description": "Can create event"},
            ],
            RoleName.USER: [
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
            ],
            RoleName.SUPPORT: [
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
                {"name": "get_events", "description": "Can view a list of events"},
                {
                    "name": "get_contracts",
                    "description": "Can view a list of contracts",
                },
                {"name": "update_event", "description": "Can edit a event"},
            ],
            RoleName.MANAGEMENT: [
                {
                    "name": "get_customers",
                    "description": "Can view the dashboard of clients",
                },
                {"name": "create_user", "description": "Can create a user"},
                {"name": "delete_user", "description": "Can delete a user"},
                {"name": "update_user", "description": "Can update a user"},
                {"name": "create_contract", "description": "Can create a contract"},
                {"name": "update_contract", "description": "Can update a contract"},
                {"name": "get_events", "description": "Can view a list of events"},
                {"name": "update_event", "description": "Can edit a event"},
            ],
        }

        # Création des rôles et des permissions
        for role_name, permissions in permissions_by_role.items():
            # Vérifie si le rôle existe déjà
            role = session.query(Role).filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name.value} role")
                session.add(role)

            # Création et association des permissions
            for perm_data in permissions:
                # Vérifie si la permission existe déjà
                permission = (
                    session.query(Permission).filter_by(name=perm_data["name"]).first()
                )
                if not permission:
                    permission = Permission(
                        name=perm_data["name"], description=perm_data["description"]
                    )
                    session.add(permission)

                # Associe la permission au rôle
                if permission not in role.permissions:
                    role.permissions.append(permission)

        if own_session:
            session.commit()
    except Exception as e:
        if own_session:
            session.rollback()
        raise e
    finally:
        if own_session:
            session.close()

    print("Rôles et permissions ont été initialisés avec succès.")
