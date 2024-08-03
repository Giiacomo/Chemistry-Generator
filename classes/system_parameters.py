class SystemParameters:
    def __init__(self):
        self.ML = None
        self.CLL_ML_ACTIVE = None
        self.D_CONCENTRATION = None
        self.D_CONTRIB = None

    def validate(self):
        required_params = {'ML', 'CLL_ML_ACTIVE', 'D_CONCENTRATION', 'D_CONTRIB'}
        missing = required_params - self.__dict__.keys()
        if missing:
            raise ValueError(f"Missing system parameters: {', '.join(missing)}")
