#!env/bin/python3
import click

from independent_set.plot import ind_set
from graph_coloring.plot import coloring

@click.group()
def run():
    pass

run.add_command(ind_set)
run.add_command(coloring)

if __name__ == "__main__":
    run()