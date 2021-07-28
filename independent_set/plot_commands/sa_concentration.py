import os
import sys

import click

import util.plot.plot as plot
from util.plot.plot import Formatting
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

@click.command()
@click.option(
    "--today",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to set file name to load to today's file name.",
)
@click.option(
    "--file-name",
    required=False,
    help="The file name to save the graph as. Prompt will be provided if option not provided.",
)
@click.option(
    "--transient",
    required=False,
    is_flag=True,
    default=False,
    help="Shows the plot instead of saving.",
)
def plot_sa_concentration(today, file_name, transient):
    # ? Load results and generate file name if not set
    result: SucAugConcentrationResults = verify_and_load_results(
        today, generate_suc_aug_concentration_results_file_name, SucAugConcentrationResults, "independent_set"
    )
    if not transient:
        file_name = prompt_file_name(file_name)

    # ? Need to mess around with the structure a bit
    plot.initialize_figure(
        "Subset Size (s)", "Intersection Size", "Successive Augmentation Concentration", (40, 16)
    )

    # ? Go throughe ach epsilon and graph appropriately for each
    # TODO: Set different colors for each different graph here
    max_size: int = -1
    counter: int = 0
    for epsilon in result.epsilon_values:
        # Choose formatting for this epsilon value
        formatting: Formatting = Formatting(color=COLOR_LIST[counter], alpha=0.75, label=f"epsilon={epsilon}")
        counter = 0 if counter + 1 == len(COLOR_LIST) else counter + 1
        # Graph the results for this epsilon
        sa: SuccAugResults = result.get_results_for_epsilon(epsilon)
        def f(trial_num: int, sizes: List[int], intersection_sizes: List[int]):
            nonlocal max_size
            final_size: int = sizes[len(sizes) - 1]
            max_size = max_size if final_size < max_size else final_size
            plot_series(sizes, intersection_sizes, formatting)
        sa.for_each_trial_results(f)
    
    # ? Add notes for the graph about the overall experiment
    # draw_line((0, 0), (max_size, max_size), LINE_FORMATTING)
    plot.add_notes(
        f"Graph Size: {result.n}\nPlanted Size: {result.planted_ind_set_size}\n",
        0.05,
        0.9,
    )
    plot.draw_legend()

    # ? Save / show plot
    if transient:
        plot.show_plot()
    else:
        plot.save_plot(file_name, "independent_set")
