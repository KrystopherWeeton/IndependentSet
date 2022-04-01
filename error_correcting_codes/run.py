import click

from error_correcting_codes.commands.correction_heatmap.run import (
    run_correction_heatmap_gallager, run_correction_heatmap_tanner)
from error_correcting_codes.commands.correction_series.run import \
    run_correction_series
from error_correcting_codes.commands.global_local.run import run_global_local
from error_correcting_codes.commands.search_space_map.run import \
    search_space_map
from error_correcting_codes.commands.threshold_map.run import threshold_map


@click.group()
def ecc():
    pass

ecc.add_command(run_correction_heatmap_tanner)
ecc.add_command(run_correction_heatmap_gallager)
ecc.add_command(run_global_local)
ecc.add_command(run_correction_series)
ecc.add_command(search_space_map)
ecc.add_command(threshold_map)

if __name__ == "__main__":
    ecc()
