import configparser
from utils.constants import CONFIG_FILE

class ConfigHandler:
    _instance = None

    def __new__(cls, config_file):
        if cls._instance is None:
            cls._instance = super(ConfigHandler, cls).__new__(cls)
            cls._instance._initialize(config_file)
        return cls._instance

    def _initialize(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def _convert_to_boolean(self, value):
        if isinstance(value, str):
            value = value.strip().lower()
            if value in {'true', 'yes', '1'}:
                return True
            elif value in {'false', 'no', '0'}:
                return False
        return value

    def _convert_to_number(self, value):
        try:
            return float(value)
        except ValueError:
            return value

    def _get_property(self, section, key):
        value = self.config.get(section, key, fallback=None)
        if section == 'DEBUG':
            return self._convert_to_boolean(value)
        if section == 'CHEMISTRY':
            return self._convert_to_number(value)
        return value

    def __getattr__(self, name):
        if name in self.config['DEFAULT']:
            return self._get_property('DEFAULT', name)
    
        if name in self.config['DEBUG']:
            return self._get_property('DEBUG', name)
        
        if name in self.config['CHEMISTRY']:
            return self._get_property('CHEMISTRY', name)
        
        raise AttributeError(f"ConfigHandler has no property '{name}'")

config_handler = ConfigHandler(CONFIG_FILE)
