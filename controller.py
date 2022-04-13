from model import *
from util import *
from exception import *


class Controller:
    """
    Gère la transition entre l'interface (la vue) et le modèle (les opérations sur le compte)
    Transmet au modèle la requête de l'utilisateur et retourne à l'utilisateur le résultat ou les erreurs s'il y en a
    """

    def __init__(self, compte_courant: CompteCourant, compte_epargne: CompteEpargne):
        """
        Constructeur de l'objet Controller
        Paramètre en entrée : les comptes courant et épargne de l'utilisateur
        """
        self.__compte_courant = compte_courant
        self.__compte_epargne = compte_epargne

    def traiter_requete(self, requete: dict):
        """
        Transmet la requête de l'utilisateur, transmise sous la forme d'un dictionnaire contenant 2 clés :
        - "compte" qui a pour valeur associée "epargne" ou "courant"
        - "valeur" qui a pour valeur associée une string : la valeur de l'opération que veut réaliser l'utilisateur
        Gère les exceptions éventuelles
        Renvoie un dictionnaire contenant la clé "erreur" si une exception a été levée, la clé "resultat" sinon
        """

        reponse = {}

        try:
            # on teste si la requête est sous le bon format
            check_requete_valide(requete)

            # on récupère le compte associé à la clé "compte" de la requête
            if requete["compte"] == "epargne":
                compte = self.__compte_epargne
            elif requete["compte"] == "courant":
                compte = self.__compte_courant

            # on récupère la valeur associée à la clé "valeur" de la requête
            valeur = float(requete["valeur"])

            # on vérifie que l'utilisateur a le droit d'effectuer ses opérations
            check_valeur_non_nulle(valeur)
            check_au_dela_du_decouvert(compte, valeur)

            # on appelle les méthodes du compte qui effectuent les opérations
            if valeur < 0:
                compte.retrait(-valeur)
            else:
                compte.versement(valeur)

            # on applique les intérêts ou les agios suivant le type de compte
            if type(compte) == CompteEpargne:
                compte.appliquer_interets()
            elif type(compte) == CompteCourant:
                compte.appliquer_agios()

            # on renvoie l'affichage du compte, sous forme de str dans la reponse
            reponse["resultat"] = str(compte)
            return reponse

        # s'il y a une erreur on l'ajoute
        except (EntreeUtilisateurException, ValeurOperationNulleException, DecouvertSurLeCompteException) as erreur:
            reponse["erreur"] = str(erreur)
            return reponse
