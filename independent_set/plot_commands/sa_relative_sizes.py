import inspect
import math
import os
import sys
from dataclasses import dataclass
from decimal import *
from typing import Callable, List, Set, Tuple

import click

import util.file_util as file_util
import util.plot.plot as plot
from independent_set.result_models.sa_results import SuccAugResults
from util.commands import prompt_file_name, verify_and_load_results_v2
from util.misc import source_code, validate
from util.plot.plot import Formatting
from util.plot.series import plot_series
from util.plot.shapes import draw_line

SIZE_FORMATTING: Formatting =           Formatting(color="blue", alpha=0.5, include_markers=False, label="Subset Size")
INTERSECTION_FORMATTING: Formatting =   Formatting(color="red", alpha=0.5, include_markers=False, label="Intersection Size")
LINE_FORMATTING: Formatting =           Formatting(color="gray", alpha=1, include_markers=False, label="Function")

#! Keep these functions to a single line so their output in the graphs looks nice.

"""The function defining the 'invariant' you want to test the intersection for"""
def invariant(x: int) -> int:
    return int(math.sqrt(x))

""" 
The point at which 'random restarts' should be considered, e.g. we analyze how
many runs hit a certain threshold at this point, and what happens to the runs
which hit this threshold.
"""
def random_restart_point(n: int) -> int:
    return int(n/4)

"""
The threshold, under which we 'throw away' results
"""
def random_restart_threshold(s: int) -> int:
    return 2 * int(math.sqrt(s))


def plot_overview(transient: bool, directory_name: str, results: SuccAugResults):
    #* (PLOT 1) All runs overlayed onto a graph. Every piece of information
    plot.initialize_figure("Step", "Subset / Intersection Size", "Relative Intersection / Size", (40, 16))
    # ? Plot lines for actual results
    def f(trial_num: int, sizes: List[int], intersection_sizes: List[int]):
        """ Plot a specific trial"""
        plot_series(results.step_values, sizes, SIZE_FORMATTING)
        plot_series(results.step_values, intersection_sizes, INTERSECTION_FORMATTING)
    results.for_each_trial_results(f)
    plot_series(results.step_values, [3 * math.sqrt(x) for x in results.step_values], Formatting("orange", 1))
    plot.add_notes(
        f"Graph Size: {results.n}\nPlanted Size: {results.planted_size}\n",
        0.05,
        0.9,
    ) 
    plot.show_or_save(transient, f"{directory_name}/all-runs", "independent_set")

    #* (Plot 2) Mean case on a graph, with invariant plotted
    # NOTE: Includes analysis of how many runs actually 
    mean_sizes: List[int] = results.size_results.collapse_to_list()
    mean_intersection: List[int] = results.intersection_results.collapse_to_list()
    mean_invariant: List[int] = [invariant(x) for x in mean_sizes]
    plot.initialize_figure("Step", "Mean Size / Intersection", "Avg. Size / Intersection", (40, 16))
    plot_series(results.step_values, mean_sizes, SIZE_FORMATTING)
    plot_series(results.step_values, mean_intersection, INTERSECTION_FORMATTING)
    plot_series(results.step_values, mean_invariant, LINE_FORMATTING)
    plot.show_or_save(transient, f"{directory_name}/mean-case", "independent_set")


