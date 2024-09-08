import argparse
from crm_project.project.settings import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outils de gestion du projet.")
    parser.add_argument("command", help="Commande à exécuter", choices=["test", "create_db", "drop_db", "init_roles", "create_user", "coverage"])
    parser.add_argument("test_path", nargs="?", help="Chemin vers un fichier de test ou une classe de test spécifique", default=None)

    args = parser.parse_args()

    match args.command:
        case "init_roles":
            initialize_roles_and_permissions()
        case "create_db":
            create_db()
        case "drop_db":
            drop_db()
        case "test":
            print("Tests en cours d'exécution...")
            run_tests(args.test_path)
        case "coverage":
            run_coverage(args.test_path)
        case "create_user":
            create_user()
        case _:
            print("Commande non reconnue.")
