import click

from error_correcting_codes.commands.correction_heatmap.run import (
    run_correction_heatmap_gallager, run_correction_heatmap_tanner)


@click.group()
def ecc():
    pass

ecc.add_command(run_correction_heatmap_tanner)
ecc.add_command(run_correction_heatmap_gallager)

if __name__ == "__main__":
    ecc()
