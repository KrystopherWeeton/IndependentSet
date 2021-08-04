#!env/bin/python3
import click

from graph_coloring.plot_commands.plot_basic_heuristic import plot_basic_heuristic
from graph_coloring.plot_commands.plot_basic_local_sesarch import plot_basic_local_search
from graph_coloring.plot_commands.plot_glauber_dynamics import plot_glauber_dynamics


@click.group()
def coloring():
    pass


coloring.add_command(plot_basic_heuristic)
coloring.add_command(plot_basic_local_search)
coloring.add_command(plot_glauber_dynamics)
if __name__ == "__main__":
    coloring()
