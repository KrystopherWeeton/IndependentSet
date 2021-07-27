#!env/bin/python3
import click


from graph_coloring.experiments.basic_heuristic import basic_heuristic

@click.group()
def coloring():
    pass


coloring.add_command(basic_heuristic)

if __name__ == "__main__":
    coloring()