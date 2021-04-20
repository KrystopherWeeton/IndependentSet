#!env/bin/python3
import click
import util.storage as storage


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
    # Print header if doing verbose output
    if verbose:
        print(
                "[V] Running size to see performance of GWW using different fixed set sizes with the following parameters.\n"
                f"[V] n={n}, min_k={min_k}, max_k={max_k}, step={step}, trials={trials}"
        )

    # Check all parameters passed in
    if n < 1:
        raise Exception("Experiment must be run with positive n.") 
    if min_k > n or max_k > n:
        raise Exception("Experiment must be run with min_k and max_k at most n")
    if trials < 1:
        raise Exception("Experiment must be run with a positive number of trials")

    # 

    return
