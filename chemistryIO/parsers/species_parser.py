from classes import Species

def parse_species(line):
    parts = line.split()
    # Check for the minimum required number of parts
    if len(parts) < 4:
        raise ValueError("Error!\nSpecies correct form:\n<speciename> <concentration> <contribution> <can_cross_membrane> [external_concentration] [diffusion_constant]")
    
    # Extract the mandatory fields
    name = parts[0]
    concentration = float(parts[1])
    contrib = float(parts[2])
    can_cross_membrane = parts[3].upper() == 'T'
    
    external_concentration = None
    diffusion_constant = None

    if len(parts) > 4:
        try:
            external_concentration = float(parts[4])
        except ValueError:
            pass  
    
    if len(parts) > 5:
        try:
            diffusion_constant = float(parts[5])
        except ValueError:
            pass  

    return Species(name, concentration, contrib, can_cross_membrane, external_concentration, diffusion_constant)


