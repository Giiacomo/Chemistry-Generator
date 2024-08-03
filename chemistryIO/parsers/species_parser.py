from classes import Species

def parse_species(line):
    parts = line.split()
    if len(parts) != 3:
        raise ValueError("Error!\nSpecies correct form:\n<speciename> <concentration> <contribution>")
    name, concentration, contrib = parts
    return Species(name, float(concentration), float(contrib), is_in_initial_set=True)
