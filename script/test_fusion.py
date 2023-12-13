import unittest
from fusion import Fusione, MauvaisInput

class TestFusione(unittest.TestCase):
    
    def test_init(self):
        # valeurs par défault
        fusione = Fusione()
        self.assertEqual(fusione.merged, [])
        self.assertEqual(fusione.index_2, 0)
        
        # noms de fichiers donnés
        fusione = Fusione('a.txt', 'b.txt')
        self.assertEqual(fusione.nom_1, 'a.txt')
        self.assertEqual(fusione.nom_2, 'b.txt')
        
        # début
        fusione = Fusione('a.txt', 'b.txt', 2)
        self.assertEqual(fusione.index_1, 2)
        self.assertEqual(fusione.index_2, 2)

    def test_lire(self):
        # lecture
        fusione = Fusione('a.txt', 'b.txt')
        fusione.lignes_1 = fusione._Fusione__lire(fusione.nom_1)
        self.assertEqual(len(fusione.lignes_1), 5)

        # fichier inexistant
        fusione = Fusione('a.txt', 'b.txt')
        with self.assertRaises(FileNotFoundError):
            fusione._Fusione__lire('d.txt')
        
        # fichier pas accessible
        fusione = Fusione('a.txt', 'b.txt')
        with self.assertRaises(IOError):
            fusione._Fusione__lire('/')

    def test_ajout(self):
        # ajout de ligne
        fusione = Fusione('a.txt', 'b.txt')
        fusione.lignes_1 = fusione._Fusione__lire(fusione.nom_1)
        fusione._Fusione__ajout(1)
        self.assertEqual(len(fusione.lignes_1), 4)
        self.assertEqual(fusione.merged, ['abc\n'])
        self.assertEqual(fusione.index_1, 1)

    def test_suppr(self):
        # suppresion de ligne
        fusione = Fusione('a.txt', 'b.txt')
        fusione.lignes_1 = fusione._Fusione__lire(fusione.nom_1)
        fusione._Fusione__suppr(1)
        self.assertEqual(len(fusione.lignes_1), 4)
        self.assertEqual(fusione.merged, [])
        self.assertEqual(fusione.index_1, 1)
        
    def test_idem(self):
        # cas où les lignes sont identiques 
        fusione = Fusione('a.txt', 'b.txt')
        fusione.lignes_1 = fusione._Fusione__lire(fusione.nom_1)
        fusione.lignes_2 = fusione._Fusione__lire(fusione.nom_2)
        fusione._Fusione__idem()
        self.assertEqual(len(fusione.lignes_1), 4)
        self.assertEqual(len(fusione.lignes_2), 4)
        self.assertEqual(fusione.merged, ['abc\n'])
        self.assertEqual(fusione.index_1, 1)
        self.assertEqual(fusione.index_2, 1)

    def test_ecrit(self):
        # écriture du résultat
        fusione = Fusione('a.txt', 'b.txt')
        fusione.lignes_1 = fusione._Fusione__lire(fusione.nom_1)
        fusione.lignes_2 = fusione._Fusione__lire(fusione.nom_2)
        for i in range(3):
            fusione._Fusione__idem()
        fusione._Fusione__ecrit('out.txt')
        with open('out.txt', encoding = 'utf8') as fichier:
            test_out = fichier.readlines()
        self.assertEqual(fusione.merged, test_out)

        # fichier pas accessible
        fusione = Fusione('a.txt', 'b.txt')
        fusione.lignes_1 = fusione._Fusione__lire(fusione.nom_1)
        fusione.lignes_2 = fusione._Fusione__lire(fusione.nom_2)
        for i in range(3):
            fusione._Fusione__idem()
        with self.assertRaises(IOError):
            fusione._Fusione__ecrit('/out.txt')


unittest.main()
