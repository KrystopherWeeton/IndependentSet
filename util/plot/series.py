from typing import Callable, List

import matplotlib.pyplot as plt

from util.plot.plot import DEFAULT_FORMATTING, Formatting, annotate_all_points


def plot_series(
    x_points: List[float],
    y_points: List[float],
    formatting: Formatting = DEFAULT_FORMATTING,
    annotate_points: bool = False
):
    if formatting.include_markers:
        plt.plot(x_points, y_points, 
            formatting.marker_type, 
            label=formatting.label, 
            color=formatting.color,
            linestyle=formatting.style,
            alpha=formatting.alpha,
        )
    else:
        plt.plot(x_points, y_points, 
            label=formatting.label, 
            color=formatting.color,
            alpha=formatting.alpha,
            linestyle=formatting.style,
            linewidth=formatting.width,
        )
    if annotate_points:
        annotate_all_points(
            x_points=x_points, 
            y_points=y_points,
            annotations=[f"{y:.1f}" for y in y_points],
            x_offset=20,
            y_offset=0
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
