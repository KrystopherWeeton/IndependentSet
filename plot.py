#!env/bin/python3
import click

from plot_commands.size_heatmap import plot_size_heatmap
from plot_commands.heuristic_graph import plot_heuristics_graphs

@click.group()
def run():
    pass

run.add_command(plot_size_heatmap)
run.add_command(plot_heuristics_graphs)

if __name__ == "__main__":
    run()