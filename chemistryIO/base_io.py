import sys
from .parsers import parse_species, parse_catalyzer_param, parse_system_param, parse_reactions, parse_len_classes
from classes import SystemParameters
from .config_handler import config_handler
from utils.constants import *

class BaseIO:
    def __init__(self, input_file, output_file=None):


        self.input_file = f"{config_handler.input_dir}/{input_file}.{config_handler.output_fmt}"
        self.output_file = f"{config_handler.output_dir}/{output_file if output_file is not None else DEFAULT_OUTPUT_FILE}.{config_handler.output_fmt}"


    def parse_data(self):
        data = {}
        current_section = None
        catalyzer_params_counter = 0
        try:
            with open(self.input_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    data, current_section, catalyzer_params_counter = self._process_line(line, data, current_section, catalyzer_params_counter)

            data['system'].validate()

        except FileNotFoundError:
            print(self.input_file)
            print("Error: File not found.")
            sys.exit(1)
        except ValueError as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print("Error:", str(e))
            sys.exit(1)
        return data

    def _process_line(self, line, data, current_section, catalyzer_params_counter):
        if line.startswith(SPECIES):
            current_section = SPECIES_SECTION
            data[current_section] = []
        elif line.startswith(CATALYZER_PARAMS):
            current_section = CATALYZER_PARAMS_SECTION
            data[current_section] = []
        elif line.startswith(REACTIONS):
            current_section = REACTIONS_SECTION
            data[current_section] = {"conds": [], "clls": []}
        elif line.startswith(SYSTEM):
            current_section = SYSTEM_SECTION
            data[current_section] = SystemParameters()
        elif line.startswith(LEN_CLASSES):
            current_section = LEN_CLASSES_SECTION
            data[current_section] = []
        else:
            data, catalyzer_params_counter = self._read_data(line, data, current_section, catalyzer_params_counter)
        return data, current_section, catalyzer_params_counter

    def _read_data(self, line, data, current_section, catalyzer_params_counter):
        if current_section == SPECIES_SECTION:
            data[current_section].append(parse_species(line))
        elif current_section == CATALYZER_PARAMS_SECTION:
            data[current_section].append(parse_catalyzer_param(line, catalyzer_params_counter))
            catalyzer_params_counter += 1
        elif current_section == REACTIONS_SECTION:
            parse_reactions(line, data)
        elif current_section == SYSTEM_SECTION:
            parse_system_param(line, data['system'])
        elif current_section == LEN_CLASSES_SECTION:
            new_params = parse_len_classes(line)
            data[current_section].extend(new_params)
        return data, catalyzer_params_counter
