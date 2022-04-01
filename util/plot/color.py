from typing import List


def generate_red_range(num_colors: int) -> List[str]:
    """ Returns a list of reds tat spans all possible values and has granularity num_colors"""
    x: float = 1 / num_colors
    return [(1, 1 - (x * i), 1 - (x * i)) for i in range(num_colors)]
