def parse_catalyzer_param(line, catalyzer_params_counter):
    try:
        if catalyzer_params_counter == 0:
            value = list(map(int, line.split(',')))
            if int(value[0]) < 1:
                raise ValueError("Error!\nMinimum length of a chemical species to become a catalyst must be at least 1.")
        elif catalyzer_params_counter in [1, 2]:
            value = int(line)
            if value < 0:
                raise ValueError("Error!\nThe number of catalyst species must be non-negative.")
        elif catalyzer_params_counter == 3:
            if line not in ['ON', 'OFF']:
                raise ValueError("Error!\nCondensation and cleavage catalyst must be either 'ON' or 'OFF'.")
            value = line
        else:
            raise ValueError("Error!\nUnexpected number of parameters in the CATALYZERS section.")
    except ValueError:
        raise ValueError("Error!\nCatalyzer values must be integers for the first three lines.")
    return value
