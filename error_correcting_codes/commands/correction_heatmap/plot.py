from typing import List

import click

import util.plot.heatmap as heatmap
import util.plot.plot as plot
from error_correcting_codes.models.results.correction_heatmap_results import (
    GallagerHeatmapResults, TannerHeatmapResults)
from util.commands import prompt_file_name, verify_and_load_results_v2


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
def plot_tanner_heatmap(today, file_name, transient):
    results: TannerHeatmapResults = verify_and_load_results_v2(TannerHeatmapResults, "error_correcting_codes", today)
    heatmap.graph_heatmap([f"{x:.2f}" for x in results.p_values], results.d_values, results.get_matrix_data(), include_annotation=False)
    # TODO: Add axis and graph titles
    plot.show_or_save(transient, prompt_file_name(file_name), "error_correcting_codes")

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
def plot_gallager_heatmap(today, file_name, transient):
    results: GallagerHeatmapResults = verify_and_load_results_v2(GallagerHeatmapResults, "error_correcting_codes", today)
    heatmap.graph_heatmap([f"{x:.2f}" for x in results.p_values], results.j_values, results.get_matrix_data(), include_annotation=True)
    # TODO: Add axis and graph titles
    plot.show_or_save(transient, prompt_file_name(file_name), "error_correcting_codes")
