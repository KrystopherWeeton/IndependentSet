#!env/bin/python3
import click

from experiments.size import size


@click.group()
def run():
    pass

run.add_command(size)

if __name__ == "__main__":
    run()