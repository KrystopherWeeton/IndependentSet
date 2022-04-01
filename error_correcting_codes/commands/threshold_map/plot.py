import click
import networkx as nx

import util.file_util as file_util
import util.plot.graph as graph
import util.plot.plot as plot
from error_correcting_codes.commands.threshold_map.results import ThresholdMap
from util.commands import verify_and_load_results_v2


def _plot(today, dir_name, transient):
    if not transient:
        dir_name = file_util.create_dir_in_experiment_results_directory(dir_name, "error_correcting_codes")
    results: ThresholdMap = verify_and_load_results_v2(ThresholdMap, "error_correcting_codes", today)

    for threshold in results.get_all_thresholds():
        g: nx.Graph = results.get_search_space(threshold)
        #labels = nx.get_node_attributes(g, "score")
        labels = None
        colorings = {tuple([0] * results.n): "red"}
        graph.draw_graph(g, iterations=50, labels=labels, colorings=colorings)
        plot.show_or_save(transient, f"{dir_name}/threshold-{threshold}", "error_correcting_codes")

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
def threshold_map(today, dir_name, transient):
    _plot(today, dir_name, transient)
