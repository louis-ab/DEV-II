class MauvaisInput(Exception):
    """Input no  reconnu."""

class Fusione:
    """Fusione deux fichiers similaires."""
    def __init__(self, nom_1=None, nom_2=None, debut=0):
        """
        Initialise la liste des lignes du fichier fusionné
        PRE : lignes_1 et lignes_2 sont des listes de strings
        POST : les variables de la classe sont créées
        """
        self.nom_1, self.nom_2 = nom_1, nom_2
        self.index_1, self.index_2 = debut, debut
        self.lignes_1, self.lignes_2 = None, None
        self.merged = []

    def __lire(self, path):
        """
        Lit un fichier indiqué par path
        PRE : -
        POST : Renvoie une liste contenant les lignes du fichier
        RAISES : - IOError si le fichier n'existe pas
                 - FileNotFoundError si le fichier ne peut pas être lu
        """
        with open(path, encoding='utf8') as fichier:
            return fichier.readlines()

    def __ajout(self, n_fichier):
        """
        Ajoute une ligne à la liste des lignes fusionées
        PRE : n_fichier est 1 ou 2
        POST : la ligne est ajoutée à self.merged et supprimée de la liste des lignes du fichier
        """
        if n_fichier == 1:
            ligne = self.lignes_1.pop(0)
            self.index_1 += 1
        elif n_fichier == 2:
            ligne = self.lignes_2.pop(0)
            self.index_2 += 1
        self.merged.append(ligne)
        print(str(len(self.merged)) + " : " + ligne[:-1])

    def __suppr(self, n_fichier):
        """
        Supprime la ligne dans la liste des lignes d'un fichier.
        PRE : n_fichier est 1 ou 2
        POST : la ligne est supprimée de la liste des lignes du fichier
        """
        if n_fichier == 1:
            self.lignes_1.pop(0)
            self.index_1 += 1
        elif n_fichier == 2:
            self.lignes_2.pop(0)
            self.index_2 += 1

    def __idem(self):
        """
        Ajoute la ligne dans le cas ou les deux fichiers sont en accord.
        PRE : -
        POST : la ligne est ajoutée à self.merged et supprimée de les deux listes des lignes
        """
        self.__ajout(1)
        self.__suppr(2)

    def __diff(self):
        """
        Demande quoi faire quand les lignes sont différentes et ajoute/suppime en fonction.
        PRE : -
        POST : les lignes sont ajoutées/supprimées en fonction du choix
        """
        print(f"1 : choisir {self.nom_1}, 2 : choisir {self.nom_2}, \
              12 : choisir {self.nom_1} puis {self.nom_2}, \
              21 : choisir {self.nom_2} puis {self.nom_1}, 0 : aucune des deux")
        choix = input("> ")
        print("")

        if choix == '1':
            self.__ajout(1)
            self.__suppr(2)
        elif choix == '2':
            self.__ajout(2)
            self.__suppr(1)
        elif choix == '12':
            self.__ajout(1)
            self.__ajout(2)
        elif choix == '21':
            self.__ajout(2)
            self.__ajout(1)
        elif choix == '0':
            self.__suppr(1)
            self.__suppr(2)
        else:
            raise MauvaisInput

    def __inser(self, n):
        """
        Gère le cas quand une ligne est insérée dans un des fichiers.
        PRE : n est 1 ou 2
        POST : la ligne est ajoutée/supprimée en fonction du choix
        """
        print("1 : garder, 2 : jeter.")
        choix = input("> ")
        print("")

        if choix == '1':
            self.__ajout(n)
        elif choix == '2':
            self.__suppr(n)
        else:
            raise MauvaisInput

    def __inser_prompt(self, n, prompt):
        """
        Demande quoi faire quand une ligne est insérée dans un des fichiers.
        PRE : n est 1 ou 2, prompt est une chaine à afficher
        POST : la ligne est ajoutée/supprimée en fonction du choix
        """
        print("")
        if n == 1:
            print(f"{prompt} {self.nom_1} : {self.lignes_1[0]}")
        else:
            print(f"{prompt} {self.nom_2} : {self.lignes_2[0]}")
        a_faire = True
        while a_faire:
            try:
                self.__inser(n)
                a_faire = False
            except MauvaisInput:
                print("Mauvais input")

    def __inspecte(self):
        """
        Analyse les lignes suivantes et utilise les autres fonctions en fonction du cas.
        PRE : -
        POST : la/les ligne(s) a/ont été traitée(s)
        """
        len_1 = len(self.lignes_1)
        len_2 = len(self.lignes_2)
        if len_1 >= 1 and len_2 >= 1:
            if self.lignes_1[0] == self.lignes_2[0]:
                self.__idem()
            elif len_1 >= 2 and self.lignes_1[1] == self.lignes_2[0]:
                self.__inser_prompt(1, "Une ligne insérée dans")
            elif len_2 >= 2 and self.lignes_1[0] == self.lignes_2[1]:
                self.__inser_prompt(2, "Une ligne insérée dans")
            else:
                print("Différence entre les fichiers :")
                print(" " + str(self.nom_1) + " ligne " + str(self.index_1) + " : " +
                      self.lignes_1[0][:-1])
                print(" " + str(self.nom_2) + " ligne " + str(self.index_2) + " : " +
                      self.lignes_2[0][:-1])
                print("")
                a_faire = True
                while a_faire:
                    try:
                        self.__diff()
                        a_faire = False
                    except MauvaisInput:
                        print("Mauvais input")
        elif len_1 >= 1:
            self.__inser_prompt(1, "Une ligne de plus plus dans")
        elif len_2 >= 1:
            self.__inser_prompt(2, "Une ligne de plus plus dans")

    def __ecrit(self, out):
        """
        Écrit les lignes fusionées dans un fichier.
        PRE : out est une chaine
        POST : lesl ignes on été écrites dans le fichier
        RAISES : IOError si écrire à cet endroit est Impossible
        """
        with open(out, 'w', encoding = 'utf8') as f_sauv:
            for ligne in self.merged:
                f_sauv.write(ligne)

    def run(self):
        """
        Intéractions avec l'utilisateur et traite les fichiers jusqu'à la fin
        PRE : -
        POST : la fusion est faite et le résultat est écrit ou non suivant les choix faits
        """
        if self.nom_1 is None:
            self.nom_1 = input("Premier fichier : ")
        if self.nom_2 is None:
            self.nom_2 = input("Deuxième fichier : ")
        while self.lignes_1 is None:
            try:
                self.lignes_1 = self.__lire(self.nom_1)
            except (FileNotFoundError, IOError):
                print("Fichier non trouvé ou Impossible à lire.")
                self.nom_1 = input("Choisir un autre fichier : ")
        while self.lignes_2 is None:
            try:
                self.lignes_2 = self.__lire(self.nom_2)
            except (FileNotFoundError, IOError):
                print("Fichier non trouvé ou Impossible à lire.")
                self.nom_2 = input("Choisir un autre fichier : ")

        print("Début de la fusion")
        print("")
        while len(self.lignes_1) >= 1 or len(self.lignes_2) >= 1:
            self.__inspecte()

        print("")
        sauv = input("Fin de la fusion. Sauvegarder le résultat ? (Y/n) : ")
        while sauv[0] not in ('n', 'N'):
            out = input("Sauvegarder dans le fichier : ")
            try:
                self.__ecrit(out)
                sauv = 'n'
            except IOError:
                print("Impossible d'écrire dans ce fichier.")
                sauv = input("Sauvegarder le résultat ? (Y/N) : ")

if __name__ == '__main__':
    fusion = Fusione()
    fusion.run()
