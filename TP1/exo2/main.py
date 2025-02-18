import os
from item import Item
from fichier import Fichier
from dossier import Dossier

if __name__ == '__main__':
    try:
        fichier = Fichier("dcc", "U:/", "18-02-2025", ".txt")

        #  print(f"")
        fichier.ouvrir()
    except ValueError as e:
        print(f"erreur lors de l'ouverture du dossier{e}")

    # try:
    #     dossier = ""
    #     print(f"")
    #     dossier.retirer_doublons()
    # except ValueError as e:
    #     print(f"erreur lors de la suppression du dossier{e}")
