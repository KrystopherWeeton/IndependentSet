#!env/bin/python3
import click


##########################################
#       Configuration
##########################################


##########################################
#       Commands / Experiments
##########################################


@click.command()
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("--min-n", required=False, multiple=False, type=int)
@click.option("--max-n", required=False, multiple=False, type=int)
@click.option("--step", required=False, multiple=False, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
@click.option("--delta", required=False, multiple=False, type=int, default=2)
@click.option("max_iterations", required=False, multiple=False, type=int, default=100000)
def glauber_dynamics(verbose, min_n, max_n, step, num_trials):
