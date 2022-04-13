from model import *
from controller import Controller
import tkinter as tk


class AffichageTk:
    """
    L'affichage avec Tkinter
    Récupère les requêtes de l'utilisateur et les transmet au controller
    Affiche le résultat à l'utilisateur
    """

    def __init__(self, compte_courant: CompteCourant, compte_epargne: CompteEpargne):
        """
        Le constructeur de Affichage avec Tkinter
        Prend en paramètre les comptes courant et épargne de l'utilisateur
        Affiche la fenêtre avec les différents widgets
        """
        self.compte_courant = compte_courant
        self.compte_epargne = compte_epargne

        # le controller qui va servir à tester les requêtes de l'utilisateur
        self.controller = Controller(compte_courant, compte_epargne)

        # la fenêtre Tkinter qui va accueillir tous les widgets
        self.fenetre = tk.Tk()
        self.fenetre.title("Opérations bancaires")

        # les différentes valeurs qui vont être modifiées suite aux requêtes de l'utilisateur
        self.epargne_var = tk.StringVar()  # la valeur du solde du compte épargne
        self.courant_var = tk.StringVar()  # la valeur du solde du compte courant
        self.compte_var = tk.StringVar()  # le choix de l'utilisateur entre "epargne" et "courant"
        self.valeur_var = tk.StringVar()  # la valeur entrée par l'utilisateur
        self.reponse_var = tk.StringVar()  # la réponse qui est faite à l'utilisateur

        # les infos initiales des comptes pour initialiser les différentes StringVar
        info_courant = compte_courant.info()
        info_epargne = compte_epargne.info()
        nom_proprietaire = info_courant["nom_proprietaire"]
        numero_courant = info_courant["numero_compte"]
        numero_epargne = info_epargne["numero_compte"]
        solde_courant = info_courant["solde"]
        solde_epargne = info_epargne["solde"]

        # l'affichage des différents éléments dans une grid
        tk.Label(self.fenetre, text="Nom : ").grid(row=0)
        tk.Label(self.fenetre, text=f"{nom_proprietaire}").grid(row=0, column=1)
        tk.Label(self.fenetre, text="Numéro de compte").grid(row=1, column=1, pady=(20, 0))
        tk.Label(self.fenetre, text="Solde").grid(row=1, column=2, pady=(20, 0))
        tk.Label(self.fenetre, text="Compte épargne : ").grid(row=2)
        tk.Label(self.fenetre, text=f"{numero_epargne}").grid(row=2, column=1)
        tk.Label(self.fenetre, text="Compte courant : ").grid(row=3)
        tk.Label(self.fenetre, text=f"{numero_courant}").grid(row=3, column=1)

        # on initialise les valeurs du compte épargne et du compte courant et on les affiche
        self.epargne_var.set(f"{solde_epargne}")
        self.courant_var.set(f"{solde_courant}")
        tk.Label(self.fenetre, textvariable=self.epargne_var).grid(row=2, column=2)
        tk.Label(self.fenetre, textvariable=self.courant_var).grid(row=3, column=2)

        # une première question à l'utilisateur
        tk.Label(self.fenetre, text="Sur quel compte voulez-vous faire des opérations").grid(row=4, columnspan=3,
                                                                                             pady=(20, 0))

        # des boutons Radio pour choisir entre Epargne et Courant
        tk.Radiobutton(self.fenetre, text="Epargne", variable=self.compte_var, value="epargne", indicatoron=False) \
            .grid(row=5, column=1)
        tk.Radiobutton(self.fenetre, text="Courant", variable=self.compte_var, value="courant", indicatoron=False) \
            .grid(row=5, column=2)

        # un champ de saisie de texte pour la valeur
        tk.Label(self.fenetre, text="Valeur de l'opération").grid(row=6, column=0, pady=(5, 0))
        tk.Entry(self.fenetre, textvariable=self.valeur_var).grid(row=6, column=1, columnspan=2, pady=(5, 0))

        # le bouton "Effectuer" qui envoie la requête de l'utilisateur
        tk.Button(self.fenetre, text="Effectuer", command=self.traiter_requete) \
            .grid(row=7, columnspan=3, pady=(20, 20))

        # le message de réponse à la requête
        tk.Message(self.fenetre, textvariable=self.reponse_var).grid(row=8, columnspan=3, pady=(20, 0))

        self.fenetre.mainloop()

    def traiter_requete(self):
        """
        Formate la requête pour qu'elle soit comprise par le controller et la transmet
        Met à jour les différents éléments et les affiches
        """

        # Formatage de la requête
        requete = {"compte": self.compte_var.get(), "valeur": self.valeur_var.get()}

        # Traitement de la réponse
        reponse = self.controller.traiter_requete(requete)
        message = ""
        if "erreur" in reponse.keys():
            message += "Erreur : " + reponse["erreur"]
        elif "resultat" in reponse.keys():
            message += "Resultat : " + reponse["resultat"]

        # Mise à jour des nouveaux éléments
        self.reponse_var.set(message)
        self.courant_var.set(self.compte_courant.info()["solde"])
        self.epargne_var.set(self.compte_epargne.info()["solde"])
        self.valeur_var.set("")


class AffichageLigneDeCommande:
    """
    L'affichage en ligne de commande
    Récupère les requêtes de l'utilisateur et les transmet au controller
    Affiche le résultat à l'utilisateur
    """

    def __init__(self, compte_courant: CompteCourant, compte_epargne: CompteEpargne):
        """
        Constructeur de l'affichage en ligne de commande Attributs : un controller pour les comptes courant et
        épargne et une variable qui indique si l'utilisateur souhaite continuer les opérations sur les comptes ou non
        """
        self.__controller = Controller(compte_courant, compte_epargne)
        self.continuer = "o"

        # appel de la méthode enregistrer_requete()
        self.enregistrer_requete()

    def enregistrer_requete(self):
        """
        Gère l'enregistrement des informations concernant l'opération de l'utilisateur, la transmission au controller
        et l'affichage
        """
        # tant que l'utilisateur ne met pas fin aux opérations, on continue
        while self.continuer == "o":

            # réinitialisation de la variable continuer
            self.continuer = ""

            # demande à l'utilisateur sur quel compte il veut faire les opérations
            compte_en_cours = ""
            while compte_en_cours not in ["e", "c"]:
                print("Sur quel compte voulez-vous effectuer les opérations ? (epargne : taper e / courant : taper c)")
                compte_en_cours = input()

            if compte_en_cours == "e":
                compte_en_cours = "epargne"
            elif compte_en_cours == "c":
                compte_en_cours = "courant"

            # demande à l'utilisateur la valeur qu'il souhaite mettre ou retirer sur son compte
            print("Taper la valeur que vous voulez ajouter ou retirer à votre compte : (un décimal avec '.' pour "
                  "separateur)")
            valeur_en_cours = input()

            # on envoie la requête au controller et on récupère la réponse
            requete = {"compte": compte_en_cours, "valeur": valeur_en_cours}
            reponse = self.__controller.traiter_requete(requete)

            # on affiche la réponse
            if "erreur" in reponse.keys():
                print("Erreur : " + reponse["erreur"])
            elif "resultat" in reponse.keys():
                print("Après opération : " + reponse["resultat"])

            # demande à l'utilisateur s'il souhaite continuer les opérations
            self.choix_de_continuer()

    def choix_de_continuer(self):
        """
        Demande à l'utilisateur s'il veut continuer ou non les opérations sur son compte ou non
        """
        while self.continuer != "o" and self.continuer != "n":
            print("Voulez-vous continuer ? (o/n)")
            self.continuer = input()
