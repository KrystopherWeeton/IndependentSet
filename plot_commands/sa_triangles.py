import click
import os
import sys

from util.results.sa_results import SuccAugResults, generate_sa_results_file_name
from util.plot.series import SeriesFormatting, plot_series, SeriesFormatting, plot_function
import util.plot.plot as plot
from plot_commands.util import verify_and_load_results, prompt_file_name


SIZE_FORMATTING: SeriesFormatting = SeriesFormatting(
    "Subset Size", "gray", 1, False, "-o"
)

INTERSECTION_FORMATTING: SeriesFormatting = SeriesFormatting(
    "Intersection Size", "blue", 1, False, "-o"
    ) 

LINE_FORMATTING: SeriesFormatting = SeriesFormatting(
    "Ideal Subset Line ", "green", 1, False, "-o"
)

NUM_ANNOTATIONS: int = 10   # The number of annotations to include in the graph

@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name to load to today's file name.")
@click.option("--file-name", required=False, help="The file name to save the graph as. Prompt will be provided if option not provided.")
@click.option("--transient", required=False, is_flag=True, default=False, help="Shows the plot instead of saving.")
def plot_sa_triangles(today, file_name, transient):
    #? Load results and generate file name if not set
    results: SuccAugResults = verify_and_load_results(
        today, generate_sa_results_file_name, SuccAugResults
    )
    file_name = prompt_file_name(file_name)

    #? Gather data for series
    steps = results.step_values
    intersection_sizes = list(results.intersection_results.collapse_to_list())
    sizes = list(results.size_results.collapse_to_list())

    #? Need to mess around with the structure a bit
    plot.initialize_figure("Subset Size (s)", "Intersection Size", "Size vs. Intersection", (20, 8))
    plot_function(sizes, lambda x: x, LINE_FORMATTING)
    plot_series(sizes, intersection_sizes, SIZE_FORMATTING)
    plot.annotate_points(
        sizes, 
        intersection_sizes, 
        results.n // NUM_ANNOTATIONS, 
        lambda x, y : f"{y :.2f}",
        0,
        50
    )

    plot.add_notes(
        f"Graph Size: {results.n}\nPlanted Size: {results.planted_size}\nSize: {results.final_size}\nIntersection: {results.final_intersection}", 
        0.05,
        0.9,
    )

    if transient:
        plot.show_plot()
    else:
        plot.save_plot(file_name, directory="results")