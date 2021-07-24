import click

import util.plot.plot as plot
from graph_coloring.result_models.basic_heuristic_results import BasicHeuristicResults
from util.plot.scatter import plot_scatter_data_from_tuple_with_trial_labels
from util.storage import load_experiment


@click.command()
@click.option("--results", required=True)
def plot_basic_heuristic(results: str):
    results: BasicHeuristicResults = load_experiment("graph_coloring", results)

    true_chr_numbers: list = results.get_true_chr_numbers()
    found_chr_numbers: list = results.get_found_chr_numbers()

    # First initialize the figure 'canvas'
    plot.initialize_figure(
        x_label="Number of nodes",
        y_label="Chromatic #",
        title="FRG results"
    )

    # Now, plot the actual data
    plot_scatter_data_from_tuple_with_trial_labels(
        [true_chr_numbers, found_chr_numbers],
        ["True", "Found"]
    )
    for trial_num, trial in enumerate(zip(true_chr_numbers, found_chr_numbers)):
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
