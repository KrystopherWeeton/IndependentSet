import click

from error_correcting_codes.commands.correction_heatmap.plot import (
    plot_gallager_heatmap, plot_tanner_heatmap)


@click.group()
def ecc():
    pass

ecc.add_command(plot_tanner_heatmap)
ecc.add_command(plot_gallager_heatmap)

if __name__ == "__main__":
    ecc()
