from classes import CondReactionClass, CllReactionClass
from utils.constants import REACTIONS_SECTION

def parse_reactions(line, data):
    error_msg = f'Error parsing {REACTIONS_SECTION} section:'

    parts = line.split()
    if len(parts) != 3:
        raise ValueError(f"{error_msg} condensation correct form:\n<reactant_1> <reactant_2> <reaction_speed>\nCleavage correct form:\n<reactant> <reaction_speed> <n_split> [<cleavage_point>]")
    
    reactant_1 = parts[0]
    reactant_2 = parts[1] # can be a string or a number based on the reaction type
    reaction_speed = parts[-1]

    if reactant_1.startswith("R-") and reactant_2.endswith("-R"): # condensation reaction
        try:
            reaction_speed = float(reaction_speed)
            data["reactions"]["conds"].append(CondReactionClass(reactant_1, reactant_2, reaction_speed))
        except ValueError:
            raise ValueError(f"{error_msg} reaction speed must be a float.")
    elif reactant_1.startswith("R-") and reactant_1.endswith("-R"):
        try:
            n_split = int(parts[1])
            reaction_speed = float(reaction_speed)
            if n_split >= len(reactant_1):
                raise RuntimeError(f"{error_msg} the value of the third parameter for cleavage reaction class must be less than the size of the defined string\nFor example R-AABBA-R, n_split must be < 5!")
            data["reactions"]["clls"].append(CllReactionClass(reactant_1, n_split, reaction_speed))
        except ValueError:
            raise ValueError(f"{error_msg} n_split, and reaction speed must be integers and float respectively.")
    else:
        raise ValueError(f"{error_msg} invalid format for reaction '{line}'.")

