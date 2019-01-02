import importlib
import logging

class BaseParser:
    def preprocess(self, payload):
        return [None]

    def make_suggestion(self, item):
        return item

SMARTIMPORT_PARSERS = {
    '1': ('otp', 'OTP'),
    '2': ('regular', 'Regular'),
    '3': ('mixed', 'Mixed'),
    '4': ('raw', 'Raw')
}

def dispatch(type):
    type = str(type)
    if type not in SMARTIMPORT_PARSERS:
        return None
    try:
        module_name = SMARTIMPORT_PARSERS[type][0]
        module = importlib.import_module('smartimport.parsers.' + module_name)
        return module.dispatch()
    except Exception as e:
        logging.error(str(e))
        raise
    return None
