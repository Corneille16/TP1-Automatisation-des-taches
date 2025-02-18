class Item:
    def __init__(self, name, chemin_parent, date_creation):
        self.name = name
        self.chemin_parent = chemin_parent
        self.date_creation = date_creation
        if self.chemin_parent != None:
            self.chemin_parent.date_creation = date_creation
        else:
               raise ValueError("le fichier ou le dossier n'existe pas")


    def ouvrir(self):
        NotImplemented
        raise NotImplementedError
