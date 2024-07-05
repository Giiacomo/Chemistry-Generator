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
    def __init__(self, name, concentration, contrib):
        self.name = name
        self.concentration = concentration
        self.contrib = contrib

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
        self.reaction_class = reaction_class #ReactionClass, to access speed and everything
        self.product = product



class Catalyzer:
    def __init__(self, catalyzer_species):
        self.species = catalyzer_species
        self.reactions = []

    def add_reaction_class(self, reaction):
        self.reactions.append(reaction)

    def get_n_catalyzed_reactions (self):
        n_catalyzed_reactions = {   'n_cata_gen_reactions': 0,
                                    'n_cata_gen_cond': 0,
                                    'n_cata_gen_cll': 0    
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