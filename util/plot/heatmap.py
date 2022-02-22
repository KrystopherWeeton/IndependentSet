import csv
import os
import random
from enum import Enum
from typing import List

import matplotlib.cm as cmap  # Used for heatmaps
import matplotlib.pyplot as plt  # Used for plotting results
import networkx as nx
import networkx.drawing as nx_draw
import numpy as np
from matplotlib.axes import \
    Axes  # Used for advanced plotting things (heatmaps)
from mpl_toolkits import mplot3d
from mpl_toolkits.axes_grid1 import make_axes_locatable
from networkx.drawing.nx_agraph import write_dot

from util.models.stat_info import StatInfo


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
    x: List[int], 
    y: List[int], 
    z: List[List[int]], 
    min: int = None, 
    max: int = None, 
    color: HeatMapColor = HeatMapColor.REDS,
    include_annotation: bool = True,
    include_tick_labels: bool = True,
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

    if not include_tick_labels:
        ax.set_yticklabels([])
        ax.set_xticklabels([])

    # Do not include colorbar right now
    # plt.colorbar()

    # Save the plot to a figure
    plt.xticks(rotation=90)
