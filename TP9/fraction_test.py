import unittest
from fraction_corr import Fraction, Divisionparzero, Pasentier, Expneg, Irrationel

class FractionTest(unittest.TestCase):
    def test_init(self):
        fraction = Fraction(1, 2)
        self.assertEqual(fraction.num, 1, "numérateur")
        self.assertEqual(fraction.den, 2, "dénominateur")
        
        fraction = Fraction(-6, 29)
        self.assertEqual(fraction.num, -6, "numérateur")
        self.assertEqual(fraction.den, 29, "dénominateur")
        
        with self.assertRaises(Divisionparzero):
            fraction = Fraction(5, 0)
        
        with self.assertRaises(Pasentier):
            fraction = Fraction(3.7, 1)
            
    def test_str(self):
        fraction = Fraction(2, 3)
        self.assertEqual(str(fraction), '2/3')
        
        fraction = Fraction(6, 24)
        self.assertEqual(str(fraction), '1/4', "simplification")
        
        fraction = Fraction(-8, 6)
        self.assertEqual(str(fraction), '-4/3', "simplification")
        
        fraction = Fraction(-7, -7)
        self.assertEqual(str(fraction), '1/1', "simplification")
    
    def test_mixed(self):
        fraction = Fraction(3, 2)
        self.assertEqual(fraction.as_mixed_number(), '1 + 1/2')
        
        fraction = Fraction(29, 3)
        self.assertEqual(fraction.as_mixed_number(), '9 + 2/3')
        
        fraction = Fraction(-9, 4)
        self.assertEqual(fraction.as_mixed_number(), '-2 + -1/4')

        
    def test_add(self):
        fraction = Fraction(1, 5)
        fraction2 = Fraction(2, 3)
        fraction3 = fraction + fraction2
        self.assertEqual(str(fraction3), '13/15')
        
        fraction = Fraction(-2, 7)
        fraction2 = Fraction(1, 5)
        fraction3 = fraction + fraction2
        self.assertEqual(str(fraction3), '-3/35')
    
    def test_sub(self):
        fraction = Fraction(1, 3)
        fraction2 = Fraction(1, 2)
        fraction3 = fraction - fraction2
        self.assertEqual(str(fraction3), '-1/6')
    
    def test_div(self):
        fraction = Fraction(5, 3)
        fraction2 = Fraction(2, 1)
        fraction3 = fraction/fraction2
        self.assertEqual(str(fraction3), '5/6')
        
        fraction = Fraction(6, 5)
        fraction2 = Fraction(3, 2)
        fraction3 = fraction/fraction2
        self.assertEqual(str(fraction3), '4/5')
        
        fraction = Fraction(48, 3)
        fraction2 = Fraction(-8, 9)
        fraction3 = fraction/fraction2
        self.assertEqual(str(fraction3), '-18/1')
        
        fraction = Fraction(4, 3)
        fraction2 = Fraction(0, 1)
        with self.assertRaises(Divisionparzero):
            fraction3 = fraction/fraction2
    
    def test_pow(self):
        fraction = Fraction(7, 2)
        fraction2 = Fraction(3, 1)
        fraction3 = fraction**fraction2
        self.assertEqual(str(fraction3), '343/8')
        
        fraction = Fraction(25, 9)
        fraction2 = Fraction(1, 2)
        fraction3 = fraction**fraction2
        self.assertEqual(str(fraction3), '5/3')
        
        fraction = Fraction(3, 4)
        fraction2 = Fraction(1, 7)
        with self. assertRaises(Irrationel):
            fraction3 = fraction**fraction2
        
        fraction = Fraction(-8, 3)
        fraction2 = Fraction(2, 1)
        with self.assertRaises(Expneg):
            fraction3 = fraction**fraction2
    
    def test_eq(self):
        fraction = Fraction(-2, 5)
        fraction2 = Fraction(-2, 5)
        self.assertEqual(fraction == fraction2, True)
    
        fraction = Fraction(2, 3)
        fraction2 = Fraction(1, 3)
        self.assertEqual(fraction == fraction2, False)
        
        fraction = Fraction(4, 2)
        fraction2 = Fraction(2, 1)
        self.assertEqual(fraction == fraction2, True)
        
        fraction = Fraction(-5, -6)
        fraction2 = Fraction(5, 6)
        self.assertEqual(fraction == fraction2, True)
        
    def test_int(self):
        fraction = Fraction(1, 2)
        self.assertEqual(fraction.is_integer(), False)
        
        fraction = Fraction(6, 6)
        self.assertEqual(fraction.is_integer(), True)
        
        fraction = Fraction(-2, 5)
        self.assertEqual(fraction.is_integer(), False)
    
    def test_proper(self):
        fraction = Fraction(1, 4)
        self.assertEqual(fraction.is_proper(), True)
        
        fraction = Fraction(-3, 5)
        self.assertEqual(fraction.is_proper(), True)
        
        fraction = Fraction(4, 3)
        self.assertEqual(fraction.is_proper(), False)
        
    def test_adjacent(self):
        fraction = Fraction(8, 7)
        fraction2 = Fraction(15, 7)
        self.assertEqual(fraction.is_adjacent_to(fraction2), True)
        
        fraction = Fraction(9, 11)
        fraction2 = Fraction(2, 5)
        self.assertEqual(fraction.is_adjacent_to(fraction2), False)
        
        fraction = Fraction(-1, -8)
        fraction2 = Fraction(18, 16)
        self.assertEqual(fraction.is_adjacent_to(fraction2), True)


unittest.main()
