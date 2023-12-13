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
        self.__num = num
        self.__den = den

    @property
    def num(self):
        """Permet de retourner le numérateur de la fraction.
        PRE : -
        POST : Renvoie le numérateur de la fraction
        """
        return self.__num

    @property
    def den(self):
        """Permet de retourner le dénominateur de la fraction.
        PRE : -
        POST : Renvoie le dénominateur de la fraction
        """
        return self.__den
    
    @num.setter
    def num(self, num):
        if type(num) is int:
            self.__num = num
        else:
            raise Pasentier
    
    @den.setter
    def den(self, den):
        if type(den) is int:
            self.__den = den
        else:
            raise Pasentier

# ------------------ Textual representations ------------------

    def __str__(self) :
        """Return a textual representation of the reduced form of the fraction

        PRE : -
        POST : une représentation textuelle de la fraction réduite
        """
        num = self.__num
        den = self.__den
        sign = 1
        if num < 0:
            num = -num
            sign = -sign
        if den < 0:
            den = -den
            sign = -sign
        for div in range(2,num+1):
            if den%div == 0 and num%div == 0:
                num = int(num/div)
                den = int(den/div)
        if sign == 1:
            return f"{num}/{den}"
        else:
            return f"-{num}/{den}"

    def as_mixed_number(self) :
        """Return a textual representation of the reduced form of the fraction as a mixed number

        A mixed number is the sum of an integer and a proper fraction

        PRE : -
        POST : la représentation mixte de la fraction. Par exemple : 3/2 -> "1 + 1/2"
        """
        n = self.__num/self.__den
        num = self.__num
        sign = n>=0
        entier = 0
        if sign and num >= 0:
            while num >= self.__den:
                num -= self.__den
                entier += 1
        elif sign:
            while num <= self.__den:
                num -= self.__den
                entier += 1
        else:
            while num <= -self.__den:
                num += self.__den
                entier -= 1
        if num == 0:
            return f"{entier}"
        if entier == 0:
            return str(Fraction(num, self.den))
        return f"{entier} + {str(Fraction(num, self.den))}"


# ------------------ Operators overloading ------------------

    def __add__(self, other):
        """Overloading of the + operator for fractions

         PRE : other est un objet Fraction à ajouter
         POST : renvoie leur somme sous forme d'un nouvel objet Fraction
         """
        return Fraction(self.__num*other.den + other.num*self.__den, self.__den * other.den)


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
        return Fraction(self.__num*other.num, self.__den*other.den)


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

        # (a/b)^(c/d) = ((a/b)^c)^(1/d) = (a^c/d / b^c/d)
        if self.__num < 0 or self.__den < 0:
            raise Expneg("le nombre exponencé est négatif")
        a = pow(self.__num,1/other.den)
        b = pow(self.__den,1/other.den)
        if a%1 == 0 and b%1 == 0:
            return Fraction(int(pow(self.__num, other.num/other.den)), int(pow(self.__den, other.num/other.den)))
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
        return self.__num/self.__den

# TODO : [BONUS] You can overload other operators if you wish (ex : <, >, ...)



# ------------------ Properties checking  ------------------

    def is_zero(self):
        """Check if a fraction's value is 0

        PRE : -
        POST : True si l'objet est égal à 0, False sinon
        """
        return self.__num == 0


    def is_integer(self):
        """Check if a fraction is integer (ex : 8/4, 3, 2/2, ...)

        PRE : -
        POST : 1 si l'objet est un entier, 0 sinon
        """
        return not self.__num % self.__den

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1

        PRE : -
        POST : True si l'objet est <1, False sinon
        """
        if self.__den > 0:
            return self.__num < self.__den
        return self.__num > -self.__den

    def is_unit(self):
        """Check if a fraction's numerator is 1 in its reduced form

        PRE : -
        POST : 1 si l'objet est de forme 1/n dans sa forme réduite, 0 sinon
        """
        return not self.__den % self.__num

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

    test5.num = 5
    print(test5)
    print(test5.num)

    # division par 0:
    test6 = Fraction(1,0)
