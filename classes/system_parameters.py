from utils.constants import CLL_ML_ACTIVE

class SystemParameters:
    def __init__(self):
        self.ML = None
        self.CLL_ML_ACTIVE = None

    def set_CLL_ML_ACTIVE(self, value):
        if value == 'ON':
            setattr(self, CLL_ML_ACTIVE, True)
        elif value == 'OFF':
            setattr(self, CLL_ML_ACTIVE, False)
        else:
            raise ValueError(f"{CLL_ML_ACTIVE} parameter must be 'ON' or 'OFF'")

    def validate(self):
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is None:
                raise ValueError(f"{attr_name} parameter cannot be None")
            
        if self.ML and not str(self.ML).isdigit():
            raise ValueError("ML parameter must be an integer")

        if self.CLL_ML_ACTIVE not in ['ON', 'OFF']:
            raise ValueError(f"{CLL_ML_ACTIVE} parameter must be 'ON' or 'OFF'")
        
        self.set_CLL_ML_ACTIVE(self.CLL_ML_ACTIVE)
