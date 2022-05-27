import unittest

import json

import tmm.payload.PayloadParserFactory as ppf
from os.path import dirname, join

class TestDraginoParser(unittest.TestCase):

    """
    Using a slightly modified original JSON palyoad, sent be a registered Dragino sensor via TTN, 
    this test checks whether the required are successfully extracted and returned as a dictionary with the 
    proper keys.
    """
    def test_parse_payload(self):
        dragino_parser = ppf.get_parser_for_model(brand="dragino", model="lse01")
        project_root_path = dirname(dirname(__file__)) 
        filepath = f"{project_root_path}/test/dragino_ttn_payload.json"
        
        with open(filepath, 'r') as file:
            payload = json.load(file)
            data = dragino_parser.parse_payload(payload)

            self.assertEqual(data["battery"], 3.304, "Battery value not ok")
            self.assertEqual(data["conductivity"], 57, "Conductivity value not ok")
            self.assertEqual(data["temperature"], 7.87, "Temperature value not ok")
            self.assertEqual(data["moisture"], 23.42, "Moisture value not ok")

            self.assertEqual(data["battery_unit"], "V", "Battery unit not ok")
            self.assertEqual(data["conductivity_unit"], "uS/cm", "Conductivity unit not ok")
            self.assertEqual(data["temperature_unit"], "°C", "Temperature unit not ok")
            self.assertEqual(data["moisture_unit"], "%", "Moisture unit not ok")


if __name__ == '__main__':
    unittest.main()
    
    