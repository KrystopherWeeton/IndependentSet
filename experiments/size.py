#!env/bin/python3
import click


"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
@click.option("--verbose",  required=False, is_flag=True,   help="Prints extra output to help track execution.")
@click.option("-n",         required=True,  type=int,       help="The number of vertices to have on the graph the experiment is run on.")
@click.option("--min-k",    required=True,  type=int,       help="The min. size of subset to run GWW with.")
@click.option("--max-k",    required=True,  type=int,       help="The max. size of subset to run GWW with.")
@click.option("--step",     required=True,  type=int,       help="The step size for k in the experiment.")
@click.option("--trials",   required=True,  type=int,       help="The number of trials to run for each k.")
def size(verbose, n, min_k, max_k, step, trials):
    return
