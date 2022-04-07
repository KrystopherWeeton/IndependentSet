from copy import deepcopy
from typing import Callable

import click
import networkx as nx

import util.plot.graph as graph
from error_correcting_codes.commands.global_structure.results import \
    GlobalStructure
from util.commands import dir_plot_command


@dir_plot_command("error_correcting_codes", GlobalStructure)
def _plot(results, save: Callable):
    for threshold in results.get_all_thresholds():
        g: nx.Graph = results.get_search_space(threshold)
        #labels = nx.get_node_attributes(g, "score")
        labels = None
        colorings = {}
        for x in g.nodes:
            if g.nodes[x]['score'] >= 11:
                colorings[x] = "green"
        colorings[tuple([0] * results.n)] = "red"
        graph.draw_graph(g, results.n, iterations=50, labels=labels, colorings=colorings)
        save(f"threshold-{threshold}")

        g2: nx.Graph = deepcopy(g)
        for x in g.nodes:
            if x == tuple([0] * results.n):
                print('considering', x)
                print(len(g.edges(x)))
                print(len(g.edges(x)) == 0)
            if len(g.edges(x)) == 0:
                g2.remove_node(x)
        colorings = {x: "green" for x in g2.nodes if g2.nodes[x]['score'] >= 11}
        colorings[tuple([0] * results.n)] = "red"
        graph.draw_graph(g2, results.n, labels=None, colorings=colorings)
        save(f"threshold-isolated-removed-{threshold}")

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
def global_structure(today, dir_name, transient):
    _plot(today, dir_name, transient)
