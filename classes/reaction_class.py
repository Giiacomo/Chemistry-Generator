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