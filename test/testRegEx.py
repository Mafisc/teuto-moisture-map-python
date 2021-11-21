import unittest

from context import tmm
from tmm import app

class TestRegEx(unittest.TestCase):

    def test_extract_numbers_temperature(self):
        self.assertEqual(app.extract_numbers_from_string("19.9 °C"), ["19.9"])

    def test_extract_numbers_moisture(self):
        self.assertEqual(app.extract_numbers_from_string("23.5 %"), ["23.5"])

    def test_extract_numbers_voltage(self):
        self.assertEqual(app.extract_numbers_from_string("3.6534 V"), ["3.6534"])

    def test_extract_numbers_conductivity(self):
        self.assertEqual(app.extract_numbers_from_string("55 uS/cm"), ["55"])

if __name__ == '__main__':
    unittest.main()
    
    