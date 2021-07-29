import os
import sys

import click

import util.plot.plot as plot
from util.plot.plot import Formatting
from util.misc import validate
import util.file_util as file_util
from util.commands import prompt_file_name, verify_and_load_results
from util.plot.series import plot_function, plot_series
from util.plot.shapes import draw_polygon, draw_line
from independent_set.result_models.suc_aug_concentration_results import SucAugConcentrationResults, generate_suc_aug_concentration_results_file_name
from independent_set.result_models.sa_results import SuccAugResults 
from typing import Callable, List, Tuple

LINE_FORMATTING: Formatting = Formatting(style="-", width="1", color="green", alpha=0.25)

COLOR_LIST: [str] = [
    "aqua",
    "blue",
    "crimson",
    "darkgreen",
    "gold",
    "lavender",
    "lime",
    "violet",
    "yellowgreen",
]


def __plot_result(sa: SuccAugResults, color: str, series_label: str):
    # Choose formatting
    formatting: Formatting = Formatting(color=color, alpha=0.75, label=series_label)
    # Define function and then run to graph
    def f(trial_num: int, sizes: List[int], intersection_sizes: List[int]):
        final_size: int = sizes[len(sizes) - 1]
        plot_series(sizes, intersection_sizes, formatting)
    sa.for_each_trial_results(f) 

@click.command()
@click.option(
    "--today",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to set file name to load to today's file name.",
)
@click.option(
    "--transient",
    required=False,
    is_flag=True,
    default=False,
    help="Shows the plot instead of saving.",
)
@click.option(
    "--dir-name",
    required=False,
    
)
# TODO: Put into separate graphs through an option.
def plot_sa_concentration(today, transient, dir_name):
    validate(transient or (dir_name is not None), f"Concentration graphs require either transient output or a directory name.")
    # ? Load results and generate file name if not set
    result: SucAugConcentrationResults = verify_and_load_results(
        today, generate_suc_aug_concentration_results_file_name, SucAugConcentrationResults, "independent_set"
    )
    # ? Create directory to store files in
    if not transient:
        file_util.create_dir_in_experiment_results_directory(dir_name, "independent_set")

    # ? Need to mess around with the structure a bit
    plot.initialize_figure(
        "Subset Size (s)", "Intersection Size", "Successive Augmentation Concentration", (40, 16)
    )


    # ? Go through each epsilon and graph appropriately for each
    counter: int = 0
    for epsilon in result.epsilon_values:
        color: str = COLOR_LIST[counter]
        counter = 0 if counter + 1 == len(COLOR_LIST) else counter + 1
        sa: SuccAugResults = result.get_results_for_epsilon(epsilon)
        __plot_result(sa, color, series_label=f"epsilon={epsilon}")
    
    # ? Add notes for the graph about the overall experiment
    # draw_line((0, 0), (max_size, max_size), LINE_FORMATTING)
    plot.add_notes(
        f"Graph Size: {result.n}\nPlanted Size: {result.planted_ind_set_size}\n",
        0.05,
        0.9,
    )
    plot.draw_legend()
    # ? Show the plot
    plot.show_or_save(transient, f"{dir_name}/all", "independent_set")
