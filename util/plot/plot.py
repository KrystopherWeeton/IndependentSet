import os
import random
from enum import Enum
from typing import Callable, List, Tuple

import matplotlib.cm as cmap  # Used for heatmaps
import matplotlib.pyplot as plt  # Used for plotting results
import numpy as np
from matplotlib.axes import \
    Axes  # Used for advanced plotting things (heatmaps)
from mpl_toolkits import mplot3d
from mpl_toolkits.axes_grid1 import make_axes_locatable

from util.models.stat_info import StatInfo
from util.plot.series import SeriesFormatting, plot_series


def draw_hist(values, file_name: str):
    plt.close()
    plt.hist(values)
    plt.savefig(file_name + ".png")

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


# Annotates points provided on the active plot
def annotate_all_points(
    x_points: [float],      # x points
    y_points: [float],      # y points
    annotations: [str],     # Annotations for each point
    x_offset: int,          # x offset for annotations
    y_offset: int,          # y offset for annotations
):
    for i, label in enumerate(annotations):
        plt.annotate(
            label, 
            (x_points[i], y_points[i]), 
            xytext=(x_offset, y_offset), 
            textcoords="offset pixels"
        )


# Uses a function to generate annotations for each point provided
def annotate_points(
    x_points: [float],
    y_points: [float],
    k: int,                 # Will annotate the k'th element 
    annotator: Callable,    # Annotation generation function (x, y) -> str
    x_offset: int,          # x offset for annotations
    y_offset: int,          # y offset for annotations
):
    #? Validate arguments
    if len(x_points) != len(y_points):
        raise Exception(f"Cannot annotate labels with unequal lengths. |x|={len(x_points)}, |y|={len(y_points)}")
    #? Generate annotations and pass through to helper function
    annotations: [str] = []
    for i in range(len(x_points)):
        if i % k == 0:
            annotations.append(annotator(x_points[i], y_points[i]))
        else:
            annotations.append("")
    annotate_all_points(
        x_points, y_points, annotations, x_offset, y_offset
    )


# Used to add 'notes' to a graph in the top right corner
def add_notes(
    notes: str,
    x: int,
    y: int,
):
    ax = plt.gca()
    plt.text(
        x, 
        y, 
        notes, 
        horizontalalignment="left",
        verticalalignment="center",
        transform=ax.transAxes
    )