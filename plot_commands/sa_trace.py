import click
import os
import sys

from util.storage import load
from util.results.sa_results import SuccAugResults, generate_sa_results_file_name
from util.plot.series import SeriesFormatting, plot_series, SeriesFormatting
import util.plot.plot as plot


SIZE_FORMATTING: SeriesFormatting = SeriesFormatting(
    "Subset Size", "gray", 1, False, "-o"
)

INTERSECTION_FORMATTING: SeriesFormatting = SeriesFormatting(
    "Intersection Size", "blue", 1, False, "-o"
    ) 

@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name to load to today's file name.")
@click.option("--file-name", required=False, help="The file name to save the graph as. Prompt will be provided if option not provided.")
def plot_sa_trace(today, file_name):
    if not today:
        pickle_name = click.prompt("Please enter the file to load results from", type=str)
    else:
        pickle_name = f"results/{generate_sa_results_file_name()}"

    if not os.path.isfile(f"{pickle_name}.pkl"):
        click.secho(f"The file provided could not be found.", err=True)
        sys.exit(0)

    results: SuccAugResults = load(pickle_name)
    if not results:
        click.secho("Could not load results.", err=True)
        sys.exit(0)

    if file_name is None:
        file_name = click.prompt("Please enter a name to save the graph as", type=str)
        if file_name is None:
            click.secho("Invalid file name provided.", err=True)
            sys.exit(0) 

    #? Gather data for series
    steps = list(range(results.n))
    intersection_sizes = list(results.intersection_results.collapse_to_list())
    sizes = list(results.size_results.collapse_to_list())

    plot.initialize_figure("Step", "", "Size / Intersection", (20, 8))
    plot_series(steps, sizes, SIZE_FORMATTING)
    plot_series(steps, intersection_sizes, INTERSECTION_FORMATTING)
    plot.show_plot()