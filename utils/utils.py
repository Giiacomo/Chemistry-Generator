from classes import CondReactionClass, CllReactionClass
from termcolor import colored

def flatten_species_list(lst):
    seen = set()
    unique_list = []
    for item in lst:
        if item.name not in seen:
            seen.add(item.name)
            unique_list.append(item)
    return unique_list

def are_reactions_same_no_cata(reaction1, reaction2):
    if type(reaction1.reaction_class) != type(reaction2.reaction_class):
        return False

    if isinstance(reaction1.reaction_class, CondReactionClass):
        key1 = (tuple(sorted(reaction1.reactants)), tuple(sorted(reaction1.product[0].name)))
        key2 = (tuple(sorted(reaction2.reactants)), tuple(sorted(reaction2.product[0].name)))
    elif isinstance(reaction1.reaction_class, CllReactionClass):
        key1 = (tuple(sorted(reaction1.reactants)), tuple(sorted([product.name for product in reaction1.product])))
        key2 = (tuple(sorted(reaction2.reactants)), tuple(sorted([product.name for product in reaction2.product])))
    else:
        return False

    return key1 == key2

def are_reactions_same(reaction1, reaction2):
    catalyzers_key1 = tuple(sorted(c.species for c in reaction1.reaction_class.catalyzers))
    catalyzers_key2 = tuple(sorted(c.species for c in reaction2.reaction_class.catalyzers))

    same_reaction_no_cata = are_reactions_same_no_cata(reaction1, reaction2)

    return same_reaction_no_cata and catalyzers_key1 == catalyzers_key2


def print_debug_message(message, type):
    match type:
        case 'INFO':
            print(f"{colored('[INFO] ', 'green')}{message}")
        case 'WARNING':
            print(f"{colored('[WARNING] ', 'yellow')}{message}")
        case 'ERROR':
            print(f"{colored('[ERROR] ', 'red')}{message}")
        case _:
            print(message)


    
