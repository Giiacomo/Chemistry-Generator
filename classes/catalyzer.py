
from .reaction_class import CondReactionClass, CllReactionClass

class Catalyzer:
    def __init__(self, catalyzer_species):
        self.species = catalyzer_species
        self.reactions = []

    def is_cond_catalyzer(self):
        return any(isinstance(reaction, CondReactionClass) for reaction in self.reactions)

    def get_cond_reaction_classes(self):
        return [r for r in self.reactions if isinstance(r, CondReactionClass)]
    
    def is_cll_catalyzer(self):
        return any(isinstance(reaction, CllReactionClass) for reaction in self.reactions)

    def get_cll_reaction_classes(self):
        return [r for r in self.reactions if isinstance(r, CllReactionClass)]


    def add_reaction_class(self, reaction):
        self.reactions.append(reaction)

    def get_n_catalyzed_reactions(self):
        n_catalyzed_reactions = {
            'n_cata_gen_reactions': 0,
            'n_cata_gen_cond': 0,
            'n_cata_gen_cll': 0,
        }
        for reaction in self.reactions:
            if isinstance(reaction, CondReactionClass):
                n_catalyzed_reactions['n_cata_gen_cond'] += len(reaction.generated_reactions)
            if isinstance(reaction, CllReactionClass):
                n_catalyzed_reactions['n_cata_gen_cll'] += len(reaction.generated_reactions)

        n_catalyzed_reactions['n_cata_gen_reactions'] = n_catalyzed_reactions['n_cata_gen_cll'] + n_catalyzed_reactions['n_cata_gen_cond']

        return n_catalyzed_reactions
