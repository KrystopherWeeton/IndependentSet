import click

import util.plot.plot as plot
from graph_coloring.result_models.basic_heuristic_results import BasicHeuristicResults
from util.plot.scatter import plot_scatter_data
from util.storage import load_experiment


@click.command()
@click.option("--results", required=True)
def plot_basic_heuristic(results: str):
    results: BasicHeuristicResults = load_experiment("graph_coloring", results)

    true_chr_numbers: list = results.get_all_true_chr_numbers()
    found_chr_numbers: list = results.get_all_found_chr_numbers()

    # TODO: make plot scatter data take in tuples
    plot_scatter_data(
        [numbers[0] for numbers in found_chr_numbers],
        [[numbers[1] for numbers in found_chr_numbers], [numbers[1] for numbers in true_chr_numbers]],
        "FRG results",
        "Number of Nodes",
        "Chromatic #"
    )
    plot.show_plot()
