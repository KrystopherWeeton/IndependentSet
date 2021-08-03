import os
import sys

import click

import util.plot.plot as plot
from independent_set.result_models.sa_results import (
    SuccAugResults, generate_sa_results_file_name)
from util.commands import prompt_file_name, verify_and_load_results
from util.plot.series import plot_series


@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name to load to today's file name.")
@click.option("--file-name", required=False, help="The file name to save the graph as. Prompt will be provided if option not provided.")
@click.option("--transient", required=False, is_flag=True, default=False, help="Shows the plot instead of saving.")
def sa_dist(today, file_name, transient):

    if transient:
        plot.show_plot()
    else:
        plot.save_plot(file_name, "independent_set")
