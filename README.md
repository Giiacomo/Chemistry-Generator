# Chemical Reaction Generator 🧪

## Overview ℹ️
This tool allows for the generation of chemical species and reactions based on user input. The tool has two main modes: `generator` and `gentool`, which can be selected using the appropriate flags.

## Usage 🚀

### Command Line Arguments 📋

- `file_path`: The path to the input file containing the chemical data (how the file should look to work properly is shown in the test folder or in the documentation relative to the mode you're using in the docs folder).
- `-o OUTPUT, --output OUTPUT`: The name of the output file where the generated data will be saved.
- `-debug`: Enable debug mode to write additional information to the debug file (only for **generator mode**).

### Flags 🚩

- `-generator`: Use the generator mode for generating species and reactions.
- `-gentool`: Use the gentool mode as a quick way to generate an input file for the actual generator (check the relative docs).

### Example 🌟

To run the tool in generator mode:
```bash
python main.py input.txt -generator -o output.txt -debug
```

### Command Usage Syntax
```bash
python3 main.py [-h] (-generator | -gentool) [-o OUTPUT] [-debug] [-ot {txt,txt-verbose,excel}] file_path
```
Run Generator or AutoTool based on the provided flag.

**Positional arguments:**
- `file_path`: The path to the input file.

**Options:**
- `-h, --help`: Show this help message and exit.
- `-generator`: Run the generator script.
- `-gentool`: Run the gentool script.
- `-o OUTPUT, --output OUTPUT`: The name of the output file.
- `-debug`: Enable debug mode.
- `-ot {txt,txt-verbose,excel}, --output-type {txt,txt-verbose,excel}`: Specify the output type. Choices are 'txt', 'txt-verbose', or 'excel'.

### Configuration ⚙️

The tool uses a configuration file to set default and debug-specific settings. Below are the sections and options you can configure:

#### Default Settings

The configuration allows for detailed logging of various aspects of the tool's operation. This can be configured in a settings file with different sections for default settings and debug-specific settings.

#### Default Settings

```
[DEFAULT]
input_dir = test/input
output_dir = test/output
output_fmt = txt
```

- `input_dir`: Specifies the default directory for input files.
- `output_dir`: Specifies the default directory for output files.
- `output_fmt`: Specifies the default output format. Options are `txt`, `txt-verbose`, and `excel`.

#### Debug Settings
```
[DEBUG]
print_function_time = false
print_species_involved = false
print_species_info = false
print_catalyzer_info = false
print_reaction_info = false
```

- `print_function_time`: When set to `true`, prints the time taken by each function.
- `print_species_involved`: When set to `true`, prints information about the species involved in reactions.
- `print_species_info`: When set to `true`, prints detailed information about each species.
- `print_catalyzer_info`: When set to `true`, prints detailed information about the catalyzers used.
- `print_reaction_info`: When set to `true`, prints detailed information about each reaction.

To enable these debug options, ensure the `-debug` flag is used when running the script.

