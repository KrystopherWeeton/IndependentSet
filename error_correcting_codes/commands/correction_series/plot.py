from typing import List

import click

import util.file_util as file_util
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
def plot_tanner_heatmap(today, dir_name, transient):
    if not transient:
        file_util.create_dir_in_experiment_results_directory(dir_name, "error_correcting_codes")

    results: TannerHeatmapResults = verify_and_load_results_v2(TannerHeatmapResults, "error_correcting_codes", today)
    plot.initialize_figure("Bit Flip Probability", "Edge Count in Tanner Graph", f"Average Parities Satisfied (total_parities={results.n // 2}")
    heatmap.graph_heatmap([f"{x:.2f}" for x in results.p_values], results.d_values, results.get_parity_matrix(), include_annotation=True)
    plot.show_or_save(transient, f"{dir_name}/parities", "error_correcting_codes")

    plot.initialize_figure("Bit Flip Probability", "Edge Count in Tanner Graph", f"Average Hamming Distance of Solution (n={results.n})")
    heatmap.graph_heatmap([f"{x:.2f}" for x in results.p_values], results.d_values, results.get_hamming_matrix(), include_annotation=True)
    plot.show_or_save(transient, f"{dir_name}/hamming", "error_correcting_codes")

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
def plot_gallager_heatmap(today, dir_name, transient):
    if not transient:
        file_util.create_dir_in_experiment_results_directory(dir_name, "error_correcting_codes")
    results: GallagerHeatmapResults = verify_and_load_results_v2(GallagerHeatmapResults, "error_correcting_codes", today)
    plot.initialize_figure("Bit Flip Probability", "J value in gallager construction", f"Average Parities Satisfied (total_parities={results.n // 2}")
    heatmap.graph_heatmap([f"{x:.2f}" for x in results.p_values], results.j_values, results.get_parity_matrix(), include_annotation=True)
    plot.show_or_save(transient, f"{dir_name}/parities", "error_correcting_codes")

    plot.initialize_figure("Bit Flip Probability", "J value in gallager construction", f"Average Hamming Distance of Solution (n={results.n})")
    heatmap.graph_heatmap([f"{x:.2f}" for x in results.p_values], results.j_values, results.get_hamming_matrix(), include_annotation=True)
    plot.show_or_save(transient, f"{dir_name}/hamming", "error_correcting_codes")
