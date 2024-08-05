from utils.constants import CATALYZER_PARAMS_SECTION

def parse_catalyzer_param(line, catalyzer_params_counter):
    error_msg = f"Error parsing {CATALYZER_PARAMS_SECTION} section:"
    if catalyzer_params_counter == 0:
        if len(line.split(' ')) > 1:
            raise ValueError(f"{error_msg} first row should be a range, ie 1,2")
        catalyzer_lengths = list(map(int, line.split(',')))
        if len(catalyzer_lengths) != 2:
            raise ValueError(f"{error_msg} first row should be a range, ie 1,2")
        if catalyzer_lengths[0] < 1:
            raise ValueError(f"{error_msg} minimum length of a chemical species to become a catalyst must be at least 1.")
        value = catalyzer_lengths
    elif catalyzer_params_counter in [1, 2]:
        try:
            value = int(line)
            if value < 0:
                raise ValueError(f"{error_msg} the number of catalyst species (second or third row) must be non-negative.")
        except ValueError:
            raise ValueError(f"{error_msg} invalid value for the number of catalyst species (second or third row).")
    elif catalyzer_params_counter == 3:
        if line not in ['ON', 'OFF']:
            raise ValueError(f"{error_msg} condensation and cleavage catalyst (last row) must be either 'ON' or 'OFF'.")
        value = line
    else:
        raise ValueError(f"{error_msg} unexpected number of lines for this section.")

    return value
