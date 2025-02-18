from item import Item
import os

class Fichier(Item):
    def __init__(self, name, chemin_parent, date_creation, extension):
        super().__init__(name, chemin_parent, date_creation)
        self.extension = extension

    def ouvrir(self):
        chemin_fichier = os.path.join(self.chemin_parent, self.name + self.extension)
        if os.name == 'nt':
            os.system(f'open {chemin_fichier}')
        elif os.name == 'posix':
            os.system(f'start {chemin_fichier}')
        else:
            raise ValueError(f"Unsupported OS: {os.name}, os ne permet pas d'ouvrir le fichier")
