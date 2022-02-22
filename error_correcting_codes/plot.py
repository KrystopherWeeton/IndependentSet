import click

from error_correcting_codes.commands.correction_heatmap.plot import \
    plot_correction_heatmap


@click.group()
def ecc():
    pass

ecc.add_command(plot_correction_heatmap)

if __name__ == "__main__":
    ecc()