def plot_fixed_threshold(transient: bool, directory_name: str, results: SuccAugResults):
    #* (ANALYSIS) A bit of simple calculations on the portions
    #* (Plot 3) All the 'good' runs, those that hit the threshold
    #* (Plot 4) All the 'bad' runs, those that didn't hit the threshold
    # (1) The portion which maintained the invariant throughout the entire run
    # (2) The portion maintaining the invariant, restricted to those that
    # hit a certain threshold at a certain point (provided in metadata)
    # (3) The number of runs actually hitting that threshold (also percentage)
    # Go through and organize trials
    invariant_runs: Set[int] = set()            # The runs which maintain the invariant throughout the entire run
    non_invariant_runs: Set[int] = set()        # The runs which don't maintain the invariant throughout the entire run
    threshold_runs: Set[int] = set()            # The runs which make the cutoff threshold specified
    non_threshold_runs: Set[int] = set()        # The runs which don't make the cutoff threshold specified
    random_restart_index: int = random_restart_point(results.n)
    def store_good_run(trial_num: int, sizes: List[int], intersection_sizes: List[int]):
        invariant_data: List[int] = [invariant(x) for x in sizes]
        # Perform all validation of the run
        maintains_invariant: bool = all([intersection_sizes[i] >= invariant_data[i] for i in range(len(sizes))])
        satisfies_threshold: bool = intersection_sizes[random_restart_index] >= random_restart_threshold(sizes[random_restart_index])
        # Track invariant maintenance
        if maintains_invariant:
            invariant_runs.add(trial_num)
        else:
            non_invariant_runs.add(trial_num)
        # Track threshold runs
        if satisfies_threshold:
            threshold_runs.add(trial_num)
        else:
            non_threshold_runs.add(trial_num)
    results.for_each_trial_results(store_good_run)    
    note: str =     f"""
                        Runs maintaining invariant: {len(invariant_runs)} - Runs not maintaining invariant: {len(non_invariant_runs)}\n
                        Runs satisfying threshold: {len(threshold_runs)} - Runs not satisfying threshold: {len(non_threshold_runs)}\n
                        Runs satisfying threshold and maintaining invariant: {len(threshold_runs.intersection(invariant_runs))}\n
                        Runs satisfying threshold but not maintaining invariant: {len(threshold_runs.intersection(non_invariant_runs))}\n
                        Runs not satisfying threshold but maintaining invariant: {len(non_threshold_runs.intersection(invariant_runs))}\n
                        \n
                        Invariant: {source_code(invariant)[0]}\n
                        Random restart point: {source_code(random_restart_point)[0]}\n
                        Random restart threshold: {source_code(random_restart_threshold)[0]}\n
                    """


    def add_runs_to_plot(trial_numbers: Set[int]):
        for t in trial_numbers:
            plot_series(results.step_values, list(results.size_results.get_sub_tensor("trial", t)), SIZE_FORMATTING)
            plot_series(results.step_values, list(results.intersection_results.get_sub_tensor("trial", t)), INTERSECTION_FORMATTING)

    plot.initialize_figure("Step", "Subset / Intersection Size", "Intersection / Size for invariant Maintaining Runs", (40, 16))
    add_runs_to_plot(invariant_runs)
    plot.add_notes(note, 0.05, 0.8)
    plot.show_or_save(transient, f"{directory_name}/invariant-runs", "independent_set")

    plot.initialize_figure("Step", "Subset / Intersection Size", "Intersection / Size for non-invariant Maintaining Runs", (40, 16))
    add_runs_to_plot(non_invariant_runs)
    plot.add_notes(note, 0.05, 0.8)
    plot.show_or_save(transient, f"{directory_name}/non-invariant-runs", "independent_set")

    plot.initialize_figure("Step", "Subset / Intersection Size", "Intersection / Size for runs hitting threshold", (40, 16))
    add_runs_to_plot(threshold_runs)
    plot.add_notes(note, 0.05, 0.8)
    plot.show_or_save(transient, f"{directory_name}/threshold-runs", "independent_set")

    plot.initialize_figure("Step", "Subset / Intersection Size", "Intersection / Size for runs not hitting threshold", (40, 16))
    add_runs_to_plot(non_threshold_runs)
    plot.add_notes(note, 0.05, 0.8)
    plot.show_or_save(transient, f"{directory_name}/non-threshold-runs", "independent_set")


