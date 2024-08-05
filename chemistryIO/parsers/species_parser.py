from classes import Species
from utils.constants import SPECIES_INPUT_FORM

def parse_species(line):
    parts = line.split()
    if len(parts) < 4:
        raise ValueError("Error!\nSpecies correct form:\n<speciename> <concentration> <contribution> <can_cross_membrane> [external_concentration] [diffusion_constant]")
    
    name = parts[0]
    try:
        concentration = float(parts[1])
        contrib = float(parts[2])
    except ValueError:
        raise ValueError(f"{SPECIES_INPUT_FORM[1]} (2 col) and {SPECIES_INPUT_FORM[2]} (3 col) for species should be floats.")

    if parts[3].upper() not in ['T', 'F']:
        raise ValueError(f"{SPECIES_INPUT_FORM[3]} (4 col) should be 'T' or 'F'.")
    
    can_cross_membrane = parts[3].upper() == 'T'

    external_concentration = None
    diffusion_constant = None

    if can_cross_membrane:
        if len(parts) > 4:
            try:
                external_concentration = float(parts[4])
            except ValueError:
                raise ValueError("External concentration should be a float.")
        
        if len(parts) > 5:
            try:
                diffusion_constant = float(parts[5])
            except ValueError:
                raise ValueError("Diffusion constant should be a float.")
    
    return Species(name, concentration, contrib, can_cross_membrane, external_concentration, diffusion_constant)
