from copy import deepcopy
from typing import Callable

import click
import networkx as nx

import util.plot.plot as plot
import util.plot.series as series
from error_correcting_codes.commands.global_structure.results import \
    GlobalStructure
from util.commands import dir_plot_command, single_plot_command


@dir_plot_command("error_correcting_codes", GlobalStructure)
def _plot(results: GlobalStructure, save: Callable):
    num_parities: int = results.n * results.j // results.k
    plot.initialize_figure(
        x_label="Avg. Inverse Hamming Distance in GWW Pop (Number of matching bits)", 
        y_label=f"Parities Satisfied (out of {results.n * results.j // results.k}",
        title="Global vs. Local Progress in GWW Population"
    )
    series.plot_series(
        results.pop_inv_ham, 
        results.pop_parities,
        plot.Formatting(color="blue", label="Average. Parities Satisfied vs. Hamming Distance of GWW Pop.")
    )
    series.plot_series(
        results.pop_inv_ham,
        results.exp_parities,
        plot.Formatting(color="gray", label="Expected Parities Satisfied conditioned on Hamming Dist. of GWW Pop.")
    )
    plot.draw_legend()
    save("average-expected")
    
    data = []
    for i in range(len(results.pop_parities)):
        data.append((results.pop_parities[i], results.max_matching_bits[i]))
    data = sorted(data, key = lambda x: x[0])

    plot.initialize_figure(
        x_label="Prities Satisfied",
        y_label=f"Max Inverse Hamming Distance in GWW Pop (Number of matching bits)",
        title="Max Matching Bits with Original Message vs. Parities. (Is a particle close to original message?)"
    )
    series.plot_series(
        [x[0] for x in data],
        [x[1] for x in data]
    )
    save("max-matching-bits")


@click.command()
@click.option(
    "--today",
    required=False,
    is_flag=True,
    default=False,
)
@click.option(
    "--dir-name",
    required=True,
)
@click.option(
    "--transient",
    required=False,
    is_flag=True,
    default=False,
)
def global_structure(today, dir_name, transient):
    _plot(today, dir_name, transient)
