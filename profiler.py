#!env/bin/python3
import click

from experiments.successive_augmentation import profile_successive_augmentation
from experiments.phase_heuristic import profile_phase_heuristic


@click.group()
def run():
    pass

run.add_command(profile_successive_augmentation)
run.add_command(profile_phase_heuristic)

if __name__ == "__main__":
    run()