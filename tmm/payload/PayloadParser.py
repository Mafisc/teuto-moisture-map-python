from abc import ABC, abstractmethod
import re

class PayloadParser(ABC):

    """ 
    Extracts numerical values from strings
    """
    @staticmethod
    def extract_numbers_from_string(string :str) -> float:
        return re.findall("^\d+[.]*\d*", string)

    """
    Extracts the unit of measurements from strings 
    """
    @staticmethod
    def extract_units_from_string(string: str) -> str: 
        return re.findall("[\w]*[°/%]*\w*$", string)
        
    
    @abstractmethod
    def parse_payload(self, payload : str) -> dict :
        pass