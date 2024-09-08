# 🌐 CRM Project / EPIC EVENTS

## Description

Ce projet est un système de gestion de la relation client (CRM) développé en Python. Il utilise SQLAlchemy comme ORM pour la gestion de la base de données MySql et Tkinter pour l'interface utilisateur graphique. Ce logiciel CRM permet de collecter et de traiter les données des clients
et de leurs événements, tout en facilitant la communication entre les
différents pôles de l'entreprise.


## Comment Epic Events fonctionne
Nos équipes opérationnelles sont divisées en trois départements :
-  le département commercial ;
-  le département support ;
-  le département gestion.
  
Les commerciaux démarchent les clients. Ils créent et mettent à jour
leurs profils sur la plateforme. Lorsqu’un client souhaite organiser un
événement, un collaborateur du département gestion crée un contrat et
l’associe au client.
Une fois le contrat signé, le commercial crée l’événement dans la
plateforme et le département gestion désigne un membre du
département support qui sera responsable de l’organisation et du
déroulé de l’événement.


## Besoins et fonctionnalités
### Besoins généraux
- Chaque collaborateur doit avoir ses identifiants pour utiliser la
plateforme.
- Chaque collaborateur est associé à un rôle (suivant son
département).
- La plateforme doit permettre de stocker et de mettre à jour les
informations sur les clients, les contrats et les événements.
- Tous les collaborateurs doivent pouvoir accéder à tous les clients,
contrats et événements en lecture seule.
### Besoins individuels : équipe de gestion
- Créer, mettre à jour et supprimer des collaborateurs dans le
système CRM.
- Créer et modifier tous les contrats.
- Filtrer l’affichage des événements, par exemple : afficher tous les
événements qui n’ont pas de « support » associé.
- Modifier des événements (pour associer un collaborateur support à
l’événement).
### Besoins individuels : équipe commerciale
- Créer des clients (le client leur sera automatiquement associé).
- Mettre à jour les clients dont ils sont responsables.
- Modifier/mettre à jour les contrats des clients dont ils sont
responsables.
- Filtrer l’affichage des contrats, par exemple : afficher tous les
contrats qui ne sont pas encore signés, ou qui ne sont pas encore
entièrement payés.
- Créer un événement pour un de leurs clients qui a signé un
contrat.
### Besoins individuels : équipe support
- Filtrer l’affichage des événements, par exemple : afficher
uniquement les événements qui leur sont attribués.
- Mettre à jour les événements dont ils sont responsables.
