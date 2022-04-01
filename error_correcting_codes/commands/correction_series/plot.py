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
    plot.initialize_figure("Bit Flip Probability", f"Parities Satisfied (out of {(results.n * results.j) // results.k})", f"Average Parities Satisfied by Final Solution (n={results.n})")
    series.plot_series(
        results.p_values, 
        results.get_parity_series(), 
        plot.Formatting(color="orange", include_markers=True, marker_type="x"), 
        annotate_points=True
    )
    plot.show_or_save(transient, f"{dir_name}/parities", "error_correcting_codes")


    plot.initialize_figure("Bit Flip Probability", f"Hamming Dist.", f"Average Hamming Dist of Sol. to Original (n={results.n})")
    series.plot_series(
        results.p_values, 
        results.get_hamming_series(), 
        plot.Formatting(color="blue", include_markers=True, marker_type="x"),
        annotate_points=True
    )
    plot.show_or_save(transient, f"{dir_name}/hamming", "error_correcting_codes")

    plot.initialize_figure("Bit Flip Probability", f"Normalized 'Score' of Final Solution", f"Average Global vs. Local score of Final Solution (n={results.n})")
    series.plot_series(
        results.p_values, 
        [x / results.n for x in results.get_hamming_series()], 
        plot.Formatting(color="blue", include_markers=True, label="Hamming Dist. to Original Message", marker_type="x"),
        annotate_points=False
    )
    num_parities: int = results.n * results.j / results.k
    series.plot_series(
        results.p_values, 
        [(num_parities - x) / num_parities for x in results.get_parity_series()], 
        plot.Formatting(color="orange", include_markers=True, label="Number of Unsatisfied Parities of Final Sol.", marker_type="x")
    )
    plot.draw_legend()
    plot.show_or_save(transient, f"{dir_name}/normalized", "error_correcting_codes")
