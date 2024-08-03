from openpyxl import Workbook

from classes import CondReactionClass, CllReactionClass
from .base_io import BaseIO
from utils.constants import *
from .config_handler import config_handler
from utils.logger import Logger

class GeneratorIO(BaseIO):

    def __init__(self, input_file, output_file=None, debug=False, debug_output_type=None):
        super().__init__(input_file, output_file)
        Logger.set_debug_mode(debug)
        self.debug = debug
        self.debug_output_type = debug_output_type
        self.debug_file = f"{config_handler.output_dir}/{output_file if output_file is not None else DEFAULT_OUTPUT_FILE}.debug."

        self.debug_file = self.output_file.replace(".txt", "") + ".debug."
        if debug_output_type == 'txt-verbose':
            self.debug_file += "verbose.txt"
        elif debug_output_type == 'excel':
            self.debug_file += "xls"
        else:
            self.debug_file += "txt"



    def write_data(self, data):
        with open(self.output_file, 'w') as file:
            max_name_length = max(len(str(species.name)) for species in data["species"])
            max_concentration_length = max(len(str(species.concentration)) for species in data["species"])

            for species in data["species"]:
                name_str = str(species.name).ljust(max_name_length + 2) 
                concentration_str = str(species.concentration).ljust(max_concentration_length + 2) 
                contrib_str = str(species.contrib) 

                file.write(f"{name_str} {concentration_str} {contrib_str}\n")

            file.write("\n") 

            self.counter_cond = 0
            for r in data["cond_reactions"]:  
                for catalyzer in r.reaction_class.catalyzers:
                    file.write(r.reactants[0] + " + " + r.reactants[1] + " + " + catalyzer.species + " > " + r.product[0].name + " + " + catalyzer.species + " ; " + str(r.reaction_class.reaction_speed) + "\n")
                    self.counter_cond += 1

            file.write("\n")

            self.counter_cll = 0
            for r in data["cll_reactions"]:
                for catalyzer in r.reaction_class.catalyzers:
                    file.write(r.reactants[0] + " + " + catalyzer.species + " > " + r.product[0].name + " + " + r.product[1].name + " + " + catalyzer.species + " ; " + str(r.reaction_class.reaction_speed) + "\n")
                    self.counter_cll += 1

            if self.debug:
                self.print_info(data)
                if self.debug_output_type == 'txt-verbose':
                    self.write_debug_info_verbose(data)
                elif self.debug_output_type == 'excel':
                    self.write_debug_info_excel(data)
                else:
                    self.write_debug_info(data)
            
            Logger.info(f'Seed {data["seed"]} has been used for the generation.')

    def write_debug_info_excel(self, data):
        wb = Workbook()
        ws = wb.active
        ws.title = "Debug Info"

        
        ws.append(["CATALYZERS INFO"])
        ws.append(["Name", "Length (chars)", "Reaction Class (total)", "Cond Reactions", "Cll Reactions",
                "Total Generated Reactions", "Generated Cond Reactions", "Generated Cll Reactions",
                "Catalyzers as reagent"])

        for catalyzer in data["catalyzers"]:
            name = catalyzer.species
            name_length = len(name)
            n_catalyzed_reactions = len(catalyzer.reactions)
            catalyzed_cond_reactions = [r for r in catalyzer.reactions if isinstance(r, CondReactionClass)]
            catalyzed_cll_reactions = [r for r in catalyzer.reactions if isinstance(r, CllReactionClass)]
            n_catalyzed_reactions_gen = catalyzer.get_n_catalyzed_reactions()

            counter_cata_reactant = 0
            for r in data["reaction_classes"]:
                for gen_r in r.generated_reactions:
                    if gen_r.is_species_in_reaction(name):
                        counter_cata_reactant += 1

            ws.append([name, name_length, n_catalyzed_reactions, len(catalyzed_cond_reactions), len(catalyzed_cll_reactions),
                    n_catalyzed_reactions_gen['n_cata_gen_reactions'], n_catalyzed_reactions_gen['n_cata_gen_cond'],
                    n_catalyzed_reactions_gen['n_cata_gen_cll'], counter_cata_reactant])

        ws.append([])  

        
        ws.append(["SPECIES INFO"])
        ws.append(["Name", "Length (chars)", "Total Generated Reactions", "Cond Reactions", "Cll Reactions",
                "Total Catalyzers", "Cond Catalyzers", "Cll Catalyzers", "Reactions as Reactants", "Unique Catalyzers"])

        for species in data["species"]:
            name = species.name
            name_length = len(name)
            species_generator_info = species.get_generator_reaction_info()
            reactions_as_reactant = len([gen_r for r in data["reaction_classes"] for gen_r in r.generated_reactions if gen_r.is_species_consumed(species)])
            
            unique_catalyzers = [catalyzer.species for catalyzer in species_generator_info['list_unique_catalyzers']]
            unique_catalyzers_str = ', '.join(unique_catalyzers) if unique_catalyzers else 'None'

            ws.append([name, name_length, species_generator_info['n_generator_reaction'],
                    species_generator_info['n_generator_cond_reaction'], species_generator_info['n_generator_cll_reaction'],
                    species_generator_info['n_catalyzers'], species_generator_info['n_cond_catalyzers'],
                    species_generator_info['n_cll_catalyzers'], reactions_as_reactant, unique_catalyzers_str])

        ws.append([])  

        
        ws.append(["CATALYZERS AS SPECIES INFO"])
        ws.append(["Name", "Length (chars)", "Total Generated Reactions", "Cond Reactions", "Cll Reactions",
                "Total Catalyzers", "Cond Catalyzers", "Cll Catalyzers", "Reactions as Reactants", "Unique Catalyzers"])

        for catalyzer in data["catalyzers"]:
            name = catalyzer.species
            name_length = len(name)
            species = next(s for s in data["species"] if s.name == name)
            species_generator_info = species.get_generator_reaction_info()
            reactions_as_reactant = len([gen_r for r in data["reaction_classes"] for gen_r in r.generated_reactions if gen_r.is_species_consumed(species)])
            
            unique_catalyzers = [catalyzer.species for catalyzer in species_generator_info['list_unique_catalyzers']]
            unique_catalyzers_str = ', '.join(unique_catalyzers) if unique_catalyzers else 'None'

            ws.append([name, name_length, species_generator_info['n_generator_reaction'],
                    species_generator_info['n_generator_cond_reaction'], species_generator_info['n_generator_cll_reaction'],
                    species_generator_info['n_catalyzers'], species_generator_info['n_cond_catalyzers'],
                    species_generator_info['n_cll_catalyzers'], reactions_as_reactant, unique_catalyzers_str])

        wb.save(self.debug_file)

    def write_debug_info_verbose(self, data):
        with open(self.debug_file, 'w') as file:
            file.write("CATALYZERS INFO\n\n")
            for catalyzer in data["catalyzers"]:
                name = catalyzer.species
                name_length = len(name)
                file.write(f"{name} (Length: {name_length} chars):\n")
                n_catalyzed_reactions = len(catalyzer.reactions)
                file.write(f"\t- Number of total catalyzed reactions: {n_catalyzed_reactions}\n")
                catalyzed_cond_reactions = [r for r in catalyzer.reactions if isinstance(r, CondReactionClass)]
                catalyzed_cll_reactions = [r for r in catalyzer.reactions if isinstance(r, CllReactionClass)]
                file.write(f"\t- Number of catalyzed condensation reaction classes: {len(catalyzed_cond_reactions)}\n")
                file.write(f"\t- Number of catalyzed cleavage reaction classes: {len(catalyzed_cll_reactions)}\n")
                file.write(f"\t- Catalyzed condensation reaction classes:\n")
                if len(catalyzed_cond_reactions) > 0:
                    for i, r in enumerate(catalyzed_cond_reactions):
                        file.write(f"\t\t{i+1}. R-{r.generic_reactant_1} + {r.generic_reactant_2}-R\n")
                else:
                    file.write(f"\t\tNone\n")
                file.write(f"\t- Catalyzed cleavage reactions classes\n")
                if len(catalyzed_cll_reactions) > 0:
                    for i, r in enumerate(catalyzed_cll_reactions):
                        file.write(f"\t\t{i+1}. R-{r.generic_reactant}-R\n")
                else:
                    file.write(f"\t\tNone\n")

                n_catalyzed_reactions = catalyzer.get_n_catalyzed_reactions()
                file.write(f"\t- Number of total catalyzed generated reactions: {n_catalyzed_reactions['n_cata_gen_reactions']}\n")
                file.write(f"\t- Number of total catalyzed generated condensation reactions: {n_catalyzed_reactions['n_cata_gen_cond']}\n")
                file.write(f"\t- Number of total catalyzed generated cleavage reactions: {n_catalyzed_reactions['n_cata_gen_cll']}\n")
                
                counter_cata_reactant = 0
                for r in data["reaction_classes"]:
                    for gen_r in r.generated_reactions:
                        if gen_r.is_species_in_reaction(name):
                            counter_cata_reactant += 1

                file.write(f"\t- The catalyzers species appears in {counter_cata_reactant} reactions.\n")
                file.write("\n")

            file.write("\n\n\nSPECIES INFO:\n\n")
            
            for species in data["species"]:
                name = species.name
                name_length = len(name)
                file.write(f"{name} (Length: {name_length} chars):\n")
                species_generator_info = species.get_generator_reaction_info()
                reactions_as_reactant = len([gen_r for r in data["reaction_classes"] for gen_r in r.generated_reactions if gen_r.is_species_consumed(species)])
                
                file.write(f"\t- Number of reactions that generate the species: {species_generator_info['n_generator_reaction']}\n")
                file.write(f"\t- Number of cond reactions that generate the species: {species_generator_info['n_generator_cond_reaction']}\n")
                file.write(f"\t- Number of cll reactions that generate the species: {species_generator_info['n_generator_cll_reaction']}\n")
                file.write(f"\t- Number of catalyzers that generate the species: {species_generator_info['n_catalyzers']}\n")
                file.write(f"\t- Number of condensation catalyzers that generate the species: {species_generator_info['n_cond_catalyzers']}\n")
                file.write(f"\t- Number of cleavage catalyzers that generate the species: {species_generator_info['n_cll_catalyzers']}\n")
                file.write(f"\t- Number of reactions where the species is a reactant: {reactions_as_reactant}\n")
                
                file.write(f"\t- List of catalyzers that generate the species:\n")
                for i, catalyzer in enumerate(species_generator_info['list_unique_catalyzers']):
                    file.write(f"\t\t{i+1}. {catalyzer.species}\n")
                
                file.write("\n")

            file.write("\n\n\nCATALYZERS AS SPECIES INFO:\n\n")
            
            for catalyzer in data["catalyzers"]:
                name = catalyzer.species
                name_length = len(name)
                species = next(s for s in data["species"] if s.name == name)
                species_generator_info = species.get_generator_reaction_info()
                reactions_as_reactant = len([gen_r for r in data["reaction_classes"] for gen_r in r.generated_reactions if gen_r.is_species_consumed(species)])
                
                file.write(f"{name} (Length: {name_length} chars):\n")
                file.write(f"\t- Number of reactions that generate the species: {species_generator_info['n_generator_reaction']}\n")
                file.write(f"\t- Number of cond reactions that generate the species: {species_generator_info['n_generator_cond_reaction']}\n")
                file.write(f"\t- Number of cll reactions that generate the species: {species_generator_info['n_generator_cll_reaction']}\n")
                file.write(f"\t- Number of catalyzers that generate the species: {species_generator_info['n_catalyzers']}\n")
                file.write(f"\t- Number of condensation catalyzers that generate the species: {species_generator_info['n_cond_catalyzers']}\n")
                file.write(f"\t- Number of cleavage catalyzers that generate the species: {species_generator_info['n_cll_catalyzers']}\n")
                file.write(f"\t- Number of reactions where the species is a reactant: {reactions_as_reactant}\n")
                
                file.write(f"\t- List of catalyzers that generate the species:\n")
                for i, catalyzer in enumerate(species_generator_info['list_unique_catalyzers']):
                    file.write(f"\t\t{i+1}. {catalyzer.species}\n")
                
                file.write("\n")

    def write_debug_info(self, data):
        with open(self.debug_file, 'w') as file:
            file.write("CATALYZERS\n")
            file.write(f"{'Name':<20} {'Length (chars)':<15} {'Reaction Class (total)':<25} {'Cond Reactions':<15} {'Cll Reactions':<15} "
                    f"{'Generated in reactions':<22} {'Gen Cond Reactions':<20} {'Gen Cll Reactions':<20} "
                    f"{'Catalyzers as reagent':<25}\n")
            
            for catalyzer in data["catalyzers"]:
                name = catalyzer.species
                name_length = len(name)
                n_catalyzed_reactions = len(catalyzer.reactions)
                catalyzed_cond_reactions = [r for r in catalyzer.reactions if isinstance(r, CondReactionClass)]
                catalyzed_cll_reactions = [r for r in catalyzer.reactions if isinstance(r, CllReactionClass)]
                n_catalyzed_reactions_gen = catalyzer.get_n_catalyzed_reactions()
                
                counter_cata_reactant = 0
                for r in data["reaction_classes"]:
                    for gen_r in r.generated_reactions:
                        if gen_r.is_species_in_reaction(name):
                            counter_cata_reactant += 1
                
                file.write(f"{name:<20} {name_length:<15} {n_catalyzed_reactions:<25} {len(catalyzed_cond_reactions):<15} "
                        f"{len(catalyzed_cll_reactions):<15} {n_catalyzed_reactions_gen['n_cata_gen_reactions']:<22} "
                        f"{n_catalyzed_reactions_gen['n_cata_gen_cond']:<20} "
                        f"{n_catalyzed_reactions_gen['n_cata_gen_cll']:<20} "
                        f"{counter_cata_reactant:<25}\n")
            

            file.write("\n\nSPECIES\n")
            file.write(f"{'Name':<20} {'Length (chars)':<15} {'Generated in reactions':<22} {'Cond Reactions':<15} {'Cll Reactions':<15} "
                    f"{'Total Catalyzers':<17} {'Cond Catalyzers':<15} {'Cll Catalyzers':<15} "
                    f"{'Reactions as Reactants':<25} {'Unique Catalyzers':<25}\n")
            

            for species in data["species"]:
                name = species.name
                name_length = len(name)
                
                species_generator_info = species.get_generator_reaction_info()
                
                reactions_as_reactant = len([gen_r for r in data["reaction_classes"] for gen_r in r.generated_reactions if gen_r.is_species_consumed(species)])
                
                unique_catalyzers = [catalyzer.species for catalyzer in species_generator_info['list_unique_catalyzers']]
                unique_catalyzers_str = ', '.join(unique_catalyzers) if unique_catalyzers else 'None'
                

                file.write(f"{name:<20} {name_length:<15} {species_generator_info['n_generator_reaction']:<22} "
                        f"{species_generator_info['n_generator_cond_reaction']:<15} "
                        f"{species_generator_info['n_generator_cll_reaction']:<15} "
                        f"{species_generator_info['n_catalyzers']:<17} "
                        f"{species_generator_info['n_cond_catalyzers']:<15} "
                        f"{species_generator_info['n_cll_catalyzers']:<15} "
                        f"{reactions_as_reactant:<25} {unique_catalyzers_str:<25}\n")
                

            

            file.write("\n\nCATALYZERS AS SPECIES\n")
            file.write(f"{'Name':<20} {'Length (chars)':<15} {'Generated in reactions':<22} {'Cond Reactions':<15} {'Cll Reactions':<15} "
                    f"{'Total Catalyzers':<17} {'Cond Catalyzers':<15} {'Cll Catalyzers':<15} "
                    f"{'Reactions as Reactants':<25} {'Unique Catalyzers':<25}\n")
            

            for catalyzer in data["catalyzers"]:
                name = catalyzer.species
                name_length = len(name)
                species = next(s for s in data["species"] if s.name == name)
                species_generator_info = species.get_generator_reaction_info()
                reactions_as_reactant = len([gen_r for r in data["reaction_classes"] for gen_r in r.generated_reactions if gen_r.is_species_consumed(species)])
                
                unique_catalyzers = [catalyzer.species for catalyzer in species_generator_info['list_unique_catalyzers']]
                unique_catalyzers_str = ', '.join(unique_catalyzers) if unique_catalyzers else 'None'
                
                file.write(f"{name:<20} {name_length:<15} {species_generator_info['n_generator_reaction']:<22} "
                        f"{species_generator_info['n_generator_cond_reaction']:<15} "
                        f"{species_generator_info['n_generator_cll_reaction']:<15} "
                        f"{species_generator_info['n_catalyzers']:<17} "
                        f"{species_generator_info['n_cond_catalyzers']:<15} "
                        f"{species_generator_info['n_cll_catalyzers']:<15} "
                        f"{reactions_as_reactant:<25} {unique_catalyzers_str:<25}\n")
                
    def print_info(self, data):
        
        if config_handler.print_species_info:
                print()
                new_generated_species = [species for species in data["species"] if species.is_in_initial_set == False] 
                Logger.debug(f"{len(new_generated_species)} new species have beeng generated:")        
                Logger.debug(", ".join([species.name for species in new_generated_species]))
                print()

        if config_handler.print_reaction_info:
            counter_cond = sum(len(reaction.get_catalyzers()) for reaction in data['cond_reactions'])
            counter_cll = sum(len(reaction.get_catalyzers()) for reaction in data['cll_reactions'])

            Logger.debug(f"{counter_cond} condensation reactions have been generated")
            Logger.debug(f"{counter_cll} condensation reactions have been generated")
            print()



        if config_handler.print_catalyzer_info:
            Logger.debug("Condensation catalyzers for this chemical are: " )
            Logger.debug(", ".join(catalyzer.species for catalyzer in data["catalyzers"] if catalyzer.is_cond_catalyzer()))

            Logger.debug("Cleavage catalyzers for this chemical are: " )
            Logger.debug(", ".join(catalyzer.species for catalyzer in data["catalyzers"] if catalyzer.is_cll_catalyzer()))

            Logger.debug("Assigned reactions for each catalyzer:")
            for catalyzer in data["catalyzers"]:
                Logger.debug(f"{catalyzer.species}:")
                cond_classes = [f'[R-{reaction.generic_reactant_1} + {reaction.generic_reactant_2}-R]' for reaction in catalyzer.get_cond_reaction_classes()]
                if cond_classes:
                    Logger.debug(f" Cond: {', '.join(cond_classes)}")
                cll_classes = [f'[R-{reaction.generic_reactant}-R]' for reaction in catalyzer.get_cll_reaction_classes()]
                if cll_classes:
                    Logger.debug(f" Cll: {', '.join(cll_classes)}")
            print()