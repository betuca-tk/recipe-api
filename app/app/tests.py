from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        """Test that two numbers are added together"""
        response = calc.add(3, 8)
        self.assertEqual(response, 11)

    def test_subtract_numbers(self):
        """Test that values are subtracted and returned"""
        response = calc.subtract(10, 15)
        self.assertEqual(response, 5)
