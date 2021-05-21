import click
from util.storage import load
from util.results.size_results import SizeResults, generate_size_results_file_name
import util.plot.heatmap as heatmap
import os
import sys

@click.command()
def plot_sa_trace():
    pass