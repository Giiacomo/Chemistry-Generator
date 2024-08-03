def parse_system_param(line, system_data):
    parts = line.split()
    possible_params = ['ML', 'CLL_ML_ACTIVE', 'D_CONCENTRATION', 'D_CONTRIB']
    if len(parts) != 2 or parts[0] not in possible_params:
        raise ValueError("Error!\nInvalid parameter. Check the documentation to understand more about system parameters!")
    
    setattr(system_data, parts[0], parts[1])
