import re
from model import *
from exception import *

# le regex qui décrit l'écriture des nombres décimaux
PATTERN_DECIMAL = re.compile("^[-+]{0,1}[0-9]{1,}[.]{0,1}[0-9]{0,}$")


def check_requete_valide(requete: dict):
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


def check_valeur_non_nulle(valeur: float):
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
