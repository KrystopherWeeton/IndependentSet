from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

point = Tuple[int, int]


class LineFormatting:
    def __init__(self, style: str, width: int, color: str):
        self.style = style
        self.width = width
        self.color = color


DEFAULT_LINE_FORMATTING: LineFormatting = LineFormatting(style="-", width=2, color="r")


def draw_line(start: point, end: point, formatting: LineFormatting = DEFAULT_LINE_FORMATTING):
    """Draws a line in the current plot at the provided coordinates"""
    # TODO: Figure out how to respect color and make sure it is respected.
    plt.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        linestyle=formatting.style,
        linewidth=formatting.width,
        color=formatting.color
    )


def draw_polygon(points: [point], formatting: LineFormatting = DEFAULT_LINE_FORMATTING):
    """Draws a polygon in the current plot at the provided coorinates"""
    if points is None or len(points) <= 2:
        raise Exception(f"Cannot plot polygon with less than 3 points.")

    start: point = points[0]
    for i in range(1, len(points)):
        # Draw line from prev to points[i]
        end: point = points[i]
        draw_line(start, end, formatting)
        start = end

    # Draw the last point to the end
    draw_line(points[len(points) - 1], points[0], formatting)
