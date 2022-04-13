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
