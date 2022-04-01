from typing import List

import click

import util.file_util as file_util
import util.plot.heatmap as heatmap
import util.plot.plot as plot
import util.plot.series as series
from error_correcting_codes.models.results.global_local_results import \
    GlobalLocalResults
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
def plot_global_local(today, dir_name, transient):
    if not transient:
        dir_name = file_util.create_dir_in_experiment_results_directory(dir_name, "error_correcting_codes")
    results: GlobalLocalResults = verify_and_load_results_v2(GlobalLocalResults, "error_correcting_codes", today)
    for t in range(results.num_trials):
        steps: List[int] = results.get_steps(t)
        local: List[int] = results.get_local_series(t)
        glob: List[int] = results.get_global_series(t)
        max_local: int = results.j * results.n // results.k
        max_global: int = results.n


        """
        plot.initialize_figure("Step", "Progress", f"Global (hamming dist) vs. Local (parities satisfied) for p={results.p}, n={results.n}")
        series.plot_series(steps, local, plot.Formatting(color="orange", alpha=0.75, label=f"Local Progress (out of {max_global})"))
        series.plot_series(steps, glob, plot.Formatting(color="blue", alpha=0.75, label=f"Global Progress (out of {max_local})"))
        plot.draw_legend()
        plot.show_or_save(transient, f"{dir_name}/run({t})", "error_correcting_codes")
        """

        plot.initialize_figure("Step", "", f"Global (hamming dist) vs. Local (num unsatisfied parities) (Normalized)")
        series.plot_series(
            steps,
            [(max_local - x) / max_local for x in local],
            plot.Formatting(color="orange", alpha=0.75, label="Unsatisfied Parities"),
        )
        series.plot_series(
            steps,
            [x / max_global for x in glob],
            plot.Formatting(color="blue", alpha=0.75, label="Hamming Distance to Transmitted Message"),
        )
        plot.draw_legend()
        plot.show_or_save(transient, f"{dir_name}/normalized-run({t})", "error_correcting_codes")

        plot.initialize_figure("Step", "Hamming Distance", "Hamming Distance to Transmitted Message")
        series.plot_series(steps, glob, plot.Formatting(color="blue", alpha=0.75, label=f"Global Progress (out of {max_local})"))
        plot.show_or_save(transient, f"{dir_name}/global-progress({t})", "error_correcting_codes")
