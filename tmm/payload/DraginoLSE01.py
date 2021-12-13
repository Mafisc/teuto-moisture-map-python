from .PayloadParser import PayloadParser

class DraginoLSE01(PayloadParser):

    def parse_payload(self, payload : str) -> dict :

        retval = dict()

        # Extracting the values from the message is specific to the sensor used
        # This implementation supports only the dragoni sensor as of now
        bat_value = payload["uplink_message"]["decoded_payload"]["Bat"]
        conductivity_value = payload["uplink_message"]["decoded_payload"]["conduct_SOIL"]
        temp_value = payload["uplink_message"]["decoded_payload"]["temp_SOIL"]
        moisture_value = payload["uplink_message"]["decoded_payload"]["water_SOIL"]

        retval["battery"]  = float(self.extract_numbers_from_string(bat_value)[0])
        retval["conductivity"] = float(self.extract_numbers_from_string(conductivity_value)[0])
        retval["temperature"] = float(self.extract_numbers_from_string(temp_value)[0])
        retval["moisture"] = float(self.extract_numbers_from_string(moisture_value)[0])

        retval["battery_unit"] = str(self.extract_units_from_string(bat_value)[0])
        retval["conductivity_unit"] = str(self.extract_units_from_string(conductivity_value)[0])
        retval["temperature_unit"] = str(self.extract_units_from_string(temp_value)[0])
        retval["moisture_unit"] = str(self.extract_units_from_string(moisture_value)[0])

        return retval
        
        
