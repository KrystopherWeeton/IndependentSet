import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from util.plot.series import SeriesFormatting, plot_series
import util.plot.plot as plot

def plot_scatter_data(
    x_points: [float],
    y_points: [[float]],
    title: str,
    x_title: str,
    y_title: str,
    other_y_series: [[float]] = [],
    other_y_formatting: [SeriesFormatting] = [],
    x_spacing: float = 0,
    y_spacing: float = 0
):
    """
        Plots the provided scatter data
    """
    #? Initialize Figure
    plot.initialize_figure(
        x_label=x_title, y_label=y_title, title=title, figsize=(10, 8)
    )
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
    plot.annotate_points(
        x_points = x_values,
        y_points = y_values,
        k = 1,
        annotator = lambda x, y: y,
        x_offset=x_spacing,
        y_offset=y_spacing
    )