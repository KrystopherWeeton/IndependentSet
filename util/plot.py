from typing import List
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


def draw_hist(values, file_name: str):
    plt.close()
    plt.hist(values)
    plt.savefig(file_name + ".png")


# Creates a directory if it doesn't already exists
def create_dir(name: str, agressive: bool = False) -> str:
    number = 0
    directory = f"results/{name}"
    if not agressive:
        if os.path.isdir(directory):
            print(
                f"⚠️  The directory {name} already exists. Creating new directory...")

        while os.path.isdir(directory):
            number += 1
            directory = f"results/{name}({number})"

    if not os.path.isdir(directory):
        os.mkdir(directory)
    return directory


class SeriesFormatting:
    def __init__(self, 
        label: str, 
        color: str, 
        alpha: float, 
        include_markers: bool, 
        marker_type: str
    ):
        self.label = label
        self.color = color
        self.alpha = alpha
        self.include_markers = include_markers
        self.marker_type = marker_type


DEFAULT_SERIES_FORMATTING: SeriesFormatting = SeriesFormatting("", "red", 1, False, "")


def LIGHT_GRAY(label: str) -> SeriesFormatting:
    return SeriesFormatting(label, "gray", 0.2, True, "-o")

def LIGHT_RED(label: str) -> SeriesFormatting:
    return SeriesFormatting(label, "red", 0.2, True, "-o")

def LIGHT_BLUE(label: str) -> SeriesFormatting:
    return SeriesFormatting(label, "blue", 0.2, True, "-o")

def LIGHT_GREEN(label: str) -> SeriesFormatting:
    return SeriesFormatting(label, "green", 0.2, True, "-o")


def plot_series(
    x_points: [float],
    y_points: [float],
    formatting: SeriesFormatting = DEFAULT_SERIES_FORMATTING
):
    if formatting.include_markers:
        plt.plot(x_points, y_points, 
            formatting.marker_type, 
            label=formatting.label, 
            color=formatting.color,
            alpha=formatting.alpha
        )
    else:
        plt.plot(x_points, y_points, 
            label=formatting.label, 
            color=formatting.color,
            alpha=formatting.alpha
        )


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