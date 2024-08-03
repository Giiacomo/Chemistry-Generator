

from classes import SystemParameters, Species, LengthClass, CondReactionClass, CllReactionClass
from .base_io import BaseIO

class GenToolIO(BaseIO):

    def _process_line(self, line, data, current_section, catalyzer_params_counter):
        if line.startswith('SYSTEM'):
            current_section = 'system'
            data[current_section] = {}
        elif line.startswith('SPECIES'):
            current_section = 'species'
            data[current_section] = []
        elif line.startswith('LEN_CLASSES'):
            current_section = 'len_classes'
            data[current_section] = {}
        elif line.startswith('CATALYZER_PARAMS'):
            current_section = 'catalyzer_params'
            data[current_section] = []
        elif line.startswith('CONDS'):
            current_section = 'conds'
            data[current_section] = []
        elif line.startswith('CLLS'):
            current_section = 'clls'
            data[current_section] = []
        else:
            data, catalyzer_params_counter = self._read_data(line, data, current_section, catalyzer_params_counter)
        return data, current_section, catalyzer_params_counter

    def _read_data(self, line, data, current_section, catalyzer_params_counter):
        if current_section == 'system':
            self._parse_system_param(line, data['system'])
        elif current_section == 'species':
            data[current_section].append(self._parse_species(line))
        elif current_section == 'len_classes':
            new_params = self._parse_len_classes(line)
            data[current_section].update(new_params)
        elif current_section == 'catalyzer_params':
            data[current_section].append(self._parse_catalyzer_param(line, catalyzer_params_counter))
            catalyzer_params_counter += 1
        elif current_section in ['conds', 'clls']:
            self._parse_conditions_or_cleavage(line, data, current_section)
        return data, catalyzer_params_counter

    def _parse_conditions_or_cleavage(self, line, data, current_section):
        parts = line.split()
        if current_section == 'conds' and len(parts) == 3:
            data[current_section] = parts
        elif current_section == 'clls' and len(parts) == 2:
            nt_s = parts[0].split(',')
            data[current_section] = [nt_s, parts[1]]
        else:
            raise ValueError(f"Error!\n{current_section} correct form:\n"
                             f"CONDS: <reactant_1> <reactant_2> <reaction_speed>\n"
                             f"CLLS: <reactant> <reaction_speed>")

    def write_data(self, data):
        with open(self.output_file, 'w') as file:

            file.write("SYSTEM\n")
            for key, value in data['system'].items():
                file.write(f"{key}\t{value}\n")
            file.write("\n")

            file.write("SPECIES\n")
            for specie in data["species"]:
                file.write(" ".join(specie) + "\n")

            file.write("\nCATALYZER_PARAMS\n")
            first_cata_line = ",".join(map(str, data['catalyzer_params'][0]))
            file.write(first_cata_line + "\n")  
            for param in data['catalyzer_params'][1:]:
                file.write(str(param) + "\n")       


            file.write("\nREACTIONS\n")

            for r in data["gen-conds"]["reactions"]:
                file.write(f'R-{r[0]}\t{r[1]}-R\t{data["gen-conds"]["v"]}\n')
            file.write("\n")

            for r in data["gen-clls"]["reactions"]:
                file.write(f'R-{r}-R\t{data["gen-clls"]["v"]}\t 1\n')
            print(f"\nThe chemical {self.output_file} has been generated and is ready to be used as input to the actual chemical generator!\n")