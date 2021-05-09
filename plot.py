#!env/bin/python3
import click

from plot_commands.size_heatmap import plot_size_heatmap

@click.group()
def run():
    pass

run.add_command(plot_size_heatmap)

if __name__ == "__main__":
    run()