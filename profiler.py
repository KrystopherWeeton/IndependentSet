#!env/bin/python3
import click

from experiments.successive_augmentation import profile_successive_augmentation


@click.group()
def run():
    pass

run.add_command(profile_successive_augmentation)

if __name__ == "__main__":
    run()