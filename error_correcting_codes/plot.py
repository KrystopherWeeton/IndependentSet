import click

from error_correcting_codes.commands.correction_heatmap.plot import (
    plot_gallager_heatmap, plot_tanner_heatmap)
from error_correcting_codes.commands.correction_series.plot import \
    plot_correction_series
from error_correcting_codes.commands.count_solutions.plot import \
    count_solutions
from error_correcting_codes.commands.global_local.plot import plot_global_local
from error_correcting_codes.commands.search_space_map.plot import \
    search_space_map
from error_correcting_codes.commands.threshold_map.plot import threshold_map


@click.group()
def ecc():
    pass

ecc.add_command(plot_tanner_heatmap)
ecc.add_command(plot_gallager_heatmap)
ecc.add_command(plot_global_local)
ecc.add_command(plot_correction_series)
ecc.add_command(search_space_map)
ecc.add_command(threshold_map)
ecc.add_command(count_solutions)

if __name__ == "__main__":
    ecc()
