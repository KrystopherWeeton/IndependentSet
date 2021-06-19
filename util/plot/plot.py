from typing import List, Tuple
import matplotlib.pyplot as plt  # Used for plotting results
import os
import random
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.cm as cmap        # Used for heatmaps
from matplotlib.axes import Axes    # Used for advanced plotting things (heatmaps)
from mpl_toolkits.axes_grid1 import make_axes_locatable
from enum import Enum
from util.models.stat_info import StatInfo
from util.plot.series import plot_series, SeriesFormatting

def draw_hist(values, file_name: str):
    plt.close()
    plt.hist(values)
    plt.savefig(file_name + ".png")


def plot_scatter_data(
    x_points: [float],
    y_points: [[float]],
    title: str,
    x_title: str,
    y_title: str,
    file_name: str,
    other_y_series: [[float]] = [],
    other_y_formatting: [SeriesFormatting] = [],
    directory: str = None,
    x_spacing: float = 0,
    y_spacing: float = 0
):
    #? Clear and set titles and things
    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)

    #? Flatten out the data points
    x_values: [float] = []
    y_values: [float] = []
    for i, x in enumerate(x_points):
        # Get a list of the y points corresponding to the x point
        ys: [float] = y_points[i]
        for y in ys:
            x_values.append(x)
            y_values.append(y)

    #? Plot the scatter values along with other lines 
    plt.scatter(x_values, y_values, marker="o")
    for series, formatting in zip(other_y_series, other_y_formatting):
        plot_series(x_points, series, formatting)
    plt.legend()

    #? Annotate the scatter points
    ax = plt.gca()
    for x, y in zip(x_values, y_values):
        ax.annotate(
            y,
            (x + x_spacing, y + y_spacing)
        )

    #? Save the figures
    if directory:
        # print(self.directory, self.file_name)
        plt.savefig(f"{directory}/{file_name}.png")
        plt.clf()
    else:
        plt.savefig(f"{file_name}.png")
        plt.clf() 

"""
    Initializes the figure to the provided specifications
"""
def initialize_figure(x_label: str, y_label: str, title: str, figsize: Tuple = None):
    if figsize is not None:
        plt.figure(figsize=figsize)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


"""
    Shows the plot to the user and then clears it. Can be used for testing / short term results.
"""
def show_plot():
    plt.show()
    plt.clf()

"""
    Saves the plot to a file.
"""
def save_plot(file_name: str, directory: str = None):
    if directory:
        plt.savefig(f"{directory}/{file_name}.png")
        plt.clf()
    else:
        plt.savefig(f"{file_name}.png")
        plt.clf() 