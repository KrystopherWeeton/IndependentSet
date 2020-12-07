from typing import List
import matplotlib.pyplot as plt  # Used for plotting results
import csv
import os
import networkx as nx
import random

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
            plt.savefig(f"results/{self.directory}/{self.file_name}.png")
        else:
            plt.savefig(f"results/{self.file_name}.png")


class CSVRow:
    def __init__(self, title: str, data: List):
        self.title = title
        self.data = data


def write_to_csv(rows: List[CSVRow], file_name: str, delim=','):
    results = [[row.title] + row.data for row in rows]
    results = zip(*results)
    with open(file_name + ".csv", 'w', newline='') as csvfile:
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
def create_dir(name: str) -> str:
    number = 0
    directory = name
    if os.path.isdir(directory):
        print(
            f"⚠️  The directory {name} already exists. Creating new directory...")

    while os.path.isdir(directory):
        number += 1
        directory = f"{name}({number})"
    os.mkdir(directory)
    return directory
