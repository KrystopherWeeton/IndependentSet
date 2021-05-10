#!env/bin/python3
import click

from experiments.size import size
from experiments.heuristic import heuristic
from experiments.local_search import local_search

@click.group()
def run():
    pass

run.add_command(size)
run.add_command(heuristic)
run.add_command(local_search)

if __name__ == "__main__":
    run()