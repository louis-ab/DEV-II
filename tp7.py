class Divisionparzero(Exception):
    """Divison par zéro."""
class Pasentier(Exception):
    """Le nombre devrait être entier mais ne l'est pas."""
class Expneg(Exception):
    """Exponentiation par un nombre négatif."""
class Irrationel(Exception):
    """Le résulatat est irrationel."""

class Fraction:
    """Class representing a fraction and operations on it

    Author : V. Van den Schrieck
    Date : October 2021
    This class allows fraction manipulations through several operations.
    """

    def __init__(self,num=0, den=1):
        """This builds a fraction based on some numerator and denominator.

        PRE : -
        POST : Crée l'objet Fraction avec num/den si den != 0
        RAISES : Divisionparzero si den = 0, Pasentier si num et/ou den n'est pas un int
        """
        if den == 0:
            raise Divisionparzero("Le dénominateur est 0")
        if num%1 or den%1:
            raise Pasentier("Le numérateur et/ou le dénominateur n'es pas entier")
        self.num = num
        self.den = den

    @property
    def numerator(self):
        """Permet de retourner le numérateur de la fraction.
        PRE : -
        POST : Renvoie le numérateur de la fraction
        """
        return self.num

    @property
    def denominator(self):
        """Permet de retourner le dénominateur de la fraction.
        PRE : -
        POST : Renvoie le dénominateur de la fraction
        """
        return self.den

# ------------------ Textual representations ------------------

    def __str__(self) :
        """Return a textual representation of the reduced form of the fraction

        PRE : -
        POST : une représentation textuelle de la fraction réduite
        """
        num = self.num
        den = self.den
        for div in range(2,num+1):
            if den%div == 0 and num%div == 0:
                num = int(num/div)
                den = int(den/div)
        return f"{num}/{den}"

    def as_mixed_number(self) :
        """Return a textual representation of the reduced form of the fraction as a mixed number

        A mixed number is the sum of an integer and a proper fraction

        PRE : -
        POST : la représentation mixte de la fraction. Par exemple : 3/2 -> "1 + 1/2"
        """
        n = self.num/self.den
        num = self.num
        sign = n>=0
        entier = 0
        if sign:
            while num > 1:
                num -= self.den
                entier += 1
        else:
            while num < -1:
                num += self.den
                entier -= 1
        if num == 0:
            return f"{entier}"
        if entier == 0:
            return f"{num}/{self.den}"
        return f"{entier} + {num}/{self.den}"


# ------------------ Operators overloading ------------------

    def __add__(self, other):
        """Overloading of the + operator for fractions

         PRE : other est un objet Fraction à ajouter
         POST : renvoie leur somme sous forme d'un nouvel objet Fraction
         """
        return Fraction(self.num*other.den + other.num*self.den, self.den * other.den)


    def __sub__(self, other):
        """Overloading of the - operator for fractions

        PRE : other est un objet Fraction à soustraire à self
        POST : leur différence, un objet Fraction
        """
        return self + Fraction(-other.num,other.den)


    def __mul__(self, other):
        """Overloading of the * operator for fractions

        PRE : other est un objet Fraction par lequel multiplier l'objet
        POST : leur produit, un objet Fraction
        """
        return Fraction(self.num*other.num, self.den*other.den)


    def __truediv__(self, other):
        """Overloading of the / operator for fractions

        PRE : other est un objet Fraction par lequel diviser l'objet
        POST : leur division qui est un objet Fraction
        RAISES : Divisionparzero si other = 0
        """
        if other.num == 0:
            raise Divisionparzero("Le dénominateur est 0")
        return self * Fraction(other.den,other.num)

    def __pow__(self, other):
        """Overloading of the ** operator for fractions

        PRE : other est un objet Fraction
        POST : self**other, une Fraction
        RAISES : - Expneg si le nombre exponencé est négatif,
                 - Irrationel si le résultat serait irrationel
        """

        # (a/b)^(c/d) = (a/b)^c * (a/b)^(1/d) = (a^c * a^(1/d) / b^c * b^(1/d))
        if self.num < 0 or self.den < 0:
            raise Expneg("le nombre exponencé est négatif")
        a = pow(self.num,1/other.den)
        b = pow(self.den,1/other.den)
        if a%1 == 0 and b%1 == 0:
            return Fraction(int(pow(self.num,other.num)*a), int(pow(self.den,other.num)*b))
        raise Irrationel("le résultat est irrationel")



    def __eq__(self, other):
        """Overloading of the == operator for fractions

        PRE : other est un objet Fraction
        POST : True si il est égal à l'objet, False sinon
        """
        return self.as_mixed_number() == other.as_mixed_number()


    def __float__(self) :
        """Returns the decimal value of the fraction

        PRE : -
        POST : renvoie un float de valeur équivalente à l'objet Fraction
        """
        return self.num/self.den

# TODO : [BONUS] You can overload other operators if you wish (ex : <, >, ...)



# ------------------ Properties checking  ------------------

    def is_zero(self):
        """Check if a fraction's value is 0

        PRE : -
        POST : True si l'objet est égal à 0, False sinon
        """
        return self.num == 0


    def is_integer(self):
        """Check if a fraction is integer (ex : 8/4, 3, 2/2, ...)

        PRE : -
        POST : 1 si l'objet est un entier, 0 sinon
        """
        return not self.num % self.den

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1

        PRE : -
        POST : True si l'objet est <1, False sinon
        """
        if self.den > 0:
            return self.num < self.den
        return self.num > -self.den

    def is_unit(self):
        """Check if a fraction's numerator is 1 in its reduced form

        PRE : -
        POST : 1 si l'objet est de forme 1/n dans sa forme réduite, 0 sinon
        """
        return not self.den % self.num

    def is_adjacent_to(self, other) :
        """Check if two fractions differ by a unit fraction

        Two fractions are adjacents if the absolute value of the difference between them is
            a unit fraction

        PRE : other est une objet fraction
        POST : 1 si other et l'objet sont adjacents, 0 sinon
        """
        diff = self - other
        return diff.is_unit()

if __name__ == '__main__':
    test = Fraction(2,1)
    test2 = Fraction(4,1)
    print("Fraction : ", test2)
    print("Mixed : ", test2.as_mixed_number())
    print("Adjacents : ", test2.is_adjacent_to(test))
    print("Proper : ", test2.is_proper())
    print("Integer : ", test2.is_integer())
    test3 = test**test2
    print("Exp : ", test3)

    print("")
    test4 = Fraction(1,2)
    test5 = Fraction(2,3)
    print("Mixed : ", test4.as_mixed_number())
    print("Sum : ", test4+test5)
    print("Product : ", test4*test5)
    print("Equal : ", test4 == test5)
    print("Float : ", float(test5))
    print("Unit : ", test5.is_unit())


    # division par 0:
    test6 = Fraction(1,0)
