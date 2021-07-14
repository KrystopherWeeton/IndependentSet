#!env/bin/python3
import click

from experiments.heuristic import heuristic
from experiments.local_search import local_search
from experiments.size import size
from experiments.successive_augmentation import successive_augmentation
from experiments.phase_heuristic import phase_heuristic


@click.group()
def run():
    pass

run.add_command(size)
run.add_command(heuristic)
run.add_command(local_search)
run.add_command(successive_augmentation)
run.add_command(phase_heuristic)

if __name__ == "__main__":
    run()