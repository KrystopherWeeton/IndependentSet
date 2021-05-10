#!env/bin/python3
import click

from experiments.size import size
from experiments.heuristic import heuristic

@click.group()
def run():
    pass

run.add_command(size)
run.add_command(heuristic)

if __name__ == "__main__":
    run()