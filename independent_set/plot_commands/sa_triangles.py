import os
import sys

import click

import util.plot.plot as plot
from util.plot.shapes import draw_polygon, draw_line, LineFormatting
from util.commands import prompt_file_name, verify_and_load_results
from util.plot.series import plot_function, plot_series
from util.plot.shapes import draw_line, LineFormatting
from independent_set.result_models.sa_results import (SuccAugResults,
                                     generate_sa_results_file_name)
from typing import Callable, List, Tuple
from math import e, ceil
from decimal import *

SIZE_FORMATTING: plot.Formatting = plot.Formatting(
    "Subset Size", "gray", 1, False, "-o"
)

INTERSECTION_FORMATTING: plot.Formatting = plot.Formatting(
    "Intersection Size", "blue", 1, False, "-o"
    ) 

LINE_FORMATTING: LineFormatting = LineFormatting(
    style="-", width="1", color="green", alpha=0.5
)

####### TRIANGLE FORMATTING AND SUPPORT #############

TRIANGLE_FORMATTING: LineFormatting = LineFormatting(style="-", width="1", color="orange", alpha=0.5)
# The 'length' of each phase, allowed to be a function of n
def T(m: int) -> int:
    return m // 10


def __generate_triangle(s: int, k: int, t: int) -> List[Tuple[int, int]]:
    """ Generates a triangle from provided left point s, k """
    return [(s, k), (s + t, k), (s + t, k + t)]


def __probability_of_good_move_estimator(omega: int, n: int, s: int, k: int, epsilon: int) -> float:
    if s == k:
        pg: float = omega / (2 * n)
        pb: float = (1 - omega / n) * e**(- s)
    else:
        pg: Decimal = (omega / n) * e**( - (epsilon**2) / (s - k))
        pb_exponent: Decimal = - ((k+2 * epsilon)**2 / s)
        pb: Decimal = (1 - omega / n) * e**( pb_exponent)
    return float(pg / (pg + pb))

def __expected_height(omega: int, n: int, s: int, k: int, epsilon: int, t: int) -> float:
    return t * __probability_of_good_move_estimator(omega, n, s, k, epsilon)


def __slack(alpha: float, t: int, m: int) -> float:
    # TODO: What slack do we want to actually test?
    # for now we can just ignore this and examine concentration
    # around the expectation.
    return t/4


@click.command()
@click.option("--today", required=False, is_flag=True, default=False, help="Flag to set file name to load to today's file name.")
@click.option("--file-name", required=False, help="The file name to save the graph as. Prompt will be provided if option not provided.")
@click.option("--transient", required=False, is_flag=True, default=False, help="Shows the plot instead of saving.")
def plot_sa_triangles(today, file_name, transient):
    #? Load results and generate file name if not set
    results: SuccAugResults = verify_and_load_results(
        today, generate_sa_results_file_name, SuccAugResults, "independent_set"
    )
    if not transient:
        file_name = prompt_file_name(file_name)

    #? Need to mess around with the structure a bit
    plot.initialize_figure("Subset Size (s)", "Intersection Size", "Size vs. Intersection", (40, 16))

    #? For each trial, plot results for that trial
    max_size: int = -1
    def f(trial_num: int, sizes: List[int], intersection_sizes: List[int]):
        nonlocal max_size
        final_size: int = sizes[len(sizes) - 1]
        max_size = max_size if final_size < max_size else final_size
        plot_series(sizes, intersection_sizes, SIZE_FORMATTING)

    results.for_each_trial_results(f)

    draw_line((0, 0), (max_size, max_size), LINE_FORMATTING)
    

    """
    #? Calculate and then draw triangles
    m: int = max_size
    t: int = T(m)
    omega: int = results.planted_size
    n: int = results.n
    epsilon: int = results.epsilon
    num_triangles: int = (m - results.headstart_size) // t
    origin = (results.headstart_size, results.headstart_size)
    triangles = []
    while origin[0] < m:
        triangle = __generate_triangle(origin[0], origin[1], t)
        draw_polygon(triangle, formatting=TRIANGLE_FORMATTING)
        s: int = origin[0]
        k: int = origin[1]
        expected_height: int = __expected_height(omega, n, s, k, epsilon, t)
        min_location: int = expected_height - __slack(1, t, 1)
        origin = (origin[0] + t, ceil(origin[1] + min_location))
    """

    #? Add notes for the graph about the overall experiment
    plot.add_notes(
        f"Graph Size: {results.n}\nPlanted Size: {results.planted_size}\n", 
        0.05,
        0.9,
    )

    if transient:
        plot.show_plot()
    else:
        plot.save_plot(file_name, "independent_set")