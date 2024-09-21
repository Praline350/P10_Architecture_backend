![License](https://img.shields.io/badge/License-MIT-blue.svg) 

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue) 

![Coverage](https://img.shields.io/badge/Coverage-85%25-green) 


# 🌐 **Epic Event CRM - Gestionnaire de Clients et Événements**

**Epic Event CRM** est un système de gestion des relations client (CRM) développé pour répondre aux besoins des équipes commerciales, support et gestionnaires d'événements. Il permet de gérer les clients, contrats et événements d'une manière intuitive et efficace, tout en garantissant la sécurité des données.

---

## **Table des matières**

- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Technologies Utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Tests](#tests)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## **Introduction**

Epic Event CRM est un logiciel conçu pour gérer efficacement les interactions avec les clients et organiser des événements avec un suivi rigoureux des contrats. Cette solution aide les commerciaux à suivre les prospects et les contrats, les équipes de support à gérer les événements, et les gestionnaires à superviser l'ensemble du processus.

L'objectif principal de ce projet est de faciliter la gestion des données client tout en offrant un haut niveau de personnalisation et d'intégration.

---

## **Fonctionnalités**

- **Gestion des clients** : Ajout, mise à jour et suppression des informations clients.
- **Gestion des contrats** : Création, mise à jour et filtrage des contrats associés aux clients.
- **Suivi des événements** : Planification, mise à jour et gestion des événements avec affectation des contacts support.
- **Tableau de bord personnalisé** : Tableau de bord dédié en fonction du rôle de l'utilisateur (Admin, Commercial, Support, Management).
- **Filtres et recherches avancées** : Filtrage des contrats et événements par date, montant ou client.
- **Sécurisation des accès** : Gestion des rôles et permissions pour les différentes fonctionnalités.
- **Interfaces Utilisateur (UI)** : Interface graphique moderne et intuitive développée avec **Qt pour Python**.

---

## **Technologies Utilisées**

- **Python 3.10+**
- **PySide6 (Qt pour Python)** : Interface graphique
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **MySQL** : Base de données principale
- **dotenv** : Pour la gestion des variables d'environnement
- **Sentry** : Suivi des erreurs et monitoring
- **Unittest / Pytest** : Framework de tests

---

## **Prérequis**

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Python 3.10+](https://www.python.org/downloads/)
- [MySQL](https://www.mysql.com/downloads/)
- [pip](https://pip.pypa.io/en/stable/)


## **Installation** 

### Cloner le dépôt :

```
git clone https://github.com/Praline350/P10_Architecture_backend
```

### Gérer l'environnement virtuel :

```
python -m venv env   # Créer l'env
source env/Scripts/activate  # Active l'env
pip install -r requirements.txt  # Install les dépendance du projet
```

### Lancer le programme :
```
python main.py  # A la racine du projet
```

### Initialisation de la Base de donnée :


Pour garantir la sécurité de l'acces à la base de donnée MySql le mot de passe sera demandé à la première utilisation.
La base de données s'initialise alors, créer un utilisateur manageur et encrypt le mot de passe dans un fichier **.env** pour les utilisations futur.

### Tests :

Le projet inclus des tests unitaires et d'intégration. 

Pour exécuter les tests et la couverture de test coté Back-end : 
```
python manage.py test crm_project
```
Pour exécuter les tests de l'interface graphique QT : 
```
python manage.py --Pytest
```

## **Utilisation**


Pour tous ce qui touche à l'utilisation utilisateur réfèrer vous au mode d'emploi :

--> (URL NOTION)

## **Structure du Projet** 

- **`crm_project/`** : Dossier principal contenant tout le code source du projet.
  - **`controllers/`** : Contient les fichiers gérant la logique métier pour chaque rôle (commercial, support, management).
  - **`helpers/`** : Fonctions utilitaires pour gérer les données ou tâches courantes dans le projet.
  - **`models/`** : Définition des modèles de données utilisés par SQLAlchemy pour interagir avec la base de données.
  - **`views/`** : Les interfaces graphiques (UI) développées avec Qt pour Python (PySide6).
  - **`styles/`** :  Contient le fichier QSS pour les styles généraux
  - **``project/``** :  Dossier de settings et des permissions
    - **`config.py`** : Configure la base de données et les sessions SQLAlchemy.
    - **`permissions.py`** : Methode décorateurs qui gère les permissions et rôles utilisateurs dans l'application.
    - **`settings`** : Différentes logique de commande et l'initialisation des roles et des permissions.  
  - **`tests/`** : Contient tous les tests unitaires et d'intégration.
    - **`test_controllers.py`** : Tests unitaires pour les différents contrôleurs.
     - **`test_models.py`** : Tests des modèles SQLAlchemy (vérification des entités dans la base de données).
    - **`test_views.py`** : Tests pour vérifier les interfaces graphiques Qt et leur interaction avec les contrôleurs.

- **`.env`** : Fichier contenant les variables d'environnement (configuration de la base de données, etc.). Ce fichier n'est pas inclus dans le dépôt Git pour des raisons de sécurité.

- **`requirements.txt`** : Fichier listant toutes les dépendances Python nécessaires pour le projet.

- **`main.py`** : Point d'entrée principal du projet. L'application démarre à partir de ce fichier.

- **`manage.py`** : Script de gestion permettant d'automatiser des tâches telles que la création de la base de données, l'exécution des tests, et d'autres commandes spécifiques.

---

## **Contribuer**

Les contributions sont les bienvenues ! Si vous souhaitez contribuer, veuillez suivre ces étapes :

- Forker le dépôt
- Créer une branche pour vos modifications (git checkout -b ma-nouvelle-fonctionnalité)
- Commiter vos changements (git commit -am 'Ajout d'une nouvelle fonctionnalité')
- Pusher la branche (git push origin ma-nouvelle-fonctionnalité)
- Ouvrir une Pull Request

## **Licence**

Ce projet est sous licence **MIT**.


## **Contact**

Pour toute question ou suggestion, n'hésitez pas à me contacter via mon e-mail

--> Edwin.thierry350@gmail.com


