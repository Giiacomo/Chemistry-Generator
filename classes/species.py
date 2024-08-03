from .reaction_class import CondReactionClass, CllReactionClass

class Species:
    def __init__(self, name, concentration, contrib, is_in_initial_set=False):
        self.name = name
        self.concentration = concentration
        self.contrib = contrib
        self.generator_reactions = []
        self.is_in_initial_set = is_in_initial_set

    def add_generator_reaction(self, reaction):
        if reaction not in self.generator_reactions:
            self.generator_reactions.append(reaction)

    def get_generator_reaction_info(self):
        info = {
            'n_generator_reaction': 0,
            'n_generator_cond_reaction': 0,
            'n_generator_cll_reaction': 0,
            'n_catalyzers': 0,
            'n_cond_catalyzers': 0,
            'n_cll_catalyzers': 0,
            'list_unique_catalyzers': []
        }
        info["n_generator_reaction"] = len(self.generator_reactions)
        info["n_generator_cond_reaction"] = len([r for r in self.generator_reactions if isinstance(r.reaction_class, CondReactionClass)])
        info["n_generator_cll_reaction"] = len([r for r in self.generator_reactions if isinstance(r.reaction_class, CllReactionClass)])
        
        unique_catalyzers = set()

        for r in self.generator_reactions:
            for cata in r.reaction_class.catalyzers:
                if cata not in unique_catalyzers:
                    unique_catalyzers.add(cata)
                    info['n_catalyzers'] += 1
                    if isinstance(r.reaction_class, CondReactionClass):
                        info['n_cond_catalyzers'] += 1
                    if isinstance(r.reaction_class, CllReactionClass):
                        info['n_cll_catalyzers'] += 1
                        
        info['list_unique_catalyzers'] = list(unique_catalyzers)

        return info