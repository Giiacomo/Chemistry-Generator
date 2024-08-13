from time import sleep
from classes import CondReactionClass, CllReactionClass
from termcolor import colored
import sys
from classes.generated_reaction import GeneratedReaction
from utils.logger import Logger

def flatten_species_list(lst):
    seen = set()
    unique_list = []
    for item in lst:
        if item.name not in seen:
            seen.add(item.name)
            unique_list.append(item)
    return unique_list

def add_species_if_not_exists(products, species_list):
    existing_species_names = {species.name for species in species_list}
    for product in products:  
        species_name = product.name
        if species_name not in existing_species_names:
            species_list.append(product)  
            existing_species_names.add(species_name) 


def are_reactions_same_no_cata(reaction1, reaction2):
    if type(reaction1.reaction_class) != type(reaction2.reaction_class):
        return False
    
    if isinstance(reaction1.reaction_class, CondReactionClass):
        key1 = (tuple(sorted(reaction1.reactants)), tuple(product.name for product in reaction1.product))
        key2 = (tuple(sorted(reaction2.reactants)), tuple(product.name for product in reaction2.product))
    elif isinstance(reaction1.reaction_class, CllReactionClass):
        key1 = (tuple(sorted(reaction1.reactants)), tuple(sorted(product.name for product in reaction1.product)))
        key2 = (tuple(sorted(reaction2.reactants)), tuple(sorted(product.name for product in reaction2.product)))
    else:
        return False
    return key1 == key2


def are_reactions_same(reaction1, reaction2):
    same_reaction_no_cata = are_reactions_same_no_cata(reaction1, reaction2)
    same_reaction_class = reaction1.get_reaction_class() == reaction2.get_reaction_class()
    return same_reaction_no_cata and same_reaction_class 


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


    
