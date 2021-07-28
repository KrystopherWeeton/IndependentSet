from typing import Callable, Tuple

import matplotlib.pyplot as plt  # Used for plotting results
from dataclasses import dataclass
from util.config import get_experiment_results_directory


@dataclass
class Formatting:
    color: str = "red"
    alpha: float = None
    style: str = None
    include_markers: bool = False
    marker_type: str = None
    label: str = None
    width: int = 1


DEFAULT_FORMATTING: Formatting = Formatting(label=None, color="gray", alpha="1", width=1)

def LIGHT_GRAY(label: str) -> Formatting:
    return Formatting(label=label, color="gray", alpha=0.2, include_markers=True, marker_type="-o")

def LIGHT_RED(label: str) -> Formatting:
    return Formatting(label=label, color="red", alpha=0.2, include_markers=True, marker_type="-o")

def LIGHT_BLUE(label: str) -> Formatting:
    return Formatting(label=label, color="blue", alpha=0.2, include_markers=True, marker_type="-o")

def LIGHT_GREEN(label: str) -> Formatting:
    return Formatting(label=label, color="green", alpha=0.2, include_markers=True, marker_type="-o")


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
    plt.tight_layout()
    plt.autoscale(enable=True)
    plt.show()
    plt.clf()

"""
    Saves the plot to a file.
"""
def save_plot(file_name: str, project_name: str, folder: str = None):
    directory = get_experiment_results_directory(project_name)
    path = f"{directory}/{file_name}.png"
    if folder is not None:
        path = f"{directory}/{folder}/{file_name}.png"
    plt.savefig(path)
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