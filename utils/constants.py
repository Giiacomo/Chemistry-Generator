import os

SPECIES = 'SPECIES'
CATALYZER_PARAMS = 'CATALYZER_PARAMS'
REACTIONS = 'REACTIONS'
SYSTEM = 'SYSTEM'
LEN_CLASSES = 'LEN_CLASSES'

SPECIES_SECTION = 'species'
CATALYZER_PARAMS_SECTION = 'catalyzer_params'
REACTIONS_SECTION = 'reactions'
SYSTEM_SECTION = 'system'
LEN_CLASSES_SECTION = 'len_classes'

SPECIES_INPUT_FORM = ['<speciename>', '<concentration>', '<contribution>', '<can_cross_membrane>', '[external_concentration]', '[diffusion_constant]']
PARENT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = f'{PARENT_FOLDER}/config/config.ini'
DEFAULT_OUTPUT_FILE='output'

CONTAINER='Cont'
CLL_ML_ACTIVE='CLL_ML_ACTIVE'

INFO='INFO'
WARNING='WARNING'
ERROR='ERROR'