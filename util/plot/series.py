from typing import Callable, List

import matplotlib.pyplot as plt

from util.plot.plot import DEFAULT_FORMATTING, Formatting


def plot_series(
    x_points: List[float],
    y_points: List[float],
    formatting: Formatting = DEFAULT_FORMATTING
):
    if formatting.include_markers:
        plt.plot(x_points, y_points, 
            formatting.marker_type, 
            label=formatting.label, 
            color=formatting.color,
            linestyle=formatting.style,
            alpha=formatting.alpha
        )
    else:
        plt.plot(x_points, y_points, 
            label=formatting.label, 
            color=formatting.color,
            alpha=formatting.alpha,
            linestyle=formatting.style,
            linewidth=formatting.width
        )


def plot_function(
    x_points: [float],
    func: Callable,
    formatting: Formatting = DEFAULT_FORMATTING
):
    """
        Plots the provided function
            x_points: The x values to evaluate at
            func: A function f(x) to plot
            formatting: Formatting for the series
    """
    plot_series(
        x_points,
        [func(x) for x in x_points],
        formatting
    )
