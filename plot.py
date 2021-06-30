#!env/bin/python3
import click

from plot_commands.size_heatmap import plot_size_heatmap
from plot_commands.heuristic_graph import plot_heuristics_graphs
from plot_commands.sa_trace import plot_sa_trace
from plot_commands.sa_triangles import plot_sa_triangles

@click.group()
def run():
    pass

run.add_command(plot_size_heatmap)
run.add_command(plot_heuristics_graphs)
run.add_command(plot_sa_trace)
run.add_command(plot_sa_triangles)

if __name__ == "__main__":
    run()