from typing import List

import click

import util.plot.heatmap as heatmap
import util.plot.plot as plot
from error_correcting_codes.models.results.correction_heatmap_results import \
    CorrectionHeatmapResults
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
def plot_correction_heatmap(today, file_name, transient):
    results: CorrectionHeatmapResults = verify_and_load_results_v2(CorrectionHeatmapResults, "error_correcting_codes", today)

    matrix = results.get_heatmap_data()
    d_values: List[int] = results.d_values
    p_values: List[float] = results.p_values
    heatmap.graph_heatmap([f"{x:.2f}" for x in p_values], d_values, matrix, include_annotation=False)

    if transient:
        plot.show_plot()
    else:
        file_name = prompt_file_name(file_name)
        plot.save_plot(file_name, "independent_set")
