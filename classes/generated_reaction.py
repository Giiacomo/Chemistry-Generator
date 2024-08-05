class GeneratedReaction:
    def __init__(self, reactants, reaction_class, product):
        self.reactants = reactants #[]
        self.reaction_class = reaction_class #ReactionClass
        self.product = product #[]

    def is_species_consumed(self, species):
        if species.name not in self.reactants:
            return False   
        len_reactants = len([reactant for reactant in self.reactants if reactant == species.name])
        len_prod = len([product for product in self.product if product == species.name])
        if len_reactants > len_prod:
            return True
        return False   
     

    def get_catalyzers(self):
        return self.reaction_class.catalyzers

    def is_species_in_reaction(self, species):
        return (species in self.reactants)
    