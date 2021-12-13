import unittest

from context import tmm
from tmm.payload.PayloadParser import PayloadParser

"""
This class tests the regular expressions used to extract numbers and units of measurements from strings.
"""
class TestRegEx(unittest.TestCase):

    # numbers
    def test_extract_numbers_temperature(self):
        self.assertEqual(PayloadParser.extract_numbers_from_string("19.9 °C")[0], "19.9")

    def test_extract_numbers_moisture(self):
        self.assertEqual(PayloadParser.extract_numbers_from_string("23.5 %")[0], "23.5")

    def test_extract_numbers_voltage(self):
        self.assertEqual(PayloadParser.extract_numbers_from_string("3.6534 V")[0], "3.6534")

    def test_extract_numbers_conductivity(self):
        self.assertEqual(PayloadParser.extract_numbers_from_string("55 uS/cm")[0], "55")

    # units
    def test_extract_units_temperature(self):
        self.assertEqual(PayloadParser.extract_units_from_string("19.9 °C")[0], "°C")

    def test_extract_units_moisture(self):
        self.assertEqual(PayloadParser.extract_units_from_string("23.5 %")[0], "%")

    def test_extract_units_voltage(self):
        self.assertEqual(PayloadParser.extract_units_from_string("3.6534 V")[0], "V")

    def test_extract_units_conductivity(self):
        self.assertEqual(PayloadParser.extract_units_from_string("55 uS/cm")[0], "uS/cm")

if __name__ == '__main__':
    unittest.main()
    
    