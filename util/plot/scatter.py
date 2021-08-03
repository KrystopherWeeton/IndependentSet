from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.colors import hsv_to_rgb

import util.plot.plot as plot
from util.plot.series import plot_series


def plot_scatter_data(
        x_points: List[float],
        y_points: List[List[float]],
        other_y_series: List[List[float]] = [],
        other_y_formatting: List[plot.Formatting] = [],
        x_spacing: float = 0,
        y_spacing: float = 0
):
    """
        Plots the provided scatter data
    """
    # ? Initialize Figure
    # ? Flatten out the data points
    x_values: List[float] = []
    y_values: List[float] = []
    for i, x in enumerate(x_points):
        # Get a list of the y points corresponding to the x point
        ys: List[float] = y_points[i]
        for y in ys:
            x_values.append(x)
            y_values.append(y)

    # ? Plot the scatter values along with other lines
    plt.scatter(x_values, y_values, marker="o")
    for series, formatting in zip(other_y_series, other_y_formatting):
        plot_series(x_points, series, formatting)
    plt.legend()



# Add support for graphing multiple trials with SAME x values
def plot_scatter_data_from_tuple_with_trial_labels(
        data: List[List[List[Tuple[int, int]]]],
        data_legend: List[str],
        annotator: Callable = None,
        x_offset: float = 10,
        y_offset: float = 10
):
    """

    :param data: data[Group][Trial #][Coordinate Pair #](x coord, y coord)
    :param data_legend: The labels for each group
    :param annotator:
    :param x_offset:
    :param y_offset:
    """
    # Make sure that we have a legend for each data group
    if len(data_legend) != len(data):
        raise AttributeError(
            f"The number of data groups: {len(data)}, and the number of data labels: {len(data_legend)} don't match!")
    # 1000 distinct colors:
    colors = [hsv_to_rgb([(i * 0.618033988749895) % 1.0, 1, 1])
              for i in range(1000)]
    plt.rc('axes', prop_cycle=(cycler('color', colors)))

    for i, trial in enumerate(data):
        x_values: [int] = []
        y_values: [int] = []
        for trial_num, points in enumerate(trial):
            """
            """
            x_values += [t[0] for t in points]
            y_values += [t[1] for t in points]

        plt.scatter(x_values, y_values, marker="o", color=f"C{i % 10}", label=f"{data_legend[i]}")
#            plt.scatter(x_values, y_values, marker="o", label=f"{data_legend[i]}, Trial {trial_num}")
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', ncol=2,
                   borderaxespad=0, frameon=False)

        if annotator is not None:
            plot.annotate_points(
                x_points=x_values,
                y_points=y_values,
                k=1,
                annotator=annotator,
                x_offset=x_offset,
                y_offset=y_offset,
            )
