#!env/bin/python3
import click

from independent_set.exp import ind_set
from graph_coloring.exp import coloring

@click.group()
def run():
    pass

run.add_command(ind_set)
run.add_command(coloring)

if __name__ == "__main__":
    run()