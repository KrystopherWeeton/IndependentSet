from typing import Callable, List

import click
import networkx as nx

import util.plot.graph as graph
import util.plot.plot as plot
import util.plot.series as series
from error_correcting_codes.commands.count_solutions.results import \
    SolutionCount
from util.commands import dir_plot_command


@dir_plot_command("error_correcting_codes", SolutionCount)
def _plot(results: SolutionCount, save: Callable):
    n_values, num_solutions = results.get_series()
    print(num_solutions)
    percentage_of_solutions: List[int] = [
        num_solutions[i] / (2**n_values[i]) for i in range(len(n_values))
    ]
    plot.initialize_figure(
        "n", "num solutions", f"Number of solutions with all parities satisfied"
    )
    series.plot_series(n_values, num_solutions, annotate_points=True)
    save("num-solutions")
    plot.initialize_figure(
        "n", "Percentage of Solutions", "Percentage of solutions with all parities satisfied"
    )
    series.plot_series(n_values, percentage_of_solutions, annotate_points=True)
    save("perc-solutions")

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
def count_solutions(today, dir_name, transient):
    _plot(today, dir_name, transient)
