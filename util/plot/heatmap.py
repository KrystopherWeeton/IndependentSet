from typing import List
import matplotlib.pyplot as plt  # Used for plotting results
import csv
import os
import networkx as nx
import random
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.cm as cmap        # Used for heatmaps
from matplotlib.axes import Axes    # Used for advanced plotting things (heatmaps)
from mpl_toolkits.axes_grid1 import make_axes_locatable
from enum import Enum
from util.models.stat_info import StatInfo

import networkx.drawing as nx_draw
from networkx.drawing.nx_agraph import write_dot



class HeatMapColor(Enum):
    REDS=cmap.Reds
    YELLOW_GREEN=cmap.YlGn


"""
Draws a heatmap of results.
    x: x axis keys
    y: y axis keys
    z: the matrix of values to draw
"""
def graph_heatmap(
    x: [int], 
    y: [int], 
    z: [int], 
    directory: str,
    file_name: str, 
    min: int = None, 
    max: int = None, 
    title: str = "Title", 
    x_axis_title: str = "x_axis", 
    y_axis_title: str = "y_axis",
    color: HeatMapColor = HeatMapColor.REDS,
    include_annotation: bool = True,
    plot_size: float = 10.0
):
    # Generate plot and set ticks
    plt.imshow(z, color.value, vmin=min, vmax=max)
    ax: Axes = plt.gca()
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)

    # Set annotation of the heatmap
    if include_annotation:
        for i in range(len(x)):
            for j in range(len(y)):
                ax.text(i, j, str(z[j][i]), ha="center", va="center", color="black")
    else:
        pass
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        # divider = make_axes_locatable(ax)
        # cax = divider.append_axes("right", size="5%", pad=0.05)

        # plt.colorbar(cax=cax)
        # plt.colorbar()

    # Set title of the heatmap and axes
    plt.title(title)
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)

    # Do not include colorbar right now
    # plt.colorbar()

    # Save the plot to a figure
    fig = plt.gcf()
    fig.set_size_inches(plot_size, plot_size)
    plt.xticks(rotation=90)
    plt.savefig(f"{directory}/{file_name}.png")
    plt.clf()