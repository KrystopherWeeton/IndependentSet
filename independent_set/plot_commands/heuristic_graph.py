import os
import sys

import click

import util.plot.plot as plot
import util.plot.scatter as scatter
from independent_set.result_models.heuristic_results import (
    HeuristicResults, StatInfo, generate_heuristic_results_file_name)
from util.commands import verify_and_load_results
from util.storage import load


@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to indicate to use results from today")
@click.option("--folder", required=True, help="The folder to save the graphs into")
def plot_heuristics_graphs(today, folder):
    results: HeuristicResults = verify_and_load_results(today, generate_heuristic_results_file_name, HeuristicResults, "independent_set")
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
    
    folder = file_util.create_dir_in_experiment_results_directory(folder, "independent_set")


    plot.initialize_figure(
        x_label="Number of Vertices (n)",
        y_label="Planted Ind. Set Intersection Size",
        title="Resulting Planted Independent Set Intersection",
    )
    scatter.plot_scatter_data(
        x_points=n_values,
        y_points=intersection_data,
        other_y_series=[intersection_means, planted_sizes],
        other_y_formatting=[plot.LIGHT_GRAY("Average"), plot.LIGHT_GREEN("Planted Size")],
        x_spacing=5,
        y_spacing=0.25
    )
    plot.save_plot(file_name="intersection-sizes", project_name="independent_set", folder=folder)

    plot.initialize_figure(
        x_label="Number of Vertices (n)",
        y_label="Resulting Subset Size",
        title="Resulting Subset Sizes",
    )
    scatter.plot_scatter_data(
        x_points=n_values,
        y_points=subset_data,
        other_y_series=[[x.mean for x in subset_sizes]],
        other_y_formatting=[plot.LIGHT_GRAY("Average")],
        x_spacing=5,
        y_spacing=0.25
    )
    plot.save_plot(file_name="subset-sizes", project_name="independent_set", folder=folder)

@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to indicate to use results from today")
@click.option("--folder", required=True, help="The folder to save the graphs into")
def plot_heuristics_graphs(today, folder):
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

    __generate_graphs(results, folder)
