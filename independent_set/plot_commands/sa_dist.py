from typing import List

import click

import util.plot.plot as plot
from independent_set.result_models.sa_distribution_results import \
    SADistributionResults
from util.commands import prompt_file_name, verify_and_load_results
from util.file_util import (create_dir,
                            create_dir_in_experiment_results_directory)
from util.formulas import std_dev
from util.plot.candlestick import CandlePlot
from util.plot.heatmap import graph_heatmap
from util.plot.scatter import plot_scatter_data


def __save_if_not_transient(transient: bool, path: str):
    if transient:
        plot.show_plot()
    else:
        plot.save_plot(path, "independent_set")
 


@click.command()
@click.option(
    "--today",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to set file name to load to today's file name.",
)
@click.option(
    "--dir-name",
    required=False,
    help="The dir name to save the graphs in. Prompt will be provided if option not provided.",
)
@click.option(
    "--transient",
    required=False,
    is_flag=True,
    default=False,
    help="Shows the plot instead of saving.",
)
def sa_dist(today, dir_name, transient):
    results: SADistributionResults = verify_and_load_results(
        today,
        #! Don't do this. This is absurdly bad practice and should be fixed ASAP
        SADistributionResults.generate_file_name,
        SADistributionResults,
        "independent_set",
    )

    directory = None
    if not transient:
        directory: str = create_dir_in_experiment_results_directory(prompt_file_name(dir_name), "independent_set")


    #? Plot figure for num appearances to test uniformity
    plot.initialize_figure(
        "Planted Ind Set Vertices",
        "",
        "Frequency of Appearance in Final Solution",
        (40, 4),
    )
    occurrences: List[int] = results.get_num_appearances_for_each_planted_vertex()
    x: List[int] = [t[0] for t in occurrences]
    y: List[int] = [0]
    z: List[int] = [t[1] for t in occurrences]
    graph_heatmap(
        x=x,
        y=y,
        z=[z],
        min=min(x),
        max=max(x),
        include_tick_labels=False,
    )
    plot.add_notes(f"Std Dev = {std_dev(z):0.2f}", 0.0, 1.2)

    __save_if_not_transient(transient, f"{directory}/frequency")

    #? Plot figure for non-int size to see how much we can rely on getting a subset
    plot.initialize_figure(
        "Trial Number",
        "Num of Non Planted Vertices in Final Solution",
        "Number of non-planted vertices in final solutions",
        (10, 8)
    )

    candle: CandlePlot = CandlePlot(showmeans=True)
    candle.add_candlestick(results.get_final_sizes_minus_intersections(), "Num. non-planted Vertices")
    candle.add_candlestick(results.final_sizes, "Final Sizes")
    candle.add_candlestick(z, "Num Appearances Per Planted Vertex")
    candle.plot()


    __save_if_not_transient(transient, f"{directory}/non-planted")
