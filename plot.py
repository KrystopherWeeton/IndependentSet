#!env/bin/python3
import click

from independent_set.plot import ind_set

@click.group()
def run():
    pass

run.add_command(ind_set)

if __name__ == "__main__":
    run()