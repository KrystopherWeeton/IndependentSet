#!env/bin/python3
import click

from error_correcting_codes.run import ecc
from graph_coloring.exp import coloring
from independent_set.exp import ind_set


@click.group()
def run():
    pass

run.add_command(ind_set)
run.add_command(coloring)
run.add_command(ecc)

if __name__ == "__main__":
    run()
