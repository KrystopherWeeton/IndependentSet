import os
import sys

import click

import util.plot.heatmap as heatmap
import util.plot.plot as plot
from independent_set.result_models.size_results import SizeResults
from util.commands import verify_and_load_results_v2
from util.storage import load


@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name to load to today's file name.")
@click.option("--file-name", required=False, help="The file name to save the graph as. Prompt will be provided if option not provided.")
def plot_size_heatmap(today, file_name):
    results: SizeResults = verify_and_load_results_v2(SizeResults, "independent_set", today)

    if file_name is None:
        file_name = click.prompt("Please enter a name to save the graph as", type=str)
        if file_name is None:
            click.secho("Invalid file name provided.", err=True)
            sys.exit(0)

    heatmap.graph_heatmap(
        x = results.k_values,
        y = results.n_values,
        z = results.get_avg_heatmap_values(),
        title="Performance of Fixed Size GWW",
        x_axis_title="Fixed Subset Size",
        y_axis_title="Number of vertices (n)",
        color=heatmap.HeatMapColor.YELLOW_GREEN,
        include_annotation=True,
        plot_size=10
    )
    plot.save_plot(file_name, "independent_set")
