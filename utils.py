from classes import CondReactionClass, CllReactionClass 

def flatten_list(lst):
    """
    This function takes a list and returns a new list with all unique elements,
    preserving the order of their first occurrence.
    
    Parameters:
    lst (list): A list to be flattened
    
    Returns:
    list: A flat list containing all unique elements of the input list
    """
    seen = set()
    unique_list = []
    for item in lst:
        if item.name not in seen:
            seen.add(item.name)
            unique_list.append(item)
    return unique_list

def are_reactions_same_no_cata(reaction1, reaction2):
    """Utility function to check if two reactions are the same."""
    if type(reaction1.reaction_class) != type(reaction2.reaction_class):
        return False

    if isinstance(reaction1.reaction_class, CondReactionClass):
        key1 = (tuple(sorted(reaction1.reactants)), tuple(reaction1.product))
        key2 = (tuple(sorted(reaction2.reactants)), tuple(reaction2.product))
    elif isinstance(reaction1.reaction_class, CllReactionClass):
        key1 = (tuple(reaction1.reactants), tuple(sorted([product.name for product in reaction1.product])))
        key2 = (tuple(reaction2.reactants), tuple(sorted([product.name for product in reaction2.product])))
    else:
        return False

    return key1 == key2


def are_reactions_same(reaction1, reaction2):
    """Utility function to check if two reactions are the same."""
    if not are_reactions_same_no_cata(reaction1, reaction2):
        return False
    
    catalyzers_key1 = tuple(sorted(c.species for c in reaction1.reaction_class.catalyzers))
    catalyzers_key2 = tuple(sorted(c.species for c in reaction2.reaction_class.catalyzers))

    return catalyzers_key1 == catalyzers_key2
