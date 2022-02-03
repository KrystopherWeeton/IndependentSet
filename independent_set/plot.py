#!env/bin/python3
import click

from independent_set.plot_commands.convergence_plot import convergence_plot
from independent_set.plot_commands.heuristic_graph import \
    plot_heuristics_graphs
from independent_set.plot_commands.sa_concentration import \
    plot_sa_concentration
from independent_set.plot_commands.sa_dist import sa_dist
from independent_set.plot_commands.sa_relative_sizes import plot_relative_sizes
from independent_set.plot_commands.sa_trace import plot_sa_trace
from independent_set.plot_commands.sa_triangles import plot_sa_triangles
from independent_set.plot_commands.size_heatmap import plot_size_heatmap


@click.group()
def ind_set():
    pass

ind_set.add_command(plot_size_heatmap)
ind_set.add_command(plot_heuristics_graphs)
ind_set.add_command(plot_sa_trace)
ind_set.add_command(plot_sa_triangles)
ind_set.add_command(plot_sa_concentration)
ind_set.add_command(sa_dist)
ind_set.add_command(plot_relative_sizes)
ind_set.add_command(convergence_plot)

if __name__ == "__main__":
    ind_set()
