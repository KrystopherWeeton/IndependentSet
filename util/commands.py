import os
import sys
from typing import Callable

import click

import util.file_util as file_util
import util.plot as plot
from util.config import get_experiment_results_directory
from util.models.result import Result
from util.storage import load

"""
    Verifies the provided pickle name, getting input from user if it is invalid
    and performing an os check to ensure it is a valid file.
        today - Used to mark that the pickle file is the default for today
"""
def verify_pickle_name(today: str, gen_default_file_name: Callable, project_name: str) -> str:
    #? Sets pickle_name to appropriate value using today flag
    directory: str = get_experiment_results_directory(project_name)
    if not today:
        pickle_name = f"{directory}/{click.prompt('Results File Name', type=str)}"
    else:
        pickle_name = f"{directory}/{gen_default_file_name()}"
    #? Verifies valid file on the os and returns 
    if not os.path.isfile(f"{pickle_name}.pkl"):
        click.secho(f"The file provided could not be found.", err=True)
        sys.exit(0)
    return pickle_name


# TODO: Remove this function once everything has migrated to the new results subclass
"""
    Verifies and loads a pickle file name into a class returned. Execution is halted
    on error.
"""
def verify_and_load_results(
    today: str,
    gen_default_file_name: Callable,
    results_class: type,
    project_name: str,
):
    #? Verifies path and loads results
    pickle_path = verify_pickle_name(today, gen_default_file_name, project_name)
    results: results_class = load(pickle_path)
    #? Verifies results loaded correctly and returns
    if results is None:
        click.secho("Could not load results. Exiting.", err=True)
        sys.exit(0)
    if not isinstance(results, results_class):
        click.secho("Results were of invalid type. Exiting.", err=True)
        sys.exit(0)
    return results


def verify_and_load_results_v2(
    results_class: Result,
    project_name: str,
    today: str,
):
    pickle_path = verify_pickle_name(today, results_class.generate_file_name, project_name)
    results: results_class = load(pickle_path)
    if results is None:
        click.secho("Could not load results. Exiting.", err=True)
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

"""
    Wrapper which loads results and manages saving plots into that directory

    Assumed passed through `click` is 'today, dir_name, transient'. Passed to 
    actual function is `results, save` where `save` is a callable which takes
    in a file name and saves the active plot to that file name in the directory
    created. The wrapper also takes in `project_name, results_class` for validation
    and saving. 
"""
def dir_plot_command(f, project_name: str, results_class):
    def wrapped(today, dir_name, transient):
        if not transient:
            dir_name = file_util.create_dir_in_experiment_results_directory(dir_name, project_name)
        def save(file_name: str):
            plot.show_or_save(transient, f"{dir_name}/{file_name}", project_name)
        results = verify_and_load_results_v2(results_class, project_name, today)
        f(results, save)
    return wrapped


def single_plot_command(f, project_name: str, results_class):
    """ Wrapper which loads results / saves a single plot """
    def wrapped(today, file_name, transient):
        results = verify_and_load_results_v2(results_class, project_name, today)
        if not transient:
            file_name = prompt_file_name(file_name)
        f(results)
        if transient:
            plot.show_plot()
        else:
            plot.save_plot(file_name, project_name)
    return wrapped
