#!env/bin/python3
import click

from experiments.size import size
from experiments.heuristic import heuristic
from experiments.local_search import local_search
from experiments.successive_augmentation import successive_augmentation

@click.group()
def run():
    pass

run.add_command(size)
run.add_command(heuristic)
run.add_command(local_search)
run.add_command(successive_augmentation)

if __name__ == "__main__":
    run()