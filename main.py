import sys
import time
import subprocess
import argparse

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

    if args.generator:
        print("\nRunning generation process!")
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
        start_time = time.time()
        subprocess.run(command, check=True)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"The process took {elapsed_time} seconds!\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
