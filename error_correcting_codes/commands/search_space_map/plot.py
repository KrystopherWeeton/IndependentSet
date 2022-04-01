from typing import Callable, List

import click
import networkx as nx

import util.file_util as file_util
import util.plot.graph as graph
import util.plot.plot as plot
import util.plot.series as series
from error_correcting_codes.commands.correction_series.results import \
    CorrectionSeriesResults
from error_correcting_codes.commands.search_space_map.results import \
    SearchSpaceMap
from util.commands import dir_plot_command, verify_and_load_results_v2
from util.plot.color import generate_red_range


@click.command()
@click.option(
    "--today",
    required=False,
    is_flag=True,
    default=False,
)
@click.option(
    "--dir-name",
    required=False,
)
@click.option(
    "--transient",
    required=False,
    is_flag=True,
    default=False,
)
def search_space_map(today, dir_name, transient):
    _plot(today, dir_name, transient)


@dir_plot_command("error_correcting_codes", SearchSpaceMap)
def _plot(results: SearchSpaceMap, save: Callable)
    for t in range(results.num_trials):
        G: nx.Graph = results.get_search_space(t)
        #print([G.nodes[n]['attr']['local'] for n in G.nodes])
        # Color vertices based on global score
        gradient: List = generate_red_range(results.n + 1)
        #print("gradient", gradient)
        graph.draw_gradient_graph(
            g=G,
            #get_label = lambda x: "h",
            #get_label=lambda x: f"({x['attr']['local']}, {x['attr']['global']})",
            get_color=lambda x: gradient[int(x['attr']['local'])],
            iterations=10
        )
    save("normalized")
