import sys
import random
import argparse
from classes import SystemParameters, Species, Catalyzer, GeneratedReaction
from chemistryIO.generator_io import GeneratorIO
from utils.utils import are_reactions_same_no_cata, flatten_species_list, are_reactions_same
import traceback
from utils.decorators import timing_decorator, species_involved_decorator

class ReactionGenerator:
    def __init__(self, system, species, reaction_classes, catalyzer_params, len_classes):
        self.species = species
        self.reaction_classes = reaction_classes
        self.catalyzer_params = catalyzer_params
        self.container = species[0]
        self.catalyzers = []
        self.cond_reactions = []
        self.cll_reactions = []
        self.system = system
        self.len_classes = len_classes
        self.both_on = catalyzer_params[3] == 'ON'

    def assign_catalyzers(self, eligible_species, reactions, limit=-1):
        species_pool = eligible_species[:]
        new_catalyzer_list = []
        used_species = set([c.species for c in self.catalyzers])  

        
        for reaction in reactions:
            if len(new_catalyzer_list) == limit:
                return new_catalyzer_list

            if not species_pool:
                species_pool = [s for s in eligible_species if s not in used_species]  
                if not species_pool:  
                    species_pool = eligible_species[:]  

            chosen = random.choice(species_pool)
            catalyzer = next((c for c in self.catalyzers if c.species == chosen), None)

            if catalyzer is None:
                catalyzer = Catalyzer(chosen)
                new_catalyzer_list.append(catalyzer)
                used_species.add(chosen)
                self.catalyzers.append(catalyzer)
            if reaction not in catalyzer.reactions:        
                catalyzer.add_reaction_class(reaction)
                reaction.add_catalyzer(catalyzer)

            species_pool.remove(chosen)



    @timing_decorator
    def generate_catalyzers(self):
        catalyzer_params = self.catalyzer_params
        species = self.species
        cond_reactions = self.reaction_classes["conds"]
        cll_reactions = self.reaction_classes["clls"]

        min_length, max_length = catalyzer_params[0]
        num_cond_catalyzers = catalyzer_params[1]
        num_cll_catalyzers = catalyzer_params[2]

        eligible_species = [species.name for species in species[1:] if min_length <= len(species.name) <= max_length]
        
        eligible_cond_species = random.choices(eligible_species, k=num_cond_catalyzers)
        if len(eligible_cond_species) < num_cond_catalyzers :
            raise ValueError("Error! Not enough eligible species to satisfy the cond catalyzer requirements.")

        
        self.assign_catalyzers(eligible_cond_species, cond_reactions)

        if self.both_on:
            eligible_cll_species = random.choices(eligible_species, k=num_cll_catalyzers)
        else:
            eligible_species = [species for species in eligible_species if species not in [catalyzer.species for catalyzer in self.catalyzers]]
            eligible_cll_species = random.choices(eligible_cll_species, k=num_cll_catalyzers)
            if len(eligible_cll_species) < num_cll_catalyzers :
                raise ValueError("Error! Not enough eligible species to satisfy the cll catalyzer requirements.")
        self.assign_catalyzers(eligible_cll_species, cll_reactions)

    @species_involved_decorator
    @timing_decorator
    def generate_condensation_reactions(self, species):
        reactions = self.reaction_classes["conds"]
        condensation_reactions = []
        species = [species.name for species in species if species.name != self.container.name]


        for i in range(len(species)):
            for j in range(len(species)):
                reactant_1 = species[i]
                reactant_2 = species[j]
                for reaction in reactions:
                    if reactant_1.endswith(reaction.generic_reactant_1) and reactant_2.startswith(reaction.generic_reactant_2):
                        product_species = reactant_1 + reactant_2
                        
                        product = Species(product_species, self.system.D_CONCENTRATION, self.system.D_CONTRIB)

                        for species_prod in self.species:
                            if species_prod.name == product.name:
                                product = species_prod
                                break
                        
                        new_reaction = GeneratedReaction(reactants=[reactant_1, reactant_2], reaction_class=reaction, product=[product])
                        for r in self.cond_reactions:
                            if are_reactions_same_no_cata(r, new_reaction):
                                new_reaction = r
                                break

                        if new_reaction not in condensation_reactions:
                            condensation_reactions.append(new_reaction)
                            product.add_generator_reaction(new_reaction)
                            reaction.add_generated_reaction(new_reaction)

        return condensation_reactions

    @species_involved_decorator
    @timing_decorator
    def generate_cleavage_reactions(self, species):
        reactions = self.reaction_classes["clls"]
        cleavage_reactions = []
        species = [species.name for species in species if species.name != self.container.name]

        for specie_name in species:
            for reaction in reactions:
                reactant_core = reaction.generic_reactant
                n_split = int(reaction.n_split)
                reactant_core_len = len(reactant_core)

                start_index = specie_name.find(reactant_core)
                while start_index != -1:
                    if reactant_core_len >= n_split:
                        cleavage_1 = specie_name[:start_index + n_split]
                        cleavage_2 = specie_name[start_index + n_split:]

                        
                        if (cleavage_1.endswith(reactant_core[:n_split]) and
                            cleavage_2.startswith(reactant_core[n_split:])):
                            
                            product_species1 = None
                            product_species2 = None
                            found = False

                            for species_prod in self.species:
                                if species_prod.name == cleavage_1:
                                    product_species1 = species_prod
                                    found = True
                                    break
                           
                            if not found:
                                product_species1 = Species(cleavage_1, self.system.D_CONCENTRATION, self.system.D_CONTRIB)

                            found = False

                            for species_prod in self.species:
                                if species_prod.name == cleavage_2:
                                    product_species2 = species_prod
                                    found = True
                                    break

                            if not found:
                                product_species2 = Species(cleavage_2, self.system.D_CONCENTRATION, self.system.D_CONTRIB)


                            new_reaction = GeneratedReaction(
                                reactants=[specie_name],
                                reaction_class=reaction,
                                product=[product_species1, product_species2]
                            )

                            found = False
                            for r in self.cll_reactions:
                                if found:
                                    break
                                if are_reactions_same_no_cata(r, new_reaction):                                   
                                    new_reaction = r
                                    found = True


                            cleavage_reactions.append(new_reaction)
                            product_species1.add_generator_reaction(new_reaction)
                            product_species2.add_generator_reaction(new_reaction)
                            reaction.add_generated_reaction(new_reaction)
                    start_index = specie_name.find(reactant_core, start_index + 1)

        return cleavage_reactions

    @species_involved_decorator
    @timing_decorator
    def generate_new_catalyzers(self, new_species):
        new_species = [species.name for species in new_species]
        cond_reactions = self.reaction_classes["conds"]
        cll_reactions = self.reaction_classes["clls"]

        for i in range(len(new_species)):
            extracted_specie = random.choice(new_species)
            len_extracted_specie = str(len(extracted_specie))
            if len_extracted_specie in self.len_classes:    
                extracted_specie_class = self.len_classes[len_extracted_specie]
                is_cond_catalyzer = random.random() <= extracted_specie_class.p_cond
                is_cll_catalyzer = random.random() <= extracted_specie_class.p_cll

                if not self.both_on and is_cond_catalyzer and is_cll_catalyzer:
                    if random.random() <= 0.5:
                        is_cond_catalyzer = False
                    else:
                        is_cll_catalyzer = False
                #filter based on specificity
                specificity = extracted_specie_class.specificity
                filtered_cond_reactions = [
                    reaction for reaction in cond_reactions
                    if len(reaction.generic_reactant_1) + len(reaction.generic_reactant_2) >= specificity
                ]
                filtered_cll_reactions = [
                    reaction for reaction in cll_reactions
                    if len(reaction.generic_reactant) >= specificity
                ]

                if is_cond_catalyzer:
                    self.assign_catalyzers([extracted_specie], filtered_cond_reactions, limit=1)
                if is_cll_catalyzer:
                    self.assign_catalyzers([extracted_specie], filtered_cll_reactions, limit=1)


    @timing_decorator
    def generate_new_species(self):
        new_cond_species = {reaction.product[0] for reaction in self.cond_reactions if reaction.product[0].name not in [species.name for species in self.species[:]]}
        new_cll_species = {product for reaction in self.cll_reactions for product in reaction.product if product.name not in [species.name for species in self.species[:]]}
        new_species = list(new_cond_species | new_cll_species)
        self.generate_new_catalyzers(new_species)
        self.species.extend(new_species)
        self.species = flatten_species_list(self.species)
        while True:

            current_species = flatten_species_list([species for species in self.species if species.name != self.container.name])
            new_species_short = [species for species in current_species if len(species.name) <= int(self.system.ML)]
            
            new_condensation_products = self.generate_condensation_reactions(new_species_short)
            new_cleavage_products = [] 

            if self.system.CLL_ML_ACTIVE == 'ON':
                new_cleavage_products = self.generate_cleavage_reactions(new_species_short)
            else:
                new_cleavage_products = self.generate_cleavage_reactions(current_species)

            new_species_set = set([reaction.product[0] for reaction in new_condensation_products])
            new_species_set.update([reaction.product[0] for reaction in new_cleavage_products])
            new_species_set.update([reaction.product[1] for reaction in new_cleavage_products])

            new_species_list = list(new_species_set)
            new_species_list = [specie for specie in new_species_list if specie.name not in [species.name for species in current_species]]

            self.generate_new_catalyzers(new_species_list)

            self.cond_reactions.extend(new_condensation_products)
            self.cll_reactions.extend(new_cleavage_products)
            if not new_species_list:
                break
            self.species.extend(new_species_list)

            self.species = flatten_species_list(self.species)

        self.cond_reactions = self.eliminate_duplicate_reactions(self.cond_reactions)
        self.cll_reactions = self.eliminate_duplicate_reactions(self.cll_reactions)

    def eliminate_duplicate_reactions(self, reactions):
        unique_reactions = []
        for reaction in reactions:
            if not any(are_reactions_same(r, reaction) for r in unique_reactions):
                unique_reactions.append(reaction)
        return unique_reactions

    def sort_species (self):
        self.species.sort(key=lambda x: (len(x.name), x.name))
        self.species = [self.container] + [species for species in self.species if species.name != self.container.name]

    @timing_decorator
    def run_generation(self):
        
        self.generate_catalyzers()
        self.cond_reactions = self.generate_condensation_reactions(self.species)
        self.cll_reactions = self.generate_cleavage_reactions(self.species)

        self.cond_reactions = self.eliminate_duplicate_reactions(self.cond_reactions)
        self.cll_reactions = self.eliminate_duplicate_reactions(self.cll_reactions)

        self.generate_new_species()
        self.sort_species()


        generated_data = {
            "catalyzers": self.catalyzers,
            "cond_reactions": self.cond_reactions,
            "cll_reactions": self.cll_reactions,
            "species": self.species,
            "reaction_classes": self.reaction_classes["conds"] + self.reaction_classes["clls"] 
        }

        return generated_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate species and reactions.")
    parser.add_argument("file_path", help="The path to the input file.")
    parser.add_argument("-o", "--output", help="The name of the output file.")
    parser.add_argument("-debug", action="store_true", help="Enable debug mode.", default=False)
    parser.add_argument("-ot", "--output-type", choices=["txt", "txt-verbose", "excel"], default="txt", help="Specify the output type. Choices are 'txt', 'txt-verbose', or 'excel'.")

    args = parser.parse_args()

    debug = args.debug
    output_type = args.output_type
    file_path = args.file_path
    output_file = args.output

    generatorIO = GeneratorIO(input_file=file_path, output_file=output_file, debug=debug, debug_output_type=output_type)
    try:
        parsed_data = generatorIO.parse_data()
        system = parsed_data.get("system", SystemParameters())
        species = parsed_data.get("species", [])
        len_classes = parsed_data.get("len_classes", [])
        len_dict = {str(length_class.len): length_class for length_class in len_classes}

        catalyzer_params = parsed_data.get("catalyzer_params", [])
        reaction_classes = parsed_data.get("reactions", {})


        generator = ReactionGenerator(system=system,
                                      species=species,
                                      reaction_classes=reaction_classes,
                                      catalyzer_params=catalyzer_params,
                                      len_classes=len_dict)

        generated_data = generator.run_generation()
        
        generatorIO.write_data(generated_data)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = traceback.extract_tb(exc_traceback)

        print("An error occurred:", str(e))
        for tb in traceback_details:
            print(f"File: {tb.filename}, Line: {tb.lineno}, Function: {tb.name}")
        sys.exit(1)