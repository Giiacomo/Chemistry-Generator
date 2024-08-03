from .reaction_class import CondReactionClass, CllReactionClass

class Catalyzer:
    def __init__(self, catalyzer_species):
        self.species = catalyzer_species
        self.reactions = []

    def is_cond_catalyzer(self):
        for reaction in self.reactions:
            if isinstance(reaction, CondReactionClass):
                return True
        return False

    def get_cond_reaction_classes (self):
        cond_reaction_classes = []
        for r in self.reactions:
            if isinstance(r, CondReactionClass):
                cond_reaction_classes.append(r)
        return cond_reaction_classes

    def get_cll_reaction_classes (self):
        cll_reaction_classes = []
        for r in self.reactions:
            if isinstance(r, CllReactionClass):
                cll_reaction_classes.append(r)
        return cll_reaction_classes

    def is_cll_catalyzer(self):
        for reaction in self.reactions:
            if isinstance(reaction, CllReactionClass):
                return True
        return False

    def add_reaction_class(self, reaction):
        self.reactions.append(reaction)

    def get_n_catalyzed_reactions (self):
        n_catalyzed_reactions = {   'n_cata_gen_reactions': 0,
                                    'n_cata_gen_cond': 0,
                                    'n_cata_gen_cll': 0,
                                }
        for reaction in self.reactions:
            if isinstance(reaction, CondReactionClass):
                for gen_r in reaction.generated_reactions:
                    n_catalyzed_reactions['n_cata_gen_cond'] += 1
            if isinstance(reaction, CllReactionClass):
                for gen_r in reaction.generated_reactions:
                    n_catalyzed_reactions['n_cata_gen_cll'] += 1


        n_catalyzed_reactions['n_cata_gen_reactions'] = n_catalyzed_reactions['n_cata_gen_cll'] + n_catalyzed_reactions['n_cata_gen_cond']

        return n_catalyzed_reactions