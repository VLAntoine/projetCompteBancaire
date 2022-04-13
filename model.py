from abc import ABC, abstractmethod


class Compte(ABC):
    """
    La classe abstraite, parente de toutes les classes Compte
    """

    def __init__(self, numero_compte: int, nom_proprietaire: str, solde: float = 0):
        """
        Le constructeur de la classe Compte
        Le solde est fixé par défaut à 0
        """
        self._numero_compte = numero_compte
        self._nom_proprietaire = nom_proprietaire
        self._solde = solde

    @property
    def solde(self):
        """
        Le getter de l'attribut solde
        """
        return self._solde

    def __str__(self):
        """
        Retourne l'objet compte comme un string contenant tous ses attributs.
        Le solde est arrondi à 2 chiffres après la virgule.
        """
        solde_arrondi = round(self._solde, 2)
        return f"Numéro de compte : {self._numero_compte} ; Propriétaire : {self._nom_proprietaire} ; Solde : {solde_arrondi} "

    def retrait(self, valeur: float):
        """
        Retire la valeur en entrée au solde de l'utilisateur.
        La valeur du retrait est toujours positive
        """
        self._solde -= valeur

    def versement(self, valeur: float):
        """
        Retire la valeur en entrée au solde de l'utilisateur.
        La valeur du retrait est toujours positive
        """
        self._solde += valeur

    @abstractmethod
    def operation_valable(self, valeur: float):
        """
        Méthode abstraite qui retourne True si le nouveau solde après l'opération de l'utilisateur est supérieur à la
        limite autorisée (0 pour un compte épargne, l'autorisation de découvert pour un compte courant)
        """
        pass

    def info(self) -> dict:
        """
        Retourne les informations sur le compte sous la forme d'un dictionnaire
        """
        solde_arrondi = round(self._solde, 2)
        info = {"numero_compte": self._numero_compte, "nom_proprietaire": self._nom_proprietaire, "solde": solde_arrondi}
        return info


class CompteCourant(Compte):
    """
    La classe CompteCourant, héritière de la classe Compte, qui gère les opérations spécifiques à ce type de compte
    """

    def __init__(self, numero_compte: int, nom_proprietaire: str, solde: float = 0, autorisation_decouvert: float = 0,
                 pourcentage_agios: float = 0):
        """
        Le constructeur de la classe CompteCourant
        Les autorisations de découvert et le pourcentage d'agios sont par défaut nuls
        """
        super(CompteCourant, self).__init__(numero_compte, nom_proprietaire, solde)
        self.__autorisation_decouvert = autorisation_decouvert
        self.__pourcentage_agios = pourcentage_agios

    @property
    def autorisation_decouvert(self):
        """
        Le getter de l'attribut autorisation_decouvert
        """
        return self.__autorisation_decouvert

    @property
    def pourcentage_agios(self):
        """
        Le getter de l'attribut pourcentage_agios
        """
        return self.__pourcentage_agios

    def operation_valable(self, valeur):
        """
        True si l'opération demandée par l'utilisateur est valable, i.e:
        - soit parce que le nouveau solde (après l'opération) est supérieur à 0
        - soit parce que la valeur absolue du nouveau solde est inférieure à l'autorisation de découvert
        """
        valeur_sur_le_compte = self.solde + valeur

        # la valeur absolue de ce qui est sur le compte à la fin ne doit pas être supérieure au découvert autorisé
        return valeur_sur_le_compte > 0 or -valeur_sur_le_compte < self.autorisation_decouvert

    def appliquer_agios(self):
        """
        Intègre les agios au calcul du nouveau solde
        """
        if self._solde < 0:
            self._solde += self._solde * self.__pourcentage_agios


class CompteEpargne(Compte):
    """
    La classe CompteEpargne, héritière de la classe Compte, qui gère les opérations spécifiques à ce type de compte
    """

    def __init__(self, numero_compte: int, nom_proprietaire: str, solde: float = 0, pourcentage_interets: float = 0):
        """
        Le constructeur de la classe CompteEpargne
        Le pourcentage d'intérêts est par défaut nul
        """
        super(CompteEpargne, self).__init__(numero_compte, nom_proprietaire, solde)
        self.__pourcentage_interets = pourcentage_interets

    def operation_valable(self, valeur):
        """
        True si l'opération demandée par l'utilisateur est valable, i.e si le nouveau solde (après l'opération) est
        supérieur à 0
        """
        valeur_sur_le_compte = self.solde + valeur

        # la valeur absolue de ce qui est sur le compte à la fin ne doit pas être supérieure à 0
        return valeur_sur_le_compte > 0

    def appliquer_interets(self):
        """
        Intègre les intérêts au calcul du nouveau solde
        """
        self._solde += self._solde * self.__pourcentage_interets
