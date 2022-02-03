import os
import sys
from decimal import *
from math import ceil, e
from typing import Callable, List, Tuple

import click

import util.plot.plot as plot
import util.plot.series as series
from independent_set.result_models.convergence_results import \
    ConvergenceResults
from util.commands import prompt_file_name, verify_and_load_results_v2
from util.plot.plot import Formatting
from util.plot.shapes import draw_line

FORMATTING: Formatting = Formatting(color="orange", alpha=0.5, width=0.5)

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
def convergence_plot(today, file_name, transient):
    # ? Load results and generate file name if not set
    results: ConvergenceResults = verify_and_load_results_v2(ConvergenceResults, "independent_set", today)
    if not transient:
        file_name = prompt_file_name(file_name)

    for i in range(len(results.n_values)):
        n: int = results.n_values[i]
        k: int = results.k_values[i]
        seed_int_size: int = results.seeed_int_sizes[i]

        intersections: List[List[int]] = results.get_results(n)
        plot.initialize_figure("Step", "Num. non-planted vertices in solution", "Convergence Speed of local optimization", (40, 16))
        for l in intersections:
            print(l)
            series.plot_series(range(len(l)), l, FORMATTING)

    if transient:
        plot.show_plot()
    else:
        plot.save_plot(file_name, "independent_set")