def plot_varied_threshold(transient: bool, directory_name: str, results: SuccAugResults):
    #* PLOT 4 (Fixed random restart point, vary the threshold and see, at that threshold, how many runs are ultimately successful)
    def threshold_metric(s: int, intersection: int) -> float:
        # We are using the intersection as the thing we want to measure for the threshold, may try
        # to adjust to size to see if that can fix at least 1/2 of our issues requiring oracles.
        return intersection
    
    def threshold_range() -> List[int]:
        # The values that the threshold can take
        return list(range(100))

    @dataclass
    class RestartData:
        size: int
        intersection: int
        trial_number: int

    restart_cache: List[RestartData] = []
    restart_point: int = random_restart_point(results.n)
    invariant_runs: Set[int] = set()
    def parse_run(trial_num: int, sizes: List[int], intersection_sizes: List[int]):
        nonlocal restart_cache, invariant_runs
        restart_cache.append(RestartData(size=sizes[restart_point], intersection=intersection_sizes[restart_point], trial_number=trial_num))
        invariant_data: List[int] = [invariant(x) for x in sizes]
        maintains_invariant: bool = all([intersection_sizes[i] >= invariant_data[i] for i in range(len(sizes))])
        if maintains_invariant:
            invariant_runs.add(trial_num)
    results.for_each_trial_results(parse_run)
    
    def get_threshold_runs(threshold: int) -> Set[int]:
        good_runs: List[RestartData] = [x.trial_number for x in restart_cache if threshold_metric(x.size, x.intersection) >= threshold]
        return set(good_runs)

    plot.initialize_figure("Threshold", "# Runs", "# of runs satisfying invariant from those with metric above threshold and below", (40, 16))
    threshold_values: List[int] = threshold_range()
    threshold_runs_series: List[int] = []
    not_threshold_runs_series: List[int] = []
    threshold_runs_satisfing_invariant_series: List[int] = []
    not_threshold_runs_satisfying_invariant_series: List[int] = []

    trial_values_set: Set[int] = set(results.trial_values)
    for threshold in threshold_values:
        threshold_runs: List[int] = get_threshold_runs(threshold)
        not_threshold_runs: Set[int] = trial_values_set.difference(threshold_runs)
        threshold_runs_series.append(len(threshold_runs))
        not_threshold_runs_series.append(len(not_threshold_runs))
        threshold_runs_satisfing_invariant_series.append(len(threshold_runs.intersection(invariant_runs)))
        not_threshold_runs_satisfying_invariant_series.append(len(not_threshold_runs.intersection(invariant_runs)))
    
    note: str =  f"""
                    Threshold Range: {source_code(threshold_range)}\n
                    Threshold Metric: {source_code(threshold_metric)}\n
                    Invariant: {source_code(invariant)[0]}\n
                    Random restart point: {source_code(random_restart_point)[0]}\n
                """
                
    plot.add_notes(note, 0.05, 0.8)
    plot_series(threshold_values, threshold_runs_series, Formatting("green", 0.5, None, False, None, "Runs satisfying threshold", 1))
    plot_series(threshold_values, not_threshold_runs_series, Formatting("red", 0.5, None, False, None, "Runs not satisfying threshold", 1))
    plot_series(threshold_values, threshold_runs_series, Formatting("blue", 0.5, None, False, None, "Runs satisfying threshold and invariant", 1))
    plot_series(threshold_values, threshold_runs_series, Formatting("yellow", 0.5, None, False, None, "Runs not satisfying threshold, but satisfying invariant", 1))
    plot.draw_legend()
    plot.show_or_save(transient, f"{directory_name}/varying-threshold", "independent_set")


@click.command()
@click.option(
    "--today",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to set file name to load to today's file name.",
)
@click.option(
    "--file-name",
    required=False,
    help="The file name to save the graph as. Prompt will be provided if option not provided.",
)
@click.option(
    "--transient",
    required=False,
    is_flag=True,
    default=False,
    help="Shows the plot instead of saving.",
)
@click.option(
    "--directory-name",
    required=True,
    is_flag=False,
    help="The directory to store the plots in"
)
def plot_relative_sizes(today, file_name, transient, directory_name):
    validate(transient or (directory_name is not None), 
        f"The transient flag should be passed, or a valid directory name should be provided.")
    """
    Plots a graph of the sizes / intersections of successive augmentation algorithm, along with an optional
    graph for some function of the size. Can be useful to compare whether the intersection maintains this
    function on average (can be used for inductive w.h.p proof potentially?)
    """
    # ? Load results and generate file name if not set
    results: SuccAugResults = verify_and_load_results_v2(SuccAugResults, "independent_set", today)
    if not transient:
        directory_name = file_util.create_dir_in_experiment_results_directory(directory_name, "independent_set")

    #plot_overview(transient, directory_name, results)
    #plot_fixed_threshold(transient, directory_name, results)
    # Skip these for noew for testing.
    plot_varied_threshold(transient, directory_name, results)
