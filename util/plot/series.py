import matplotlib.pyplot as plt
from typing import Callable

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


def plot_function(
    x_points: [float],
    func: Callable,
    formatting: SeriesFormatting = DEFAULT_SERIES_FORMATTING
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