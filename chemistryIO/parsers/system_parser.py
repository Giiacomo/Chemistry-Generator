def parse_system_param(line, system_data):
    parts = line.split()
    possible_params = list(system_data.__dict__.keys())
    if len(parts) != 2:
        raise ValueError("Invalid parameter format: {}. Check the documentation to understand more about system parameters!".format(line))    
    if parts[0] not in possible_params:
        raise ValueError("Invalid parameter: {}. Check the documentation to understand more about system parameters!".format(parts[0]))
    try:
        setattr(system_data, parts[0], parts[1])
    except Exception as e:
        raise ValueError("Error setting parameter: {}. Reason: {}".format(parts[0], str(e)))
