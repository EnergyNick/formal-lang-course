import os
import sys

import colorama

from project.language.interpreter import interpreter
from project.language.exceptions import *


def print_error(message: str):
    print(f'{colorama.Fore.RED}{message}')


if __name__ == "__main__":
    args = sys.argv
    size = len(args)

    if size >= 2 and args[1] == '-':
        program = " ".join(args[2:])
    elif size == 2 and os.path.isfile(args[1]):
        with open(args[1]) as file:
            program = '\n'.join(line.rstrip() for line in file)
    else:
        print_error("Incorrect args for interpreter")
        sys.exit(1)

    try:
        interpreter(program)
    except InterpreterException as e:
        print_error(f"Runtime error: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Internal interpreter error: {e}")
        sys.exit(1)
