from classes import CondReactionClass, CllReactionClass, LengthClass

def parse_reactions(line, data):
    parts = [part.replace("R-", "").replace("-R", "") for part in line.split()]
    if len(parts) != 3:
        raise ValueError(
            "Error!\nCondensation correct form:\n<reactant_1> <reactant_2> <reaction_speed>\nCleavage correct form:\n<reactant> <reaction_speed> <n_split>"
        )
    try:
        reaction_speed = float(parts[-1])
        if parts[1].isdigit():
            n_split = int(parts[1])
            if n_split >= len(parts[0]):
                raise RuntimeError("Error!\nThe value of the third parameter for cleavage reaction class must be less than the size of the defined string\nFor example R-AABBA-R, n_split must be < 5!")
            data["reactions"]["clls"].append(CllReactionClass(parts[0], n_split, reaction_speed))
        else:
            data["reactions"]["conds"].append(CondReactionClass(parts[0], parts[1], reaction_speed))
    except ValueError:
        raise ValueError("Error!\nReaction speed must be a float.")

def parse_len_classes(line):
    parts = line.split()
    if len(parts) != 4:
        raise ValueError("Error!\nLEN_CLASSES correct form:\n<class lengths> <p_cata_cond> <p_cata_cll> <specificity>")
    classes = parts[0].replace('[', '').replace(']', '').split(',')
    return [LengthClass(classes, parts[1], parts[2], parts[3])]
