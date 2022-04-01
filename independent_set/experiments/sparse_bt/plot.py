from typing import List

import click

import util.file_util as file_util
import util.plot.plot as plot
import util.plot.series as series
from error_correcting_codes.commands.correction_series.results import \
    CorrectionSeriesResults
from util.commands import verify_and_load_results_v2


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
def plot_correction_series(today, dir_name, transient):
    if not transient:
        dir_name = file_util.create_dir_in_experiment_results_directory(dir_name, "error_correcting_codes")
    results: CorrectionSeriesResults = verify_and_load_results_v2(CorrectionSeriesResults, "error_correcting_codes", today)
    
    plot.show_or_save(transient, f"{dir_name}/normalized", "error_correcting_codes")
