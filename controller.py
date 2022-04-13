from model import *
import re

# le regex qui décrit l'écriture des nombres décimaux
PATTERN_DECIMAL = re.compile("^[-+]{0,1}[0-9]{1,}[.]{0,1}[0-9]{0,}$")


class EntreeUtilisateurException(Exception):
    """
    Exception renvoyée en cas d'erreur d'entrée de l'utilisateur (s'il tape des lettres alors qu'on attend des
    chiffres par exemple)
    """
    pass


class DecouvertSurLeCompteException(Exception):
    """
    Exception si l'opération que cherche à faire l'utilisateur rend son solde inférieur à la limite de découvert
    autorisée
    """
    pass


class ValeurOperationNulleException(Exception):
    """
    Exception si l'utilisateur cherche à faire un virement ou un retrait nul
    """
    pass


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

    def traiter_requete(self, requete: dict()):
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


def check_requete_valide(requete: dict()):
    """
    Fonction qui teste la validité de la requête de l'utilisateur, qui est un dictionnaire
    Lève une exception en cas de non conformité
    """

    # la requête doit contenir une clé "compte"
    if "compte" not in requete.keys():
        raise EntreeUtilisateurException("Vous devez specifier un compte")
    # la requête doit contenir une clé "valeur"
    elif "valeur" not in requete.keys():
        raise EntreeUtilisateurException("Vous devez specifier une valeur")
    # la valeur associée à la clé "compte" est soit "epargne", soit "courant"
    elif requete["compte"] not in ["epargne", "courant"]:
        raise EntreeUtilisateurException("Le compte doit etre soit courant soit epargne")
    # la valeur associée à la clé "valeur" est une string qui décrit un décimal
    elif not PATTERN_DECIMAL.match(requete["valeur"]):
        raise EntreeUtilisateurException("La valeur doit etre un nombre décimal")


def check_valeur_non_nulle(valeur: int):
    """
    Lève une exception si la valeur entrée par l'utilisateur est égale à 0
    On considère que ce n'est ni un virement, ni un retrait
    """
    if valeur == 0:
        raise ValeurOperationNulleException("Vous ne pouvez pas retirer ou virer une somme nulle sur le compte")


def check_au_dela_du_decouvert(compte: Compte, valeur: float):
    """
    Lève une exception si la valeur obtenue à la fin de toutes les opérations est inférieur à la limite de découvert
    autorisée (dans le cas d'un compte courant) ou à zéro (pour un compte épargne)
    """

    # si l'opération n'est pas valable
    if not compte.operation_valable(valeur):

        # on lève une exception adaptée au type de compte
        if type(compte) == CompteCourant:
            raise DecouvertSurLeCompteException("Vous ne pouvez pas retirer au-delà de la limite de découvert "
                                                "autorisee")
        elif type(compte) == CompteEpargne:
            raise DecouvertSurLeCompteException("Vous ne pouvez pas retirer au-delà de 0")
