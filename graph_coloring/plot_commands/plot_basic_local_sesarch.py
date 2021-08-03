from typing import List

import click

import util.plot.plot as plot
from graph_coloring.result_models.basic_local_search_results import \
    BasicLocalSearchResults, \
    ITERATIONS, \
    NUM_CONFLICTING_EDGES, \
    CHROMATIC_NUMBER
from util.plot.scatter import plot_scatter_data_from_tuple_with_trial_labels
from util.storage import load_experiment


@click.command()
@click.option("--results", type=str, required=True)
def plot_basic_local_search(results: str):
    results: BasicLocalSearchResults = load_experiment("graph_coloring", results)

    num_conflicting_edges: List[List[tuple]] = results.get_results(NUM_CONFLICTING_EDGES)
    iterations_taken: List[List[tuple]] = results.get_results(ITERATIONS)
    chromatic_numbers: List[List[tuple]] = results.get_results(CHROMATIC_NUMBER)

    # First initialize the figure 'canvas'
    plot.initialize_figure(
        x_label="Number of nodes",
        y_label="Number of conflicts after local optimization",
        title="Local Search (for a k-coloring, where k is optimal)",
        figsize=(10, 10)
    )

    # Now, plot the actual data
    plot_scatter_data_from_tuple_with_trial_labels(
        [chromatic_numbers, num_conflicting_edges],
        ['Chromatic Number (k)', '# Conf.']

    )
    for trial_num, trial in enumerate(zip(num_conflicting_edges, chromatic_numbers)):
        true_trial, found_trial = trial[0], trial[1]
        plot.annotate_all_points(
            [t[0] for t in found_trial],
            [t[1] for t in found_trial],
            [f"T{trial_num}"] * len(found_trial),
            x_offset=10,
            y_offset=10
        )
        plot.annotate_all_points(
            [t[0] for t in true_trial],
            [t[1] for t in true_trial],
            [f"T{trial_num}"] * len(true_trial),
            x_offset=10,
            y_offset=10
        )

    #
    # annotations: [str] = []
    # for i in range(len(true_chr_numbers)):
    #     n, true_chr_num = true_chr_numbers[i]
    #     annotations.append(found_chr_numbers[i][1])
    #
    # plot.annotate_all_points(
    #     [t[0] for t in true_chr_numbers],
    #     [t[1] for t in true_chr_numbers],
    #     annotations,
    #     x_offset=10,
    #     y_offset=10
    # )

    plot.show_plot()
