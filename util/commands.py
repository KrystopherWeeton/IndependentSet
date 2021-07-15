import os
import sys
from typing import Callable

import click

from util.storage import load

"""
    Verifies the provided pickle name, getting input from user if it is invalid
    and performing an os check to ensure it is a valid file.
        today - Used to mark that the pickle file is the default for today
"""
def verify_pickle_name(today: str, gen_default_file_name: Callable) -> str:
    #? Sets pickle_name to appropriate value using today flag
    if not today:
        pickle_name = click.prompt("Results File Name", type=str)
    else:
        pickle_name = f"results/{gen_default_file_name()}"
    #? Verifies valid file on the os and returns 
    if not os.path.isfile(f"{pickle_name}.pkl"):
        click.secho(f"The file provided could not be found.", err=True)
        sys.exit(0)
    return pickle_name


"""
    Verifies and loads a pickle file name into a class returned. Execution is halted
    on error.
"""
def verify_and_load_results(
    today: str,
    gen_default_file_name: Callable,
    results_class: type,
):
    #? Verifies path and loads results
    pickle_path = verify_pickle_name(today, gen_default_file_name)
    results: results_class = load(pickle_path)
    #? Verifies results loaded correctly and returns
    if results is None:
        click.secho("Could not load results.", err=True)
        sys.exit(0)
    return results


"""
    Prompts for a file name from the user.
        file_name - The file name to use. Prompt appears if this is None.
"""
def prompt_file_name(file_name: str) -> str:
    if file_name is None:
        file_name = click.prompt("Resulting Graph File", type=str)
        if file_name is None:
            click.secho("Invalid file name provided. Exiting.", err=True)
            sys.exit(0)
    return file_name