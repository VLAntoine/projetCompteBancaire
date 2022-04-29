# Projet de création de comptes bancaires
Projet de la formation POEC cybersécurité de l'EPSI sur la gestion de comptes bancaires en Python


## Objectifs de l'exercice

Créer 3 classes : Compte (la classe mère), CompteEpargne et CompteCourant (les classes enfants)   
Gérer les opérations que vont y faire les utilisateurs (virements et retraits), en demandant :
- sur quel compte il veut effectuer des opérations
- la valeur de l'opération qu'il veut effectuer (s'il entre une valeur négative, on considère que c'est un retrait)
Il faudra gérer les erreurs induites par une mauvaise utilisation de l'application par l'utilisateur.   

Actualiser les soldes de chacun des comptes à la suite de chacune des opérations, en tenant compte de leurs règles spécifiques :
- pour les comptes épargne : appliquer le taux d'intérêt (donné en entrée) et vérifier que l'opération (si c'est un retrait) ne rend pas le solde négatif
- pour les comptes courant : vérifier que le solde ne tombe pas en-dessous de la limite de découvert autorisé (donné en entrée) et appliquer les agios si le solde est négatif


## Solution proposée

On divise l'application en 3 couches :
- le model (_model.py_) : contient la classe Compte et ses héritières. C'est là que se font les opérations sur les comptes.
- le controller (_controller.py_) : traite les informations transmises par les utilisateurs au model et retourne la réponse ou les erreurs à l'utilisateur.
- la view (_view.py_) : l'interface utilisateur. Elle se découpe en 2 classes : 
  - l'affichage en ligne de commande ;
  - l'affichage avec tk : actualise l'affichage en direct (à la suite d'une opération de l'utilisateur) des soldes présents sur les 2 comptes.   

On définit des exceptions spécifiques aux erreurs que peut faire l'utilisateur (mauvaise donnée fournit en entrée, retrait supérieur au découvert autorisé sur le compte, ...), dans le fichier _exception.py_.   

On implémente la gestion de ces erreurs dans le fichier _util.py_.

Dans _main.py_, on instancie un compte épargne et un compte courant et on demande si l'on veut un affichage en ligne de commande ou un affichage graphique (sous tk).


## Utilisation

Cloner le dépot git   
Lancer main.py

