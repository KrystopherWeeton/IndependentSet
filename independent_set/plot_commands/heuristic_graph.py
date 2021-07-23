import math
import os
import sys

import click
import networkx as nx

import util.file_util as file_util
import util.plot.plot as plot
import util.plot.series as series
import util.plot.scatter as scatter
from util.commands import verify_and_load_results
from independent_set.result_models.heuristic_results import (
    HeuristicResults, StatInfo, generate_heuristic_results_file_name)
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

    scatter.plot_scatter_data(
        x_points=n_values,
        y_points=intersection_data,
        title="Resulting Planted Independent Set Intersection",
        x_title="Number of Vertices (n)",
        y_title="Planted Ind. Set Intersection Size",
        other_y_series=[intersection_means, planted_sizes],
        other_y_formatting=[series.LIGHT_GRAY("Average"), series.LIGHT_GREEN("Planted Size")],
        x_spacing=5,
        y_spacing=0.25
    )
    plot.save_plot(file_name="intersection-sizes", project_name="independent_set", folder=folder)

    scatter.plot_scatter_data(
        x_points=n_values,
        y_points=subset_data,
        title="Resulting Subset Sizes",
        x_title="Number of Vertices (n)",
        y_title="Resulting Subset Size",
        other_y_series=[[x.mean for x in subset_sizes]],
        other_y_formatting=[series.LIGHT_GRAY("Average")],
        x_spacing=5,
        y_spacing=0.25
    )
    plot.save_plot(file_name="subset-sizes", project_name="independent_set", folder=folder)