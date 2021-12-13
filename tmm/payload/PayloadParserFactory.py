from .PayloadParser import PayloadParser
from .DraginoLSE01 import DraginoLSE01

"""
This class produces PayloadParser instances, depending on the brand and model 
of a sensor.

It keeps a local cache of instantiated parsers and returns the same instance,
once it has been created.
"""
__parsers = {}

def _get_instance(brand: str, model: str) -> PayloadParser:
        return __parsers[brand + "_" + model]

def _set_instance(brand: str, model: str, instance: PayloadParser):
    __parsers[brand + "_" + model] = instance

def get_parser_for_model(brand: str, model: str) -> PayloadParser:
    if(brand == "dragino"):
        if(model == "lse01"):
            try:
                return _get_instance(brand=brand, model=model)
            except:
                dragino = DraginoLSE01()
                _set_instance(brand=brand, model=model, instance=dragino)
                
    return _get_instance(brand=brand, model=model)
        
