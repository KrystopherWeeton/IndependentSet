import math
import click
import os
import sys
import networkx as nx

from util.storage import load
from util.results.heuristic_results import HeuristicResults, generate_heuristic_results_file_name, StatInfo
import util.plot as plot
from util.misc import round_all_values

@click.group()
def run():
    pass

def __generate_graphs(results: HeuristicResults, directory: str):
    directory = plot.create_dir(directory, agressive=True)

    n_values: [int] = results.get_n_values()

    intersection_sizes: [StatInfo] = results.get_all_intersection_size_info()
    densities: [StatInfo] = results.get_all_density_info()
    subset_sizes: [StatInfo] = results.get_all_subset_size_info()

    intersection_means: [float] = [x.mean for x in intersection_sizes]

    planted_sizes = [
        results.planted_sizes[n] for n in n_values
    ]

    intersection_data: [[float]] = results.get_intersection_data()
    subset_data: [[float]] = results.get_subset_size_data()

    plot.plot_scatter_data(
        x_points=n_values,
        y_points=intersection_data,
        title="Resulting Planted Independent Set Intersection",
        x_title="Number of Vertices (n)",
        y_title="Planted Ind. Set Intersection Size",
        file_name="intersection-sizes",
        other_y_series=[intersection_means, planted_sizes],
        other_y_formatting=[plot.LIGHT_GRAY("Average"), plot.LIGHT_GREEN("Planted Size")],
        directory=directory,
        x_spacing=5,
        y_spacing=0.25
    )

    plot.plot_scatter_data(
        x_points=n_values,
        y_points=subset_data,
        title="Resulting Subset Sizes",
        x_title="Number of Vertices (n)",
        y_title="Resulting Subset Size",
        file_name="subset-sizes",
        other_y_series=[[x.mean for x in subset_sizes]],
        other_y_formatting=[plot.LIGHT_GRAY("Average")],
        directory=directory,
        x_spacing=5,
        y_spacing=0.25
    )


@run.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name automatically to results generated today.")
def generate_graphs(today):
    if not today:
        pickle_name = click.prompt("Please enter the file for the results", type=str)
    else:
        pickle_name = f"results/{generate_heuristic_results_file_name()}"

    if not os.path.isfile(f"{pickle_name}.pkl"):
        click.secho(f"The file at {pickle_name}.pkl could not be found.", err=True)
        sys.exit(0)
    
    results: HeuristicResults = load(pickle_name)
    if not results:
        click.secho("Could not load results.", err=True)
        sys.exit(0)
    
    results_directory = click.prompt("Please enter a directory to store the graphs in.", type=str)
    __generate_graphs(results, results_directory)


if __name__ == "__main__":
    run()