#!env/bin/python3
import click

from independent_set.plot_commands.heuristic_graph import plot_heuristics_graphs
from independent_set.plot_commands.sa_trace import plot_sa_trace
from independent_set.plot_commands.sa_triangles import plot_sa_triangles
from independent_set.plot_commands.size_heatmap import plot_size_heatmap
from independent_set.plot_commands.sa_concentration import plot_sa_concentration


@click.group()
def ind_set():
    pass

ind_set.add_command(plot_size_heatmap)
ind_set.add_command(plot_heuristics_graphs)
ind_set.add_command(plot_sa_trace)
ind_set.add_command(plot_sa_triangles)
ind_set.add_command(plot_sa_concentration)

if __name__ == "__main__":
    run()