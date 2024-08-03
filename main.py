import sys
import time
import subprocess
import argparse
from utils.decorators import timing_decorator
from utils.logger import Logger
@timing_decorator
def main():
    parser = argparse.ArgumentParser(description="Run Generator or AutoTool based on the provided flag.")
    parser.add_argument("file_path", help="The path to the input file.")
    group = parser.add_mutually_exclusive_group(required=True)  # Just one, either gen or tool
    group.add_argument("-generator", action="store_true", help="Run the generator script.")
    group.add_argument("-gentool", action="store_true", help="Run the gentool script.")
    parser.add_argument("-o", "--output", help="The name of the output file.")
    parser.add_argument("-debug", action="store_true", help="Enable debug mode.", default=False)
    parser.add_argument("-ot", "--output-type", choices=["txt", "txt-verbose", "excel"], help="Specify the output type. Choices are 'txt', 'txt-verbose', or 'excel'.")

    args = parser.parse_args()

    if args.debug and not args.output_type:
        parser.error("When -debug is specified, -ot/--output-type must also be provided.")

    file_path = args.file_path
    output_file = args.output
    debug = args.debug
    output_type = args.output_type

    Logger.set_debug_mode(debug)
    Logger.get_logger()
    if args.generator:
        command = ["python3", "generator.py", file_path]

        if output_file:
            command += ["-o", output_file]
        if debug:
            command.append("-debug")
            if output_type:
                command += ["-ot", output_type]
            else:
                parser.error("-ot/--output-type is required when -debug is specified.")
        elif output_type:
            parser.error("-ot/--output-type cannot be used without -debug.")
    
    elif args.gentool:
        Logger.error("Currently under maintenance!")
        sys.exit(1)
        print("\nRunning tool process!")
        command = ["python3", "gen_tool.py", file_path]
        if output_file:
            command += ["-o", output_file]
        if debug:
            command.append("-debug")
            if output_type:
                command += ["-ot", output_type]
            else:
                parser.error("-ot/--output-type is required when -debug is specified.")
        elif output_type:
            parser.error("-ot/--output-type cannot be used without -debug.")
    
    try:
        Logger.info("Running generation process...")
        subprocess.run(command, check=True)
        Logger.info("Generation process completed!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
