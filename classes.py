class SystemParameters:
    def __init__(self):
        self.ML = None
        self.CLL_ML_ACTIVE = None
        self.D_CONCENTRATION = None
        self.D_CONTRIB = None

    def validate(self):
        required_params = {'ML', 'CLL_ML_ACTIVE', 'D_CONCENTRATION', 'D_CONTRIB'}
        missing = required_params - self.__dict__.keys()
        if missing:
            raise ValueError(f"Missing system parameters: {', '.join(missing)}")

class LengthClass:
    def __init__(self, len, p_cond, p_cll, specificity):
        self.len = len
        self.p_cond = p_cond
        self.p_cll = p_cll
        self.specificity = specificity

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

class ReactionClass:
    def __init__(self, reaction_speed):
        self.reaction_speed = reaction_speed
        self.generated_reactions = [] # Reaction
        self.catalyzers = []

    def add_catalyzer(self, catalyzer):
        self.catalyzers.append(catalyzer)

    def add_generated_reaction(self, generated_reaction):
            self.generated_reactions.append(generated_reaction)

class CondReactionClass (ReactionClass):
    def __init__(self, reactant1, reactant2, reaction_speed):
        super().__init__(reaction_speed)
        self.generic_reactant_1 = reactant1
        self.generic_reactant_2 = reactant2
    

class CllReactionClass (ReactionClass):
    def __init__(self, reactant, n_split, reaction_speed):
        super().__init__(reaction_speed)
        self.generic_reactant = reactant
        self.n_split = n_split



class GeneratedReaction:
    def __init__(self, reactants, reaction_class, product):
        self.reactants = reactants
        self.reaction_class = reaction_class #ReactionClass
        self.product = product
    
    def get_catalyzers(self):
        return self.reaction_class.catalyzers

    def is_species_in_reaction(self, species):
        return (species in self.reactants)
        



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