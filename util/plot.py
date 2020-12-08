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

import networkx.drawing as nx_draw
from networkx.drawing.nx_agraph import write_dot

_num_plots: int = 0


class Series:
    def __init__(self, **kwargs):
        self.x_values: List = []
        self.y_values: List = []
        self.color: str = ""
        self.name: str = ""

        for k, v in kwargs.items():
            setattr(self, k, v)


class PlotArgs:
    def __init__(self, **kwargs):
        self.x_title: str = ""
        self.y_title: str = ""
        self.title: str = ""
        self.series: [Series] = []
        self.file_name: str = ""
        self.directory: str = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_series(self, x_values: List, y_values: List, name: str, color: str = "b"):
        series: Series = Series(
            x_values=x_values, y_values=y_values, name=name, color=color)
        self.series.append(series)

    def plot(self):
        global _num_plots
        _num_plots += 1
        fig = plt.figure(_num_plots)
        plt.title(self.title)
        plt.xlabel(self.x_title)
        plt.ylabel(self.y_title)

        for series in self.series:
            plt.plot(series.x_values, series.y_values,
                     series.color, label=series.name, marker="o")

        if len(self.series) > 1:
            plt.legend()

        if self.directory:
            print(self.directory, self.file_name)
            plt.savefig(f"{self.directory}/{self.file_name}.png")
            plt.clf()
        else:
            plt.savefig(f"{self.file_name}.png")
            plt.clf()

"""
Draws a heatmap of results.
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
    y_axis_title: str = "y_axis"
):
    # Generate plot and set ticks
    plt.imshow(z, cmap=cmap.YlGn, vmin=min, vmax=max)
    ax: Axes = plt.gca()
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)

    # Set annotation of the heatmap
    for i in range(len(x)):
        for j in range(len(y)):
            ax.text(i, j, str(z[j][i]), ha="center", va="center", color="black")

    # Set title of the heatmap and axes
    plt.title(title)
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)

    # Do not include colorbar right now
    # plt.colorbar()

    # Save the plot to a figure
    print(directory)
    plt.savefig(f"{directory}/{file_name}.png")
    plt.clf()




class CSVRow:
    def __init__(self, title: str, data: List):
        self.title = title
        self.data = data


def write_to_csv(rows: List[CSVRow], file_name: str, directory: str = "", delim=','):
    results = [[row.title] + row.data for row in rows]
    results = zip(*results)
    with open(f"{directory}/{file_name}" + ".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delim,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in results:
            writer.writerow(row)

def draw_hist(values, file_name: str):
    plt.close()
    plt.hist(values)
    plt.savefig(file_name + ".png")

def draw_graph(g: nx.Graph, file_name: str, with_labels: bool = False):
    random.seed(1)
    pos = nx.circular_layout(g)
    pos = nx.spring_layout(g, dim=2, pos=pos, iterations = 10000) # positions for all nodes
    labels = nx.get_node_attributes(g, 'hexes') 
    nx_draw.draw(g, labels=labels, pos=pos, with_labels = with_labels, node_size=100)
    # TODO: Add a bunch of fucntionality here for drawing houses, etc.
    plt.savefig(file_name + ".png")


def store_graph(g: nx.Graph, file_name: str, with_labels: bool = False):
    write_dot(g, file_name)


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
