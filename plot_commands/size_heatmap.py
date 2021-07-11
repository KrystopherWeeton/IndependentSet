import os
import sys

import click

import util.plot.heatmap as heatmap
from util.results.size_results import (SizeResults,
                                       generate_size_results_file_name)
from util.storage import load


@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name to load to today's file name.")
@click.option("--file-name", required=False, help="The file name to save the graph as. Prompt will be provided if option not provided.")
def plot_size_heatmap(today, file_name):
    if not today:
        pickle_name = click.prompt("Please enter the file to load results from", type=str)
    else:
        pickle_name = f"results/{generate_size_results_file_name()}"

    if not os.path.isfile(f"{pickle_name}.pkl"):
        click.secho(f"The file provided could not be found.", err=True)
        sys.exit(0)
    
    results: SizeResults = load(pickle_name)
    if not results:
        click.secho("Could not load results.", err=True)
        sys.exit(0)

    if file_name is None:
        file_name = click.prompt("Please enter a name to save the graph as", type=str)
        if file_name is None:
            click.secho("Invalid file name provided.", err=True)
            sys.exit(0)

    heatmap.graph_heatmap(
        x = results.k_values,
        y = results.n_values,
        z = results.get_avg_heatmap_values(),
        directory="results",
        file_name=file_name,
        title="Performance of Fixed Size GWW",
        x_axis_title="Fixed Subset Size",
        y_axis_title="Number of vertices (n)",
        color=heatmap.HeatMapColor.YELLOW_GREEN,
        include_annotation=True,
        plot_size=10
    )