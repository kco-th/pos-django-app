
# myapp/tests.py

from django.test import SimpleTestCase
from .calculator import Calculator


class CalculatorTest(SimpleTestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(10, 5), 15)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(10, 5), 50)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 5), 2)
    
    
  
