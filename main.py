from view import *

compte_epargne = CompteEpargne(1132324, "Jean-Claude", solde=0, pourcentage_interets=0.1)
compte_courant = CompteCourant(343232, "Jean-Claude", solde=0, autorisation_decouvert=200, pourcentage_agios=0.1)

affichage = ""

while affichage != "com" and affichage != "tk":
    print("Affichage en ligne de commande / via tkinter (taper com / tk)")
    affichage = input()

if affichage == "com":
    view = AffichageLigneDeCommande(compte_courant, compte_epargne)
else:
    view = AffichageTk(compte_courant, compte_epargne)

