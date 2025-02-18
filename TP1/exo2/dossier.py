import os
from item import Item



class Dossier(Item):
    def __init__(self, name, chemin_parent, date_creation):
        super().__init__(name, chemin_parent, date_creation)

    def ouvrir(self):
        if os.name == 'nt':
            #  os.system(open(self.chemin_parent).read())
            print(f'open{self.chemin_parent} {self.name} {self.date_creation}')
            print(f"le fichier {self.name} a été ouvert dans l'explorateur windows")
        elif os.name == 'posix':
            # os.system(open(self.chemin_parent).read())
            print(f'open{self.chemin_parent} {self.name} {self.date_creation}')
        else:
            raise ValueError("le système ne peut pas ouvrir l'explorateur de fichier")

    def retirer_doublons(self):

        fichiers = os.listdir(self.chemin_parent)
        fichier_supprimer = []
        fichier_contenu = {}

        for fichier in fichiers:
            chemin_fichier = os.path.join(self.chemin_parent, fichier)
            if os.path.isfile(chemin_fichier):
                with open(chemin_fichier, 'rb') as f:
                    contenu = f.read()
            else:
                raise ValueError("le fichier n'existe pas")

            if contenu in fichier_contenu:
                fichier_supprimer.append(fichier)
                print(f"Le fichier {fichier} a le meme contenu qu'un autre fichier dans {fichier_contenu}")
            else:
                print(f"Le fichier {fichier} n'est pas un doublon.")

        for fichier in fichier_supprimer:
            # chemin_fichier = os.path.join(self.chemin_parent, fichier)
            os.remove(chemin_fichier)
            print(f" le {fichier} a été supprimé. Car, c'est un doublon")
