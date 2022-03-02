import click

from error_correcting_codes.commands.correction_heatmap.run import (
    run_correction_heatmap_gallager, run_correction_heatmap_tanner)
from error_correcting_codes.commands.correction_series.run import \
    run_correction_series
from error_correcting_codes.commands.global_local.run import run_global_local


@click.group()
def ecc():
    pass

ecc.add_command(run_correction_heatmap_tanner)
ecc.add_command(run_correction_heatmap_gallager)
ecc.add_command(run_global_local)
ecc.add_command(run_correction_series)

if __name__ == "__main__":
    ecc()
